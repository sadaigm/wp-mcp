# WordPress MCP Server

A Model Context Protocol (MCP) server for interacting with the WordPress REST API. This server provides tools for managing WordPress posts, pages, categories, and tags through a standardized MCP interface.

## Features

- **Posts Management**: Create, read, update, and delete WordPress posts
- **Pages Management**: Create, read, update, and delete WordPress pages with hierarchical support
- **Categories Management**: Create, read, update, and delete WordPress categories with parent-child relationships
- **Tags Management**: Create, read, update, and delete WordPress tags for content labeling
- **Authentication**: Basic authentication using WordPress Application Passwords
- **Resources**: Quick access to posts, pages, categories, and tags
- **Prompts**: Pre-built prompts for content creation and SEO optimization

## Installation

### Option 1: Docker (Recommended)

1. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your WordPress credentials
```

2. Build and run with Docker:
```bash
# Build the image
./build-image.sh

# Or with docker-compose
docker-compose up -d
```

3. The server will be available at `http://localhost:8000`

### Option 2: Local Python

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables (see Configuration section below)

3. Run the server:
```bash
python wordpress_server.py
```

## Configuration

The server requires the following environment variables:

### Required Environment Variables

Create a `.env` file or set these in your environment:

```bash
# WordPress site URL (without trailing slash)
WP_URL=https://example.com

# WordPress username
WP_USERNAME=admin

# WordPress Application Password (create in WP Admin > Users > Profile > Application Passwords)
WP_APP_PASSWORD=abcd-efgh-ijkl-mnop-1234-5678
```

### Creating an Application Password in WordPress

1. Log in to your WordPress admin dashboard
2. Go to **Users** > **Profile**
3. Scroll down to **Application Passwords** section
4. Enter a name (e.g., "MCP Server")
5. Click **Add New Application Password**
6. Copy the generated password (you'll only see it once!)

## Available Tools

### Posts

| Tool | Description |
|------|-------------|
| `list_posts` | List posts with filtering options |
| `get_post` | Retrieve a single post by ID |
| `create_post` | Create a new post |
| `update_post` | Update an existing post |
| `delete_post` | Delete a post (move to trash or force delete) |
| `list_draft_posts` | List all draft posts |
| `publish_post` | Publish a single draft post |
| `publish_bulk_posts` | Publish multiple posts at once |
| `publish_all_drafts` | Publish ALL draft posts at once |

### Pages

| Tool | Description |
|------|-------------|
| `list_pages` | List pages with filtering options |
| `get_page` | Retrieve a single page by ID |
| `create_page` | Create a new page |
| `update_page` | Update an existing page |
| `delete_page` | Delete a page (move to trash or force delete) |
| `list_draft_pages` | List all draft pages |
| `publish_page` | Publish a single draft page |
| `publish_bulk_pages` | Publish multiple pages at once |
| `publish_all_draft_pages` | Publish ALL draft pages at once |

### Categories

| Tool | Description |
|------|-------------|
| `list_categories` | List categories with filtering options |
| `get_category` | Retrieve a single category by ID |
| `create_category` | Create a new category |
| `update_category` | Update an existing category |
| `delete_category` | Delete a category |

### Tags

| Tool | Description |
|------|-------------|
| `list_tags` | List tags with filtering options |
| `get_tag` | Retrieve a single tag by ID |
| `create_tag` | Create a new tag |
| `update_tag` | Update an existing tag |
| `delete_tag` | Delete a tag |

## Usage Examples

### Creating a Post

```python
# Via MCP client
result = await create_post(
    title="My New Post",
    content="This is the post content with <strong>HTML</strong>.",
    status="draft",
    categories=[5, 10],
    tags=[15]
)
```

### Draft to Publish Workflow

```python
# 1. Create posts as drafts
post1 = await create_post(
    title="First Draft",
    content="Content for first post",
    status="draft"
)

post2 = await create_post(
    title="Second Draft",
    content="Content for second post",
    status="draft"
)

# 2. Review your draft posts
drafts = await list_draft_posts()
print(f"Found {len(drafts)} draft posts to review")

# 3. Publish a single post
await publish_post(post_id=post1["id"])

# 4. Or publish multiple specific posts
await publish_bulk_posts(post_ids=[post1["id"], post2["id"]])

# 5. Or publish ALL drafts at once
result = await publish_all_drafts()
print(f"Published {len(result['successful'])} posts")
if result['failed']:
    print(f"Failed to publish {len(result['failed'])} posts")
```

### Creating a Page Hierarchy

```python
# Create parent page
parent = await create_page(
    title="Services",
    content="Our services overview",
    status="publish"
)

# Create child pages
await create_page(
    title="Web Development",
    content="Web development services",
    parent=parent["id"],
    menu_order=1
)
```

### Managing Categories

```python
# Create a category with children
tech = await create_category(
    name="Technology",
    description="Tech-related posts"
)

await create_category(
    name="Python",
    parent=tech["id"]
)
```

### Managing Tags

```python
# Create multiple tags for content organization
javascript = await create_tag(
    name="JavaScript",
    description="JavaScript programming posts"
)

tutorial = await create_tag(
    name="Tutorial",
    description="Tutorial and how-to content"
)

# Assign tags to posts
await update_post(
    post_id=42,
    tags=[javascript["id"], tutorial["id"]]
)
```

## Server Configuration

The server uses FastMCP with streamable HTTP transport by default. You can customize the host and port by modifying the server initialization:

```python
mcp = FastMCP("WordPress", host="0.0.0.0", port=8000, json_response=True)
```

## Security Notes

- Always use HTTPS for your WordPress site URL
- Keep Application Passwords secure and never commit them to version control
- Create dedicated Application Passwords for each integration
- Rotate Application Passwords periodically
- The server requires authentication for write operations (POST, PUT, DELETE)

## Error Handling

The server returns error information in the following format:

```json
{
  "error": true,
  "status_code": 401,
  "message": "Sorry, you are not allowed to do that."
}
```

Common HTTP status codes:
- `401` - Authentication failed or missing
- `400` - Invalid request parameters
- `404` - Resource not found
- `403` - Forbidden (insufficient permissions)

## Development

### Project Structure

```
wp-mcp/
├── wordpress_server.py      # Main server implementation
├── pyproject.toml           # Project configuration
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose configuration
├── build-image.sh           # Build script for Docker image
├── .dockerignore            # Files to exclude from Docker build
├── README.md                # This file
├── .env.example             # Example environment variables
└── docs/                    # API documentation
```

### Docker Deployment

The Docker setup includes:
- **Health checks**: Monitors server availability
- **Auto-restart**: Container restarts on failure
- **Environment variables**: Loaded from `.env` file
- **Exposed port**: 8000 (configurable via docker-compose.yml)

#### Docker Commands

```bash
# Build the image
docker build -t wp-mcp:latest .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### Adding New Tools

To add a new tool, decorate a function with `@mcp.tool()`:

```python
@mcp.tool()
async def my_new_tool(param: str) -> Dict[str, Any]:
    """Tool description."""
    # Implementation
    return result
```

## License

MIT

## Resources

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
