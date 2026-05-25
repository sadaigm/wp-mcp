# WordPress REST API: Posts Endpoint Documentation

This documentation covers the WordPress REST API Posts endpoint (`/wp/v2/posts`), which allows you to programmatically retrieve, create, update, and delete WordPress posts.

## Table of Contents

- [Authentication](#authentication)
- [Post Schema](#post-schema)
- [List Posts](#list-posts)
- [Retrieve a Single Post](#retrieve-a-single-post)
- [Create a Post](#create-a-post)
- [Update a Post](#update-a-post)
- [Delete a Post](#delete-a-post)

---

## Authentication

For read operations (GET requests), authentication is typically not required for public posts. However, for write operations (POST, PUT, DELETE), you must authenticate.

### Authentication Methods

1. **Cookie Authentication**: Use when making requests from the WordPress admin area
2. **OAuth2 Authentication**: Use for third-party applications
3. **Basic Authentication**: Use with Application Passwords for simple cases
4. **JWT Authentication**: Use JSON Web Tokens for stateless authentication

### Example: Basic Authentication with Application Password

```bash
curl -u username:application_password https://example.com/wp-json/wp/v2/posts
```

### Example: Bearer Token Header

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://example.com/wp-json/wp/v2/posts
```

---

## Post Schema

The schema defines all fields available in a post record:

| Field | Type | Context | Description |
|-------|------|---------|-------------|
| `id` | integer | view, edit, embed | Unique identifier for the post (read-only) |
| `date` | string/null | view, edit, embed | Date published in site's timezone |
| `date_gmt` | string/null | view, edit | Date published as GMT |
| `guid` | object | view, edit | Globally unique identifier (read-only) |
| `modified` | string | view, edit | Date last modified (read-only) |
| `modified_gmt` | string | view, edit | Date last modified as GMT (read-only) |
| `password` | string | edit | Password to protect access |
| `slug` | string | view, edit, embed | URL-friendly identifier |
| `status` | string | view, edit | One of: `publish`, `future`, `draft`, `pending`, `private` |
| `type` | string | view, edit, embed | Post type (read-only) |
| `permalink_template` | string | edit | Permalink template (read-only) |
| `generated_slug` | string | edit | Auto-generated slug (read-only) |
| `title` | object | view, edit, embed | Post title |
| `content` | object | view, edit | Post content |
| `author` | integer | view, edit, embed | Author ID |
| `excerpt` | object | view, edit, embed | Post excerpt |
| `featured_media` | integer | view, edit, embed | Featured media ID |
| `comment_status` | string | view, edit | One of: `open`, `closed` |
| `ping_status` | string | view, edit | One of: `open`, `closed` |
| `format` | string | view, edit | One of: `standard`, `aside`, `chat`, `gallery`, `link`, `image`, `quote`, `status`, `video`, `audio` |
| `meta` | object | view, edit | Meta fields |
| `sticky` | boolean | view, edit | Whether to treat as sticky |
| `template` | string | view, edit | Theme file to use |
| `categories` | array | view, edit | Category terms |
| `tags` | array | view, edit | Tag terms |

---

## List Posts

Retrieve a collection of posts with optional filtering and pagination.

### Endpoint

```
GET /wp/v2/posts
```

### Example Request

```bash
# Basic request
curl https://example.com/wp-json/wp/v2/posts

# With query parameters
curl "https://example.com/wp-json/wp/v2/posts?per_page=5&page=1"
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `context` | string | `view` | Scope of request: `view`, `embed`, `edit` |
| `page` | integer | `1` | Current page of the collection |
| `per_page` | integer | `10` | Maximum items per page (max 100) |
| `search` | string | - | Limit results to matching string |
| `after` | string | - | ISO8601 compliant date - posts published after |
| `before` | string | - | ISO8601 compliant date - posts published before |
| `author` | array | - | Limit to specific author IDs |
| `author_exclude` | array | - | Exclude specific author IDs |
| `exclude` | array | - | Exclude specific IDs |
| `include` | array | - | Limit to specific IDs |
| `offset` | integer | - | Offset result set by number |
| `order` | string | `desc` | `asc` or `desc` |
| `orderby` | string | `date` | `author`, `date`, `id`, `include`, `modified`, `parent`, `relevance`, `slug`, `title` |
| `search_columns` | array | - | Column names to search |
| `slug` | array | - | Limit to specific slugs |
| `status` | string | `publish` | One or more statuses |
| `categories` | array | - | Limit to specific category IDs |
| `categories_exclude` | array | - | Exclude specific category IDs |
| `tags` | array | - | Limit to specific tag IDs |
| `tags_exclude` | array | - | Exclude specific tag IDs |
| `sticky` | boolean | - | Limit to sticky posts |

### Example Response

```json
[
  {
    "id": 1,
    "date": "2024-01-15T10:00:00",
    "date_gmt": "2024-01-15T15:00:00",
    "guid": {
      "rendered": "https://example.com/?p=1"
    },
    "modified": "2024-01-15T10:00:00",
    "modified_gmt": "2024-01-15T15:00:00",
    "slug": "hello-world",
    "status": "publish",
    "type": "post",
    "link": "https://example.com/hello-world/",
    "title": {
      "rendered": "Hello World"
    },
    "content": {
      "rendered": "<p>Welcome to WordPress...</p>",
      "protected": false
    },
    "excerpt": {
      "rendered": "<p>Welcome to WordPress...</p>",
      "protected": false
    },
    "author": 1,
    "featured_media": 0,
    "comment_status": "open",
    "ping_status": "open",
    "sticky": false,
    "template": "",
    "format": "standard",
    "meta": [],
    "categories": [1],
    "tags": [],
    "_links": {
      "self": [{"href": "https://example.com/wp-json/wp/v2/posts/1"}],
      "collection": [{"href": "https://example.com/wp-json/wp/v2/posts"}]
    }
  }
]
```

---

## Retrieve a Single Post

Retrieve a specific post by its ID.

### Endpoint

```
GET /wp/v2/posts/<id>
```

### Example Request

```bash
curl https://example.com/wp-json/wp/v2/posts/1
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Unique identifier for the post |
| `context` | string | No | `view`, `embed`, `edit` (default: `view`) |
| `password` | string | No | Password if post is protected |

### Example Response

```json
{
  "id": 1,
  "date": "2024-01-15T10:00:00",
  "date_gmt": "2024-01-15T15:00:00",
  "guid": {
    "rendered": "https://example.com/?p=1"
  },
  "link": "https://example.com/hello-world/",
  "modified": "2024-01-15T10:00:00",
  "modified_gmt": "2024-01-15T15:00:00",
  "slug": "hello-world",
  "status": "publish",
  "type": "post",
  "title": {
    "rendered": "Hello World"
  },
  "content": {
    "rendered": "<p>Welcome to WordPress...</p>",
    "protected": false
  },
  "excerpt": {
    "rendered": "<p>Welcome to WordPress...</p>",
    "protected": false
  },
  "author": 1,
  "featured_media": 0,
  "comment_status": "open",
  "ping_status": "open",
  "sticky": false,
  "template": "",
  "format": "standard",
  "meta": [],
  "categories": [1],
  "tags": [],
  "_links": {
    "self": [{"href": "https://example.com/wp-json/wp/v2/posts/1"}],
    "collection": [{"href": "https://example.com/wp-json/wp/v2/posts"}],
    "author": [{"embeddable": true, "href": "https://example.com/wp-json/wp/v2/users/1"}]
  }
}
```

---

## Create a Post

Create a new post. Requires authentication.

### Endpoint

```
POST /wp/v2/posts
```

### Example Request

```bash
curl -X POST https://example.com/wp-json/wp/v2/posts \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "title": "My New Post",
    "content": "This is the post content with <strong>HTML formatting</strong>.",
    "status": "draft",
    "author": 1,
    "categories": [1, 5],
    "tags": [10, 15]
  }'
```

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | string/object | Yes | Post title |
| `content` | string/object | No | Post content |
| `excerpt` | string/object | No | Post excerpt |
| `status` | string | No | `publish`, `future`, `draft`, `pending`, `private` |
| `author` | integer | No | Author ID |
| `categories` | array | No | Category IDs |
| `tags` | array | No | Tag IDs |
| `featured_media` | integer | No | Featured media ID |
| `comment_status` | string | No | `open` or `closed` |
| `ping_status` | string | No | `open` or `closed` |
| `sticky` | boolean | No | Whether post is sticky |
| `format` | string | No | Post format |
| `date` | string | No | Publication date |
| `date_gmt` | string | No | Publication date as GMT |
| `slug` | string | No | URL slug |
| `password` | string | No | Post password |
| `meta` | object | No | Meta fields |

### Example Response

```json
{
  "id": 42,
  "date": "2024-01-20T14:30:00",
  "date_gmt": "2024-01-20T19:30:00",
  "guid": {
    "rendered": "https://example.com/?p=42"
  },
  "modified": "2024-01-20T14:30:00",
  "modified_gmt": "2024-01-20T19:30:00",
  "slug": "my-new-post",
  "status": "draft",
  "type": "post",
  "link": "https://example.com/?p=42",
  "title": {
    "rendered": "My New Post",
    "raw": "My New Post"
  },
  "content": {
    "rendered": "<p>This is the post content with <strong>HTML formatting</strong>.</p>",
    "raw": "This is the post content with <strong>HTML formatting</strong>."
  },
  "excerpt": {
    "rendered": "<p>This is the post content with <strong>HTML formatting</strong>.</p>",
    "raw": "This is the post content with <strong>HTML formatting</strong>."
  },
  "author": 1,
  "featured_media": 0,
  "comment_status": "open",
  "ping_status": "open",
  "sticky": false,
  "template": "",
  "format": "standard",
  "meta": [],
  "categories": [1, 5],
  "tags": [10, 15],
  "_links": {
    "self": [{"href": "https://example.com/wp-json/wp/v2/posts/42"}],
    "collection": [{"href": "https://example.com/wp-json/wp/v2/posts"}]
  }
}
```

---

## Update a Post

Update an existing post. Requires authentication.

### Endpoint

```
POST /wp/v2/posts/<id>
```

### Example Request

```bash
curl -X POST https://example.com/wp-json/wp/v2/posts/42 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "title": "Updated Post Title",
    "content": "Updated content here."
  }'
```

### Parameters

All parameters from [Create a Post](#create-a-post) are supported. Only include the fields you want to update.

### Example Response

```json
{
  "id": 42,
  "date": "2024-01-20T14:30:00",
  "date_gmt": "2024-01-20T19:30:00",
  "guid": {
    "rendered": "https://example.com/?p=42"
  },
  "modified": "2024-01-20T15:45:00",
  "modified_gmt": "2024-01-20T20:45:00",
  "slug": "my-new-post",
  "status": "draft",
  "type": "post",
  "link": "https://example.com/?p=42",
  "title": {
    "rendered": "Updated Post Title",
    "raw": "Updated Post Title"
  },
  "content": {
    "rendered": "<p>Updated content here.</p>",
    "raw": "Updated content here."
  },
  "excerpt": {
    "rendered": "<p>Updated content here.</p>",
    "raw": "Updated content here."
  },
  "author": 1,
  "featured_media": 0,
  "comment_status": "open",
  "ping_status": "open",
  "sticky": false,
  "template": "",
  "format": "standard",
  "meta": [],
  "categories": [1, 5],
  "tags": [10, 15]
}
```

---

## Delete a Post

Delete an existing post. Requires authentication.

### Endpoint

```
DELETE /wp/v2/posts/<id>
```

### Example Request

```bash
# Move to trash (default)
curl -X DELETE https://example.com/wp-json/wp/v2/posts/42 \
  -u username:application_password

# Force delete permanently
curl -X DELETE "https://example.com/wp-json/wp/v2/posts/42?force=true" \
  -u username:application_password
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | integer | - | Post ID |
| `force` | boolean | `false` | Bypass trash and force deletion |

### Example Response

```json
{
  "id": 42,
  "deleted": true,
  "previous": {
    "id": 42,
    "title": {
      "rendered": "Updated Post Title"
    },
    "status": "draft",
    "type": "post"
  }
}
```

---

## Common Use Cases

### Filter Posts by Category

```bash
curl "https://example.com/wp-json/wp/v2/posts?categories=5"
```

### Search Posts

```bash
curl "https://example.com/wp-json/wp/v2/posts?search=wordpress"
```

### Pagination

```bash
curl "https://example.com/wp-json/wp/v2/posts?per_page=20&page=2"
```

### Sort Posts

```bash
# Sort by title ascending
curl "https://example.com/wp-json/wp/v2/posts?orderby=title&order=asc"

# Sort by modification date
curl "https://example.com/wp-json/wp/v2/posts?orderby=modified"
```

### Retrieve Posts Modified After Date

```bash
curl "https://example.com/wp-json/wp/v2/posts?modified_after=2024-01-01T00:00:00"
```

---

## Error Responses

### 401 Unauthorized

```json
{
  "code": "rest_forbidden",
  "message": "Sorry, you are not allowed to do that.",
  "data": {
    "status": 401
  }
}
```

### 404 Not Found

```json
{
  "code": "rest_post_invalid_id",
  "message": "Invalid post ID.",
  "data": {
    "status": 404
  }
}
```

### 400 Bad Request

```json
{
  "code": "rest_invalid_param",
  "message": "Invalid parameter(s): status",
  "data": {
    "status": 400,
    "params": {
      "status": "Status is not one of available options."
    }
  }
}
```

---

## Additional Resources

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [Authentication Documentation](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/)
- [Working with Post Meta](https://developer.wordpress.org/rest-api/extending-the-rest-api/modifying-responses/)
- [Pagination Guide](https://developer.wordpress.org/rest-api/using-the-rest-api/pagination/)

---

*Documentation generated from the official WordPress REST API Reference*
