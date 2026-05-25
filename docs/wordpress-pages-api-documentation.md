# WordPress REST API: Pages Endpoint Documentation

This documentation covers the WordPress REST API Pages endpoint (`/wp/v2/pages`), which allows you to programmatically retrieve, create, update, and delete WordPress pages.

## Table of Contents

- [Authentication](#authentication)
- [Page Schema](#page-schema)
- [List Pages](#list-pages)
- [Retrieve a Single Page](#retrieve-a-single-page)
- [Create a Page](#create-a-page)
- [Update a Page](#update-a-page)
- [Delete a Page](#delete-a-page)

---

## Authentication

For read operations (GET requests), authentication is typically not required for public pages. However, for write operations (POST, PUT, DELETE), you must authenticate.

### Authentication Methods

1. **Cookie Authentication**: Use when making requests from the WordPress admin area
2. **OAuth2 Authentication**: Use for third-party applications
3. **Basic Authentication**: Use with Application Passwords for simple cases
4. **JWT Authentication**: Use JSON Web Tokens for stateless authentication

### Example: Basic Authentication with Application Password

```bash
curl -u username:application_password https://example.com/wp-json/wp/v2/pages
```

### Example: Bearer Token Header

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://example.com/wp-json/wp/v2/pages
```

---

## Page Schema

The schema defines all fields available in a page record:

| Field | Type | Context | Description |
|-------|------|---------|-------------|
| `id` | integer | view, edit, embed | Unique identifier for the page (read-only) |
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
| `parent` | integer | view, edit | Parent page ID for hierarchical structure |
| `title` | object | view, edit, embed | Page title |
| `content` | object | view, edit | Page content |
| `author` | integer | view, edit, embed | Author ID |
| `excerpt` | object | view, edit, embed | Page excerpt |
| `featured_media` | integer | view, edit, embed | Featured media ID |
| `comment_status` | string | view, edit | One of: `open`, `closed` |
| `ping_status` | string | view, edit | One of: `open`, `closed` |
| `menu_order` | integer | view, edit | Order in relation to other pages |
| `meta` | object | view, edit | Meta fields |
| `template` | string | view, edit | Theme file to use |

### Key Differences from Posts

- **Hierarchical Structure**: Pages support parent-child relationships via the `parent` field
- **Menu Ordering**: Pages have `menu_order` for custom ordering in navigation
- **No Taxonomies**: Pages don't have categories or tags
- **No Formats**: Pages don't support post formats
- **No Sticky**: Pages cannot be marked as sticky

---

## List Pages

Retrieve a collection of pages with optional filtering and pagination.

### Endpoint

```
GET /wp/v2/pages
```

### Example Request

```bash
# Basic request
curl https://example.com/wp-json/wp/v2/pages

# With query parameters
curl "https://example.com/wp-json/wp/v2/pages?per_page=5&page=1"
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `context` | string | `view` | Scope of request: `view`, `embed`, `edit` |
| `page` | integer | `1` | Current page of the collection |
| `per_page` | integer | `10` | Maximum items per page (max 100) |
| `search` | string | - | Limit results to matching string |
| `after` | string | - | ISO8601 compliant date - pages published after |
| `before` | string | - | ISO8601 compliant date - pages published before |
| `author` | array | - | Limit to specific author IDs |
| `author_exclude` | array | - | Exclude specific author IDs |
| `exclude` | array | - | Exclude specific IDs |
| `include` | array | - | Limit to specific IDs |
| `menu_order` | integer | - | Limit to specific menu_order value |
| `offset` | integer | - | Offset result set by number |
| `order` | string | `desc` | `asc` or `desc` |
| `orderby` | string | `date` | `author`, `date`, `id`, `include`, `modified`, `parent`, `relevance`, `slug`, `title`, `menu_order` |
| `parent` | array | - | Limit to specific parent IDs |
| `parent_exclude` | array | - | Exclude specific parent IDs |
| `search_columns` | array | - | Column names to search |
| `slug` | array | - | Limit to specific slugs |
| `status` | string | `publish` | One or more statuses |

### Example Response

```json
[
  {
    "id": 2,
    "date": "2024-01-15T10:00:00",
    "date_gmt": "2024-01-15T15:00:00",
    "guid": {
      "rendered": "https://example.com/?page_id=2"
    },
    "modified": "2024-01-15T10:00:00",
    "modified_gmt": "2024-01-15T15:00:00",
    "slug": "about-us",
    "status": "publish",
    "type": "page",
    "link": "https://example.com/about-us/",
    "title": {
      "rendered": "About Us"
    },
    "content": {
      "rendered": "<p>This is the About Us page content...</p>",
      "protected": false
    },
    "excerpt": {
      "rendered": "<p>This is the About Us page content...</p>",
      "protected": false
    },
    "author": 1,
    "featured_media": 0,
    "parent": 0,
    "menu_order": 0,
    "comment_status": "closed",
    "ping_status": "closed",
    "template": "",
    "meta": [],
    "_links": {
      "self": [{"href": "https://example.com/wp-json/wp/v2/pages/2"}],
      "collection": [{"href": "https://example.com/wp-json/wp/v2/pages"}]
    }
  }
]
```

---

## Retrieve a Single Page

Retrieve a specific page by its ID.

### Endpoint

```
GET /wp/v2/pages/<id>
```

### Example Request

```bash
curl https://example.com/wp-json/wp/v2/pages/2
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Unique identifier for the page |
| `context` | string | No | `view`, `embed`, `edit` (default: `view`) |
| `password` | string | No | Password if page is protected |

### Example Response

```json
{
  "id": 2,
  "date": "2024-01-15T10:00:00",
  "date_gmt": "2024-01-15T15:00:00",
  "guid": {
    "rendered": "https://example.com/?page_id=2"
  },
  "link": "https://example.com/about-us/",
  "modified": "2024-01-15T10:00:00",
  "modified_gmt": "2024-01-15T15:00:00",
  "slug": "about-us",
  "status": "publish",
  "type": "page",
  "title": {
    "rendered": "About Us"
  },
  "content": {
    "rendered": "<div class=\"wp-block-group\"><h2>Welcome to our company</h2><p>This is the About Us page content...</p></div>",
    "protected": false
  },
  "excerpt": {
    "rendered": "<p>This is the About Us page content...</p>",
    "protected": false
  },
  "author": 1,
  "featured_media": 0,
  "parent": 0,
  "menu_order": 0,
  "comment_status": "closed",
  "ping_status": "closed",
  "template": "",
  "meta": [],
  "_links": {
    "self": [{"href": "https://example.com/wp-json/wp/v2/pages/2"}],
    "collection": [{"href": "https://example.com/wp-json/wp/v2/pages"}],
    "author": [{"embeddable": true, "href": "https://example.com/wp-json/wp/v2/users/1"}],
    "up": [{"embeddable": true, "href": "https://example.com/wp-json/wp/v2/pages/0"}]
  }
}
```

---

## Create a Page

Create a new page. Requires authentication.

### Endpoint

```
POST /wp/v2/pages
```

### Example Request

```bash
curl -X POST https://example.com/wp-json/wp/v2/pages \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "title": "Contact Us",
    "content": "Contact us at info@example.com or call +1-555-0123.",
    "status": "draft",
    "parent": 0,
    "menu_order": 10,
    "author": 1
  }'
```

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | string/object | Yes | Page title |
| `content` | string/object | No | Page content |
| `excerpt` | string/object | No | Page excerpt |
| `status` | string | No | `publish`, `future`, `draft`, `pending`, `private` |
| `parent` | integer | No | Parent page ID (0 for top-level) |
| `menu_order` | integer | No | Order in navigation |
| `author` | integer | No | Author ID |
| `featured_media` | integer | No | Featured media ID |
| `comment_status` | string | No | `open` or `closed` |
| `ping_status` | string | No | `open` or `closed` |
| `template` | string | No | Template file name |
| `date` | string | No | Publication date |
| `date_gmt` | string | No | Publication date as GMT |
| `slug` | string | No | URL slug |
| `password` | string | No | Page password |
| `meta` | object | No | Meta fields |

### Creating Child Pages

```bash
curl -X POST https://example.com/wp-json/wp/v2/pages \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "title": "Our Team",
    "content": "Meet our dedicated team members...",
    "parent": 2,
    "menu_order": 1
  }'
```

### Example Response

```json
{
  "id": 15,
  "date": "2024-01-20T14:30:00",
  "date_gmt": "2024-01-20T19:30:00",
  "guid": {
    "rendered": "https://example.com/?page_id=15"
  },
  "modified": "2024-01-20T14:30:00",
  "modified_gmt": "2024-01-20T19:30:00",
  "slug": "contact-us",
  "status": "draft",
  "type": "page",
  "link": "https://example.com/?page_id=15",
  "title": {
    "rendered": "Contact Us",
    "raw": "Contact Us"
  },
  "content": {
    "rendered": "<p>Contact us at info@example.com or call +1-555-0123.</p>",
    "raw": "Contact us at info@example.com or call +1-555-0123."
  },
  "excerpt": {
    "rendered": "<p>Contact us at info@example.com or call +1-555-0123.</p>",
    "raw": "Contact us at info@example.com or call +1-555-0123."
  },
  "author": 1,
  "featured_media": 0,
  "parent": 0,
  "menu_order": 10,
  "comment_status": "closed",
  "ping_status": "closed",
  "template": "",
  "meta": [],
  "_links": {
    "self": [{"href": "https://example.com/wp-json/wp/v2/pages/15"}],
    "collection": [{"href": "https://example.com/wp-json/wp/v2/pages"}]
  }
}
```

---

## Update a Page

Update an existing page. Requires authentication.

### Endpoint

```
POST /wp/v2/pages/<id>
```

### Example Request

```bash
curl -X POST https://example.com/wp-json/wp/v2/pages/15 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "title": "Contact Information",
    "content": "Get in touch with us through various channels...",
    "status": "publish"
  }'
```

### Parameters

All parameters from [Create a Page](#create-a-page) are supported. Only include the fields you want to update.

### Updating Page Hierarchy

```bash
# Move a page to become a child of another page
curl -X POST https://example.com/wp-json/wp/v2/pages/15 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "parent": 2
  }'
```

### Example Response

```json
{
  "id": 15,
  "date": "2024-01-20T14:30:00",
  "date_gmt": "2024-01-20T19:30:00",
  "guid": {
    "rendered": "https://example.com/?page_id=15"
  },
  "modified": "2024-01-20T15:45:00",
  "modified_gmt": "2024-01-20T20:45:00",
  "slug": "contact-information",
  "status": "publish",
  "type": "page",
  "link": "https://example.com/contact-information/",
  "title": {
    "rendered": "Contact Information",
    "raw": "Contact Information"
  },
  "content": {
    "rendered": "<p>Get in touch with us through various channels...</p>",
    "raw": "Get in touch with us through various channels..."
  },
  "excerpt": {
    "rendered": "<p>Get in touch with us through various channels...</p>",
    "raw": "Get in touch with us through various channels..."
  },
  "author": 1,
  "featured_media": 0,
  "parent": 0,
  "menu_order": 10,
  "comment_status": "closed",
  "ping_status": "closed",
  "template": "",
  "meta": []
}
```

---

## Delete a Page

Delete an existing page. Requires authentication.

### Endpoint

```
DELETE /wp/v2/pages/<id>
```

### Example Request

```bash
# Move to trash (default)
curl -X DELETE https://example.com/wp-json/wp/v2/pages/15 \
  -u username:application_password

# Force delete permanently
curl -X DELETE "https://example.com/wp-json/wp/v2/pages/15?force=true" \
  -u username:application_password
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | integer | - | Page ID |
| `force` | boolean | `false` | Bypass trash and force deletion |

### Example Response

```json
{
  "id": 15,
  "deleted": true,
  "previous": {
    "id": 15,
    "title": {
      "rendered": "Contact Information"
    },
    "status": "publish",
    "type": "page"
  }
}
```

---

## Common Use Cases

### Filter Pages by Parent

```bash
# Get all top-level pages (no parent)
curl "https://example.com/wp-json/wp/v2/pages?parent=0"

# Get all child pages of a specific parent
curl "https://example.com/wp-json/wp/v2/pages?parent=2"
```

### Sort Pages by Menu Order

```bash
curl "https://example.com/wp-json/wp/v2/pages?orderby=menu_order&order=asc"
```

### Search Pages

```bash
curl "https://example.com/wp-json/wp/v2/pages?search=contact"
```

### Pagination

```bash
curl "https://example.com/wp-json/wp/v2/pages?per_page=20&page=2"
```

### Retrieve Pages Modified After Date

```bash
curl "https://example.com/wp-json/wp/v2/pages?modified_after=2024-01-01T00:00:00"
```

### Get Pages with Specific Menu Order

```bash
curl "https://example.com/wp-json/wp/v2/pages?menu_order=5"
```

### Exclude Child Pages

```bash
# Get only top-level pages, exclude all child pages
curl "https://example.com/wp-json/wp/v2/pages?parent_exclude[]=1&parent_exclude[]=2&parent_exclude[]=3"
```

---

## Page Hierarchies

Pages in WordPress support hierarchical structures, allowing you to create parent-child relationships.

### Building a Page Tree

```bash
# 1. Create parent page
PARENT_RESPONSE=$(curl -X POST https://example.com/wp-json/wp/v2/pages \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{"title": "Services", "content": "Our services overview..."}')

PARENT_ID=$(echo $PARENT_RESPONSE | jq -r '.id')

# 2. Create child pages
curl -X POST https://example.com/wp-json/wp/v2/pages \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{\"title\": 'Web Development', \"parent\": $PARENT_ID, \"menu_order\": 1}"

curl -X POST https://example.com/wp-json/wp/v2/pages \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{\"title\": 'Mobile Apps', \"parent\": $PARENT_ID, \"menu_order\": 2}"

curl -X POST https://example.com/wp-json/wp/v2/pages \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{\"title\": 'Consulting', \"parent\": $PARENT_ID, \"menu_order\": 3}"
```

### Retrieving a Page Hierarchy

```bash
# Get all pages, then process client-side to build tree
curl "https://example.com/wp-json/wp/v2/pages?per_page=100" | \
  jq '[.[] | {id, title: .title.rendered, parent, link}] | group_by(.parent)'
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
  "message": "Invalid page ID.",
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

### 403 Forbidden (Parent Loop)

```json
{
  "code": "rest_post_invalid_parent",
  "message": "Invalid parent page ID.",
  "data": {
    "status": 403
  }
}
```

---

## Pages vs Posts: Key Differences

| Feature | Pages | Posts |
|---------|-------|-------|
| Hierarchical | Yes (parent-child) | No (flat structure) |
| Categories/Tags | No | Yes |
| Menu Order | Yes | No |
| Post Formats | No | Yes |
| Sticky Posts | No | Yes |
| Timestamps | Less important | Chronological by default |
| Typical Use | Static content | Blog articles |

---

## Additional Resources

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [Authentication Documentation](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/)
- [Working with Page Meta](https://developer.wordpress.org/rest-api/extending-the-rest-api/modifying-responses/)
- [Pagination Guide](https://developer.wordpress.org/rest-api/using-the-rest-api/pagination/)
- [Posts Endpoint Documentation](./wordpress-posts-api-documentation.md)

---

*Documentation generated from the official WordPress REST API Reference*
