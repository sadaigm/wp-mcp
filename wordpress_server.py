"""
WordPress MCP Server
Provides tools for interacting with WordPress REST API to manage posts, pages, and categories.
"""

import os
import logging
from typing import Optional, List, Any, Dict, Union
import base64
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

mcp = FastMCP("WordPress", host="0.0.0.0", port=8000, json_response=True)

# Configuration
WP_URL = os.getenv("WP_URL", "")
WP_USERNAME = os.getenv("WP_USERNAME", "")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "")

def get_auth_headers() -> Dict[str, str]:
    """Generate basic authentication headers."""
    if not WP_USERNAME or not WP_APP_PASSWORD:
        raise ValueError("WP_USERNAME and WP_APP_PASSWORD environment variables must be set")

    credentials = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
    return {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }

def get_api_url(endpoint: str) -> str:
    """Construct full API URL."""
    if not WP_URL:
        raise ValueError("WP_URL environment variable must be set")
    base_url = WP_URL.rstrip("/")
    return f"{base_url}/wp-json/wp/v2/{endpoint}"

async def make_request(method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None, require_auth: bool = False) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Make HTTP request to WordPress API."""
    url = get_api_url(endpoint)
    headers = get_auth_headers() if method in ["POST", "PUT", "DELETE"] or require_auth else {}

    # Log request details
    logger.info(f"REST Request: {method} {url}")
    if params:
        logger.info(f"Query Params: {params}")
    if data:
        logger.info(f"Request Payload: {data}")
    if headers:
        # Log headers without sensitive data
        safe_headers = {k: v for k, v in headers.items() if k != "Authorization"}
        safe_headers["Authorization"] = f"Basic {headers['Authorization'][:20]}..." if "Authorization" in headers else ""
        logger.info(f"Request Headers: {safe_headers}")

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, headers=headers, params=params, timeout=30.0)
            elif method == "POST":
                response = await client.post(url, headers=headers, json=data, params=params, timeout=30.0)
            elif method == "PUT":
                response = await client.put(url, headers=headers, json=data, params=params, timeout=30.0)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers, params=params, timeout=30.0)
            else:
                raise ValueError(f"Unsupported method: {method}")

            # Log response details
            logger.info(f"Response Status: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")

            try:
                response_json = response.json()
                logger.info(f"Response Body: {response_json}")
            except Exception:
                logger.info(f"Response Body: {response.text[:500]}")

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status Error: {e.response.status_code}")
            logger.error(f"Error Response: {e.response.text}")
            return {
                "error": True,
                "status_code": e.response.status_code,
                "message": e.response.text
            }
        except httpx.RequestError as e:
            logger.error(f"Request Error: {str(e)}")
            return {
                "error": True,
                "message": f"Request failed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            return {
                "error": True,
                "message": f"Unexpected error: {str(e)}"
            }

# ==================== POSTS ====================

@mcp.tool()
async def list_posts(
    per_page: int = 10,
    page: int = 1,
    search: str = "",
    status: str = "publish",
    categories: Optional[str] = None,
    tags: Optional[str] = None,
    author: Optional[int] = None,
    order: str = "desc",
    orderby: str = "date"
) -> List[Dict[str, Any]]:
    """
    List WordPress posts with optional filtering.

    Args:
        per_page: Number of posts per page (max 100)
        page: Current page number
        search: Search term to filter posts
        status: Post status (publish, draft, pending, private, future)
        categories: Comma-separated category IDs
        tags: Comma-separated tag IDs
        author: Author ID
        order: Order direction (asc or desc)
        orderby: Order by field (date, title, modified, author, id)

    Returns:
        Dictionary with posts list or error
    """
    params = {
        "per_page": min(per_page, 100),
        "page": page,
        "order": order,
        "orderby": orderby
    }

    if search:
        params["search"] = search
    if status:
        params["status"] = status
    if categories:
        params["categories"] = categories
    if tags:
        params["tags"] = tags
    if author:
        params["author"] = author

    # Require auth for non-public statuses
    require_auth = status in ["draft", "pending", "private", "future"]
    return await make_request("GET", "posts", params=params, require_auth=require_auth)

@mcp.tool()
async def get_post(post_id: int) -> Dict[str, Any]:
    """
    Retrieve a single WordPress post by ID.

    Args:
        post_id: The post ID

    Returns:
        Dictionary with post data or error
    """
    return await make_request("GET", f"posts/{post_id}")

@mcp.tool()
async def create_post(
    title: str,
    content: str,
    status: str = "draft",
    excerpt: str = "",
    author: Optional[int] = None,
    categories: Optional[List[int]] = None,
    tags: Optional[List[int]] = None,
    featured_media: Optional[int] = None,
    comment_status: str = "open",
    ping_status: str = "open"
) -> Dict[str, Any]:
    """
    Create a new WordPress post.

    Args:
        title: Post title
        content: Post content (HTML allowed)
        status: Post status (publish, draft, pending, private, future)
        excerpt: Post excerpt
        author: Author ID
        categories: List of category IDs
        tags: List of tag IDs
        featured_media: Featured media ID
        comment_status: Comment status (open or closed)
        ping_status: Ping status (open or closed)

    Returns:
        Dictionary with created post data or error
    """
    data = {
        "title": title,
        "content": content,
        "status": status,
        "excerpt": excerpt,
        "comment_status": comment_status,
        "ping_status": ping_status
    }

    if author is not None:
        data["author"] = author
    if categories:
        data["categories"] = categories
    if tags:
        data["tags"] = tags
    if featured_media is not None:
        data["featured_media"] = featured_media

    return await make_request("POST", "posts", data=data)

@mcp.tool()
async def update_post(
    post_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    status: Optional[str] = None,
    excerpt: Optional[str] = None,
    categories: Optional[List[int]] = None,
    tags: Optional[List[int]] = None,
    featured_media: Optional[int] = None
) -> Dict[str, Any]:
    """
    Update an existing WordPress post.

    Args:
        post_id: The post ID
        title: Post title
        content: Post content
        status: Post status
        excerpt: Post excerpt
        categories: List of category IDs
        tags: List of tag IDs
        featured_media: Featured media ID

    Returns:
        Dictionary with updated post data or error
    """
    data = {}
    if title is not None:
        data["title"] = title
    if content is not None:
        data["content"] = content
    if status is not None:
        data["status"] = status
    if excerpt is not None:
        data["excerpt"] = excerpt
    if categories is not None:
        data["categories"] = categories
    if tags is not None:
        data["tags"] = tags
    if featured_media is not None:
        data["featured_media"] = featured_media

    return await make_request("POST", f"posts/{post_id}", data=data)

@mcp.tool()
async def delete_post(post_id: int, force: bool = False) -> Dict[str, Any]:
    """
    Delete a WordPress post.

    Args:
        post_id: The post ID
        force: Whether to bypass trash and force permanent deletion

    Returns:
        Dictionary with deletion result or error
    """
    params = {"force": "true" if force else "false"}
    return await make_request("DELETE", f"posts/{post_id}", params=params)

@mcp.tool()
async def list_draft_posts(per_page: int = 100, page: int = 1) -> List[Dict[str, Any]]:
    """
    List all draft posts in WordPress.

    Args:
        per_page: Number of posts per page (max 100)
        page: Current page number

    Returns:
        Dictionary with draft posts list or error
    """
    return await make_request("GET", "posts", params={"status": "draft", "per_page": min(per_page, 100), "page": page}, require_auth=True)

@mcp.tool()
async def publish_post(post_id: int) -> Dict[str, Any]:
    """
    Publish a single draft post immediately.

    Args:
        post_id: The post ID to publish

    Returns:
        Dictionary with updated post data or error
    """
    return await make_request("POST", f"posts/{post_id}", data={"status": "publish"})

@mcp.tool()
async def publish_bulk_posts(post_ids: List[int]) -> Dict[str, Any]:
    """
    Publish multiple draft posts at once.

    Args:
        post_ids: List of post IDs to publish

    Returns:
        Dictionary with results for each post:
        - successful: List of successfully published posts
        - failed: List of failed publish attempts with error messages
    """
    results = {"successful": [], "failed": []}

    for post_id in post_ids:
        try:
            result = await make_request("POST", f"posts/{post_id}", data={"status": "publish"})
            if result.get("error"):
                results["failed"].append({"post_id": post_id, "error": result})
            else:
                results["successful"].append({"post_id": post_id, "post": result})
        except Exception as e:
            results["failed"].append({"post_id": post_id, "error": str(e)})

    return results

@mcp.tool()
async def publish_all_drafts() -> Dict[str, Any]:
    """
    Publish ALL draft posts at once.

    This tool will:
    1. Fetch all draft posts (handles pagination automatically)
    2. Publish each draft post
    3. Return a summary of the operation

    Returns:
        Dictionary with:
        - total_found: Total number of draft posts found
        - successful: List of successfully published posts
        - failed: List of failed publish attempts with error messages
    """
    page = 1
    all_draft_ids = []

    # Fetch all draft posts (handle pagination)
    while True:
        drafts = await make_request("GET", "posts", params={"status": "draft", "per_page": 100, "page": page}, require_auth=True)

        if not isinstance(drafts, list):
            return {"error": True, "message": "Failed to fetch draft posts", "details": drafts}

        if not drafts:
            break

        all_draft_ids.extend([post["id"] for post in drafts])

        # If we got less than 100, we're done
        if len(drafts) < 100:
            break

        page += 1

    # Publish all drafts
    return await publish_bulk_posts(all_draft_ids)

# ==================== PAGES ====================

@mcp.tool()
async def list_pages(
    per_page: int = 10,
    page: int = 1,
    search: str = "",
    status: str = "publish",
    parent: Optional[int] = None,
    parent_exclude: Optional[List[int]] = None,
    order: str = "asc",
    orderby: str = "menu_order"
) -> List[Dict[str, Any]]:
    """
    List WordPress pages with optional filtering.

    Args:
        per_page: Number of pages per page (max 100)
        page: Current page number
        search: Search term to filter pages
        status: Page status (publish, draft, pending, private)
        parent: Parent page ID filter
        parent_exclude: Exclude parent page IDs
        order: Order direction (asc or desc)
        orderby: Order by field (date, title, menu_order, modified, parent)

    Returns:
        Dictionary with pages list or error
    """
    params = {
        "per_page": min(per_page, 100),
        "page": page,
        "order": order,
        "orderby": orderby
    }

    if search:
        params["search"] = search
    if status:
        params["status"] = status
    if parent is not None:
        params["parent"] = parent
    if parent_exclude:
        params["parent_exclude"] = ",".join(map(str, parent_exclude))

    # Require auth for non-public statuses
    require_auth = status in ["draft", "pending", "private"]
    return await make_request("GET", "pages", params=params, require_auth=require_auth)

@mcp.tool()
async def get_page(page_id: int) -> Dict[str, Any]:
    """
    Retrieve a single WordPress page by ID.

    Args:
        page_id: The page ID

    Returns:
        Dictionary with page data or error
    """
    return await make_request("GET", f"pages/{page_id}")

@mcp.tool()
async def create_page(
    title: str,
    content: str,
    status: str = "draft",
    excerpt: str = "",
    parent: int = 0,
    menu_order: int = 0,
    author: Optional[int] = None,
    featured_media: Optional[int] = None,
    comment_status: str = "closed",
    ping_status: str = "closed",
    template: str = ""
) -> Dict[str, Any]:
    """
    Create a new WordPress page.

    Args:
        title: Page title
        content: Page content (HTML allowed)
        status: Page status (publish, draft, pending, private)
        excerpt: Page excerpt
        parent: Parent page ID (0 for top-level)
        menu_order: Order in navigation
        author: Author ID
        featured_media: Featured media ID
        comment_status: Comment status (open or closed)
        ping_status: Ping status (open or closed)
        template: Template file name

    Returns:
        Dictionary with created page data or error
    """
    data = {
        "title": title,
        "content": content,
        "status": status,
        "excerpt": excerpt,
        "parent": parent,
        "menu_order": menu_order,
        "comment_status": comment_status,
        "ping_status": ping_status
    }

    if author is not None:
        data["author"] = author
    if featured_media is not None:
        data["featured_media"] = featured_media
    if template:
        data["template"] = template

    return await make_request("POST", "pages", data=data)

@mcp.tool()
async def update_page(
    page_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    status: Optional[str] = None,
    excerpt: Optional[str] = None,
    parent: Optional[int] = None,
    menu_order: Optional[int] = None,
    featured_media: Optional[int] = None
) -> Dict[str, Any]:
    """
    Update an existing WordPress page.

    Args:
        page_id: The page ID
        title: Page title
        content: Page content
        status: Page status
        excerpt: Page excerpt
        parent: Parent page ID
        menu_order: Order in navigation
        featured_media: Featured media ID

    Returns:
        Dictionary with updated page data or error
    """
    data = {}
    if title is not None:
        data["title"] = title
    if content is not None:
        data["content"] = content
    if status is not None:
        data["status"] = status
    if excerpt is not None:
        data["excerpt"] = excerpt
    if parent is not None:
        data["parent"] = parent
    if menu_order is not None:
        data["menu_order"] = menu_order
    if featured_media is not None:
        data["featured_media"] = featured_media

    return await make_request("POST", f"pages/{page_id}", data=data)

@mcp.tool()
async def delete_page(page_id: int, force: bool = False) -> Dict[str, Any]:
    """
    Delete a WordPress page.

    Args:
        page_id: The page ID
        force: Whether to bypass trash and force permanent deletion

    Returns:
        Dictionary with deletion result or error
    """
    params = {"force": "true" if force else "false"}
    return await make_request("DELETE", f"pages/{page_id}", params=params)

@mcp.tool()
async def list_draft_pages(per_page: int = 100, page: int = 1) -> List[Dict[str, Any]]:
    """
    List all draft pages in WordPress.

    Args:
        per_page: Number of pages per page (max 100)
        page: Current page number

    Returns:
        Dictionary with draft pages list or error
    """
    return await make_request("GET", "pages", params={"status": "draft", "per_page": min(per_page, 100), "page": page}, require_auth=True)

@mcp.tool()
async def publish_page(page_id: int) -> Dict[str, Any]:
    """
    Publish a single draft page immediately.

    Args:
        page_id: The page ID to publish

    Returns:
        Dictionary with updated page data or error
    """
    return await make_request("POST", f"pages/{page_id}", data={"status": "publish"})

@mcp.tool()
async def publish_bulk_pages(page_ids: List[int]) -> Dict[str, Any]:
    """
    Publish multiple draft pages at once.

    Args:
        page_ids: List of page IDs to publish

    Returns:
        Dictionary with results for each page:
        - successful: List of successfully published pages
        - failed: List of failed publish attempts with error messages
    """
    results = {"successful": [], "failed": []}

    for page_id in page_ids:
        try:
            result = await make_request("POST", f"pages/{page_id}", data={"status": "publish"})
            if result.get("error"):
                results["failed"].append({"page_id": page_id, "error": result})
            else:
                results["successful"].append({"page_id": page_id, "page": result})
        except Exception as e:
            results["failed"].append({"page_id": page_id, "error": str(e)})

    return results

@mcp.tool()
async def publish_all_draft_pages() -> Dict[str, Any]:
    """
    Publish ALL draft pages at once.

    This tool will:
    1. Fetch all draft pages (handles pagination automatically)
    2. Publish each draft page
    3. Return a summary of the operation

    Returns:
        Dictionary with:
        - total_found: Total number of draft pages found
        - successful: List of successfully published pages
        - failed: List of failed publish attempts with error messages
    """
    page = 1
    all_draft_ids = []

    # Fetch all draft pages (handle pagination)
    while True:
        drafts = await make_request("GET", "pages", params={"status": "draft", "per_page": 100, "page": page}, require_auth=True)

        if not isinstance(drafts, list):
            return {"error": True, "message": "Failed to fetch draft pages", "details": drafts}

        if not drafts:
            break

        all_draft_ids.extend([page_data["id"] for page_data in drafts])

        # If we got less than 100, we're done
        if len(drafts) < 100:
            break

        page += 1

    # Publish all drafts
    return await publish_bulk_pages(all_draft_ids)

# ==================== CATEGORIES ====================

@mcp.tool()
async def list_categories(
    per_page: int = 10,
    page: int = 1,
    search: str = "",
    hide_empty: bool = False,
    parent: Optional[int] = None,
    order: str = "asc",
    orderby: str = "name"
) -> List[Dict[str, Any]]:
    """
    List WordPress categories with optional filtering.

    Args:
        per_page: Number of categories per page (max 100)
        page: Current page number
        search: Search term to filter categories
        hide_empty: Whether to hide empty categories
        parent: Parent category ID filter
        order: Order direction (asc or desc)
        orderby: Order by field (id, name, slug, count, description)

    Returns:
        Dictionary with categories list or error
    """
    params = {
        "per_page": min(per_page, 100),
        "page": page,
        "order": order,
        "orderby": orderby
    }

    if search:
        params["search"] = search
    if hide_empty:
        params["hide_empty"] = "true"
    if parent is not None:
        params["parent"] = parent

    return await make_request("GET", "categories", params=params)

@mcp.tool()
async def get_category(category_id: int) -> Dict[str, Any]:
    """
    Retrieve a single WordPress category by ID.

    Args:
        category_id: The category ID

    Returns:
        Dictionary with category data or error
    """
    return await make_request("GET", f"categories/{category_id}")

@mcp.tool()
async def create_category(
    name: str,
    description: str = "",
    slug: str = "",
    parent: int = 0
) -> Dict[str, Any]:
    """
    Create a new WordPress category.

    Args:
        name: Category name (required)
        description: Category description
        slug: URL-friendly slug
        parent: Parent category ID (0 for top-level)

    Returns:
        Dictionary with created category data or error
    """
    data = {
        "name": name,
        "description": description,
        "parent": parent
    }

    if slug:
        data["slug"] = slug

    return await make_request("POST", "categories", data=data)

@mcp.tool()
async def update_category(
    category_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    slug: Optional[str] = None,
    parent: Optional[int] = None
) -> Dict[str, Any]:
    """
    Update an existing WordPress category.

    Args:
        category_id: The category ID
        name: Category name
        description: Category description
        slug: URL-friendly slug
        parent: Parent category ID

    Returns:
        Dictionary with updated category data or error
    """
    data = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if slug is not None:
        data["slug"] = slug
    if parent is not None:
        data["parent"] = parent

    return await make_request("POST", f"categories/{category_id}", data=data)

@mcp.tool()
async def delete_category(category_id: int) -> Dict[str, Any]:
    """
    Delete a WordPress category.

    Args:
        category_id: The category ID

    Returns:
        Dictionary with deletion result or error
    """
    return await make_request("DELETE", f"categories/{category_id}", params={"force": "true"})

# ==================== TAGS ====================

@mcp.tool()
async def list_tags(
    per_page: int = 10,
    page: int = 1,
    search: str = "",
    hide_empty: bool = False,
    order: str = "asc",
    orderby: str = "name"
) -> List[Dict[str, Any]]:
    """
    List WordPress tags with optional filtering.

    Args:
        per_page: Number of tags per page (max 100)
        page: Current page number
        search: Search term to filter tags
        hide_empty: Whether to hide empty tags
        order: Order direction (asc or desc)
        orderby: Order by field (id, name, slug, count, description)

    Returns:
        Dictionary with tags list or error
    """
    params = {
        "per_page": min(per_page, 100),
        "page": page,
        "order": order,
        "orderby": orderby
    }

    if search:
        params["search"] = search
    if hide_empty:
        params["hide_empty"] = "true"

    return await make_request("GET", "tags", params=params)

@mcp.tool()
async def get_tag(tag_id: int) -> Dict[str, Any]:
    """
    Retrieve a single WordPress tag by ID.

    Args:
        tag_id: The tag ID

    Returns:
        Dictionary with tag data or error
    """
    return await make_request("GET", f"tags/{tag_id}")

@mcp.tool()
async def create_tag(
    name: str,
    description: str = "",
    slug: str = ""
) -> Dict[str, Any]:
    """
    Create a new WordPress tag.

    Args:
        name: Tag name (required)
        description: Tag description
        slug: URL-friendly slug

    Returns:
        Dictionary with created tag data or error
    """
    data = {
        "name": name,
        "description": description
    }

    if slug:
        data["slug"] = slug

    return await make_request("POST", "tags", data=data)

@mcp.tool()
async def update_tag(
    tag_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    slug: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing WordPress tag.

    Args:
        tag_id: The tag ID
        name: Tag name
        description: Tag description
        slug: URL-friendly slug

    Returns:
        Dictionary with updated tag data or error
    """
    data = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if slug is not None:
        data["slug"] = slug

    return await make_request("POST", f"tags/{tag_id}", data=data)

@mcp.tool()
async def delete_tag(tag_id: int) -> Dict[str, Any]:
    """
    Delete a WordPress tag.

    Args:
        tag_id: The tag ID

    Returns:
        Dictionary with deletion result or error
    """
    return await make_request("DELETE", f"tags/{tag_id}", params={"force": "true"})

# ==================== COMMENTS ====================

@mcp.tool()
async def list_comments(
    per_page: int = 10,
    page: int = 1,
    search: str = "",
    post: Optional[int] = None,
    status: str = "approve",
    parent: Optional[int] = None,
    order: str = "desc",
    orderby: str = "date_gmt"
) -> List[Dict[str, Any]]:
    """
    List WordPress comments with optional filtering.

    Args:
        per_page: Number of comments per page (max 100)
        page: Current page number
        search: Search term to filter comments
        post: Filter by post ID
        status: Comment status (approve, hold, spam, trash)
        parent: Parent comment ID (for threaded comments)
        order: Order direction (asc or desc)
        orderby: Order by field (date, date_gmt, id, post, parent)

    Returns:
        Dictionary with comments list or error
    """
    params = {
        "per_page": min(per_page, 100),
        "page": page,
        "order": order,
        "orderby": orderby
    }

    if search:
        params["search"] = search
    if post:
        params["post"] = post
    if status:
        params["status"] = status
    if parent is not None:
        params["parent"] = parent

    # Require auth for non-approved comments
    require_auth = status in ["hold", "spam", "trash"]
    return await make_request("GET", "comments", params=params, require_auth=require_auth)

@mcp.tool()
async def get_comment(comment_id: int) -> Dict[str, Any]:
    """
    Retrieve a single WordPress comment by ID.

    Args:
        comment_id: The comment ID

    Returns:
        Dictionary with comment data or error
    """
    return await make_request("GET", f"comments/{comment_id}")

@mcp.tool()
async def create_comment(
    post: int,
    content: str,
    author_name: str = "",
    author_email: str = "",
    author_url: str = "",
    parent: int = 0,
    status: str = "hold"
) -> Dict[str, Any]:
    """
    Create a new WordPress comment.

    Args:
        post: Associated post ID (required)
        content: Comment content (required)
        author_name: Display name for comment author
        author_email: Email address for comment author
        author_url: URL for comment author
        parent: Parent comment ID (0 for top-level)
        status: Comment status (approve, hold, spam)

    Returns:
        Dictionary with created comment data or error
    """
    data = {
        "post": post,
        "content": content,
        "parent": parent
    }

    if author_name:
        data["author_name"] = author_name
    if author_email:
        data["author_email"] = author_email
    if author_url:
        data["author_url"] = author_url
    if status:
        data["status"] = status

    return await make_request("POST", "comments", data=data)

@mcp.tool()
async def update_comment(
    comment_id: int,
    content: Optional[str] = None,
    status: Optional[str] = None,
    author_name: Optional[str] = None,
    author_email: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing WordPress comment.

    Args:
        comment_id: The comment ID
        content: Comment content
        status: Comment status (approve, hold, spam, trash)
        author_name: Display name for comment author
        author_email: Email address for comment author

    Returns:
        Dictionary with updated comment data or error
    """
    data = {}
    if content is not None:
        data["content"] = content
    if status is not None:
        data["status"] = status
    if author_name is not None:
        data["author_name"] = author_name
    if author_email is not None:
        data["author_email"] = author_email

    return await make_request("POST", f"comments/{comment_id}", data=data)

@mcp.tool()
async def approve_comment(comment_id: int) -> Dict[str, Any]:
    """
    Approve a comment immediately.

    Args:
        comment_id: The comment ID to approve

    Returns:
        Dictionary with updated comment data or error
    """
    return await make_request("POST", f"comments/{comment_id}", data={"status": "approve"})

@mcp.tool()
async def spam_comment(comment_id: int) -> Dict[str, Any]:
    """
    Mark a comment as spam.

    Args:
        comment_id: The comment ID to mark as spam

    Returns:
        Dictionary with updated comment data or error
    """
    return await make_request("POST", f"comments/{comment_id}", data={"status": "spam"})

@mcp.tool()
async def delete_comment(comment_id: int, force: bool = False) -> Dict[str, Any]:
    """
    Delete a WordPress comment.

    Args:
        comment_id: The comment ID
        force: Whether to bypass trash and force permanent deletion

    Returns:
        Dictionary with deletion result or error
    """
    params = {"force": "true" if force else "false"}
    return await make_request("DELETE", f"comments/{comment_id}", params=params)

@mcp.tool()
async def list_pending_comments(per_page: int = 100, page: int = 1) -> List[Dict[str, Any]]:
    """
    List all pending comments for moderation.

    Args:
        per_page: Number of comments per page (max 100)
        page: Current page number

    Returns:
        Dictionary with pending comments list or error
    """
    return await make_request("GET", "comments", params={"status": "hold", "per_page": min(per_page, 100), "page": page}, require_auth=True)

@mcp.tool()
async def bulk_approve_comments(comment_ids: List[int]) -> Dict[str, Any]:
    """
    Approve multiple comments at once.

    Args:
        comment_ids: List of comment IDs to approve

    Returns:
        Dictionary with results for each comment
    """
    results = {"successful": [], "failed": []}

    for comment_id in comment_ids:
        try:
            result = await make_request("POST", f"comments/{comment_id}", data={"status": "approve"})
            if result.get("error"):
                results["failed"].append({"comment_id": comment_id, "error": result})
            else:
                results["successful"].append({"comment_id": comment_id, "comment": result})
        except Exception as e:
            results["failed"].append({"comment_id": comment_id, "error": str(e)})

    return results

# ==================== SEARCH ====================

@mcp.tool()
async def search_site(
    search: str,
    per_page: int = 10,
    page: int = 1,
    type: Optional[str] = None,
    subtype: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Perform a site-wide search across WordPress content.

    Args:
        search: Search query string (required)
        per_page: Number of results per page (max 100)
        page: Current page number
        type: Object type filter (post, term, post-format)
        subtype: Object subtype filter (post, page, category, post_tag)

    Returns:
        Dictionary with search results including:
        - results: List of search results
        - type: Content type
        - subtype: Content subtype
        Each result has: id, title, url, type, subtype
    """
    params = {
        "search": search,
        "per_page": min(per_page, 100),
        "page": page
    }

    if type:
        params["type"] = type
    if subtype:
        params["subtype"] = subtype

    return await make_request("GET", "search", params=params)

@mcp.tool()
async def search_posts(search: str, per_page: int = 10, page: int = 1) -> List[Dict[str, Any]]:
    """
    Search only posts in WordPress.

    Args:
        search: Search query string
        per_page: Number of results per page (max 100)
        page: Current page number

    Returns:
        Dictionary with post search results
    """
    return await search_site(search=search, per_page=per_page, page=page, type="post", subtype="post")

@mcp.tool()
async def search_pages(search: str, per_page: int = 10, page: int = 1) -> List[Dict[str, Any]]:
    """
    Search only pages in WordPress.

    Args:
        search: Search query string
        per_page: Number of results per page (max 100)
        page: Current page number

    Returns:
        Dictionary with page search results
    """
    return await search_site(search=search, per_page=per_page, page=page, type="post", subtype="page")

# ==================== RESOURCES ====================

@mcp.resource("wordpress://posts/{status}")
async def get_posts_resource(status: str = "publish") -> str:
    """Get posts as a resource."""
    result = await list_posts(per_page=100, status=status)
    if isinstance(result, list):
        return f"Found {len(result)} {status} posts."
    return f"Error retrieving posts: {result}"

@mcp.resource("wordpress://pages")
async def get_pages_resource() -> str:
    """Get pages as a resource."""
    result = await list_pages(per_page=100)
    if isinstance(result, list):
        return f"Found {len(result)} pages."
    return f"Error retrieving pages: {result}"

@mcp.resource("wordpress://categories")
async def get_categories_resource() -> str:
    """Get categories as a resource."""
    result = await list_categories(per_page=100, hide_empty=False)
    if isinstance(result, list):
        return f"Found {len(result)} categories."
    return f"Error retrieving categories: {result}"

@mcp.resource("wordpress://tags")
async def get_tags_resource() -> str:
    """Get tags as a resource."""
    result = await list_tags(per_page=100, hide_empty=False)
    if isinstance(result, list):
        return f"Found {len(result)} tags."
    return f"Error retrieving tags: {result}"

@mcp.resource("wordpress://comments")
async def get_comments_resource() -> str:
    """Get comments as a resource."""
    result = await list_comments(per_page=100)
    if isinstance(result, list):
        return f"Found {len(result)} comments."
    return f"Error retrieving comments: {result}"

@mcp.resource("wordpress://pending-comments")
async def get_pending_comments_resource() -> str:
    """Get pending comments for moderation."""
    result = await list_pending_comments(per_page=100)
    if isinstance(result, list):
        return f"Found {len(result)} pending comments awaiting moderation."
    return f"Error retrieving pending comments: {result}"

# ==================== PROMPTS ====================

@mcp.prompt()
def create_blog_post(topic: str, tone: str = "professional") -> str:
    """Generate a prompt for creating a blog post."""
    return f"Write a {tone} blog post about {topic}. Include an engaging title, introduction, main body with several sections, and a conclusion."

@mcp.prompt()
def optimize_seo(content_type: str) -> str:
    """Generate a prompt for SEO optimization."""
    return f"Provide SEO recommendations for {content_type} in WordPress, including keyword placement, meta descriptions, and content structure."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
