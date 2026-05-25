# WordPress MCP Server

A Model Context Protocol (MCP) server for interacting with the WordPress REST API. This server provides tools for managing WordPress posts, pages, and categories through a standardized MCP interface.

## Features

- **Posts Management**: Create, read, update, and delete WordPress posts
- **Pages Management**: Create, read, update, and delete WordPress pages with hierarchical support
- **Categories Management**: Create, read, update, and delete WordPress categories
- **Authentication**: Basic authentication using WordPress Application Passwords
- **Resources**: Quick access to posts, pages, and categories
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

### Pages

| Tool | Description |
|------|-------------|
| `list_pages` | List pages with filtering options |
| `get_page` | Retrieve a single page by ID |
| `create_page` | Create a new page |
| `update_page` | Update an existing page |
| `delete_page` | Delete a page (move to trash or force delete) |

### Categories

| Tool | Description |
|------|-------------|
| `list_categories` | List categories with filtering options |
| `get_category` | Retrieve a single category by ID |
| `create_category` | Create a new category |
| `update_category` | Update an existing category |
| `delete_category` | Delete a category |

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
