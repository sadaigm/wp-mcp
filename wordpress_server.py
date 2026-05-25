"""
WordPress MCP Server
Provides tools for interacting with WordPress REST API to manage posts, pages, and categories.
"""

import os
import logging
from typing import Optional, List, Any, Dict
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

async def make_request(method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
    """Make HTTP request to WordPress API."""
    url = get_api_url(endpoint)
    headers = get_auth_headers() if method in ["POST", "PUT", "DELETE"] else {}

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
) -> Dict[str, Any]:
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

    return await make_request("GET", "posts", params=params)

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
) -> Dict[str, Any]:
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

    return await make_request("GET", "pages", params=params)

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
) -> Dict[str, Any]:
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
