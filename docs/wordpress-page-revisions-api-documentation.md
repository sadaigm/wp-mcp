# WordPress REST API: Page Revisions Endpoint Documentation

This documentation covers the WordPress REST API Page Revisions endpoints, which allow you to manage revision history for WordPress pages.

## Table of Contents

- [Authentication](#authentication)
- [Revision Schema](#revision-schema)
- [List Page Revisions](#list-page-revisions)
- [Retrieve a Page Revision](#retrieve-a-page-revision)
- [Delete a Page Revision](#delete-a-page-revision)
- [Autosaves](#autosaves)
- [Common Use Cases](#common-use-cases)

---

## Authentication

For read operations (GET requests), authentication is typically not required for public revisions. However, write operations require authentication.

### Authentication Methods

1. **Cookie Authentication**: Use when making requests from the WordPress admin area
2. **OAuth2 Authentication**: Use for third-party applications
3. **Basic Authentication**: Use with Application Passwords for simple cases
4. **JWT Authentication**: Use JSON Web Tokens for stateless authentication

### Example: Basic Authentication with Application Password

```bash
curl -u username:application_password https://example.com/wp-json/wp/v2/pages/<parent>/revisions
```

---

## Revision Schema

The schema defines all fields available in a page revision record:

| Field | Type | Context | Description |
|-------|------|---------|-------------|
| `author` | integer | view, edit, embed | ID of the revision author |
| `date` | string | view, edit, embed | Date revision was created (site timezone) |
| `date_gmt` | string | view, edit | Date revision was created (GMT) |
| `guid` | object | view, edit | Globally unique identifier (read-only) |
| `id` | integer | view, edit, embed | Unique identifier for the revision |
| `modified` | string | view, edit | Date last modified (site timezone) |
| `modified_gmt` | string | view, edit | Date last modified (GMT) |
| `parent` | integer | view, edit, embed | Parent page ID |
| `slug` | string | view, edit, embed | URL slug |
| `title` | object | view, edit, embed | Revision title |
| `content` | object | view, edit | Revision content |
| `excerpt` | object | view, edit, embed | Revision excerpt |

---

## List Page Revisions

Retrieve all revisions for a specific page.

### Endpoint

```
GET /wp/v2/pages/<parent>/revisions
```

### Example Request

```bash
# Get all revisions for page ID 5
curl https://example.com/wp-json/wp/v2/pages/5/revisions

# With pagination
curl "https://example.com/wp-json/wp/v2/pages/5/revisions?per_page=10&page=1"
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `parent` | integer | - | Parent page ID (required in URL) |
| `context` | string | `view` | `view`, `embed`, `edit` |
| `page` | integer | `1` | Current page of the collection |
| `per_page` | integer | `10` | Maximum items per page |
| `search` | string | - | Limit results to matching string |
| `exclude` | array | - | Exclude specific revision IDs |
| `include` | array | - | Include only specific revision IDs |
| `offset` | integer | - | Offset result set |
| `order` | string | `desc` | `asc` or `desc` |
| `orderby` | string | `date` | `date`, `id`, `include`, `relevance`, `slug`, `title` |

### Example Response

```json
[
  {
    "author": 1,
    "date": "2024-01-20T14:30:00",
    "date_gmt": "2024-01-20T19:30:00",
    "id": 157,
    "modified": "2024-01-20T14:30:00",
    "modified_gmt": "2024-01-20T19:30:00",
    "parent": 5,
    "slug": "about-us",
    "title": {
      "rendered": "About Us - Updated",
      "raw": "About Us - Updated"
    },
    "content": {
      "rendered": "<p>Updated content about our company...</p>",
      "raw": "Updated content about our company..."
    },
    "excerpt": {
      "rendered": "<p>Updated content about our company...</p>",
      "raw": "Updated content about our company..."
    }
  },
  {
    "author": 1,
    "date": "2024-01-15T10:00:00",
    "date_gmt": "2024-01-15T15:00:00",
    "id": 142,
    "modified": "2024-01-15T10:00:00",
    "modified_gmt": "2024-01-15T15:00:00",
    "parent": 5,
    "slug": "about-us",
    "title": {
      "rendered": "About Us",
      "raw": "About Us"
    },
    "content": {
      "rendered": "<p>Original content about our company...</p>",
      "raw": "Original content about our company..."
    },
    "excerpt": {
      "rendered": "<p>Original content about our company...</p>",
      "raw": "Original content about our company..."
    }
  }
]
```

---

## Retrieve a Page Revision

Retrieve a specific page revision by its ID.

### Endpoint

```
GET /wp/v2/pages/<parent>/revisions/<id>
```

### Example Request

```bash
# Get revision ID 157 of page 5
curl https://example.com/wp-json/wp/v2/pages/5/revisions/157
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `parent` | integer | Yes | Parent page ID |
| `id` | integer | Yes | Revision ID |
| `context` | string | No | `view`, `embed`, `edit` (default: `view`) |

### Example Response

```json
{
  "author": 1,
  "date": "2024-01-20T14:30:00",
  "date_gmt": "2024-01-20T19:30:00",
  "guid": {
    "rendered": "https://example.com/?p=157"
  },
  "id": 157,
  "modified": "2024-01-20T14:30:00",
  "modified_gmt": "2024-01-20T19:30:00",
  "parent": 5,
  "slug": "about-us",
  "title": {
    "rendered": "About Us - Updated",
    "raw": "About Us - Updated"
  },
  "content": {
    "rendered": "<p>Updated content about our company...</p>",
    "raw": "Updated content about our company..."
  },
  "excerpt": {
    "rendered": "<p>Updated content about our company...</p>",
    "raw": "Updated content about our company..."
  }
}
```

---

## Delete a Page Revision

Permanently delete a page revision. Requires authentication.

### Endpoint

```
DELETE /wp/v2/pages/<parent>/revisions/<id>
```

### Example Request

```bash
curl -X DELETE https://example.com/wp-json/wp/v2/pages/5/revisions/142 \
  -u username:application_password
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `parent` | integer | Yes | Parent page ID |
| `id` | integer | Yes | Revision ID |
| `force` | boolean | Yes | Must be `true` (revisions don't support trash) |

### Example Response

```json
{
  "deleted": true,
  "previous": {
    "author": 1,
    "date": "2024-01-15T10:00:00",
    "date_gmt": "2024-01-15T15:00:00",
    "id": 142,
    "parent": 5,
    "title": {
      "rendered": "About Us"
    }
  }
}
```

---

## Autosaves

Autosaves are automatic revisions created by WordPress when editing content. They allow users to recover work in case of browser crashes or lost connections.

### List Page Autosaves

Retrieve autosaves for a specific page.

```
GET /wp/v2/pages/<id>/autosaves
```

```bash
curl https://example.com/wp-json/wp/v2/pages/5/autosaves
```

### Retrieve a Page Autosave

Retrieve a specific autosave revision.

```
GET /wp/v2/pages/<parent>/autosaves/<id>
```

```bash
curl https://example.com/wp-json/wp/v2/pages/5/autosaves/158
```

### Create a Page Autosave

Create an autosave for a page. Requires authentication.

```
POST /wp/v2/pages/<id>/autosaves
```

```bash
curl -X POST https://example.com/wp-json/wp/v2/pages/5/autosaves \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "title": "Autosave draft",
    "content": "Work in progress content...",
    "excerpt": "Draft excerpt"
  }'
```

### Request Parameters for Autosaves

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date` | string | No | Publication date |
| `date_gmt` | string | No | Publication date as GMT |
| `slug` | string | No | URL slug |
| `status` | string | No | `publish`, `future`, `draft`, `pending`, `private` |
| `password` | string | No | Page password |
| `title` | string/object | No | Page title |
| `content` | string/object | No | Page content |
| `author` | integer | No | Author ID |
| `excerpt` | string/object | No | Page excerpt |
| `featured_media` | integer | No | Featured media ID |
| `comment_status` | string | No | `open` or `closed` |
| `ping_status` | string | No | `open` or `closed` |
| `menu_order` | integer | No | Order in navigation |
| `meta` | object | No | Meta fields |
| `template` | string | No | Template file name |

---

## Common Use Cases

### Compare Page Revisions

```bash
# Get two revisions to compare
curl https://example.com/wp-json/wp/v2/pages/5/revisions/157
curl https://example.com/wp-json/wp/v2/pages/5/revisions/142

# Compare the content fields programmatically
```

### Restore a Page Revision

To restore a revision, you need to update the parent page with the revision's content:

```bash
# 1. Get the revision
REVISION=$(curl https://example.com/wp-json/wp/v2/pages/5/revisions/157)

# 2. Extract title and content (using jq)
TITLE=$(echo $REVISION | jq -r '.title.raw')
CONTENT=$(echo $REVISION | jq -r '.content.raw')

# 3. Update the parent page
curl -X POST https://example.com/wp-json/wp/v2/pages/5 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{
    \"title\": \"$TITLE\",
    \"content\": \"$CONTENT\"
  }"
```

### List All Revisions with Author Information

```bash
# Get revisions and embed author information
curl "https://example.com/wp-json/wp/v2/pages/5/revisions?context=edit"
```

### Clean Up Old Revisions

```bash
# Get all revisions, then delete old ones
curl "https://example.com/wp-json/wp/v2/pages/5/revisions?per_page=100" | \
  jq -r '.[].id' | \
  while read rev_id; do
    curl -X DELETE "https://example.com/wp-json/wp/v2/pages/5/revisions/$rev_id?force=true" \
      -u username:application_password
  done
```

### Get Revision Count for a Page

```bash
curl "https://example.com/wp-json/wp/v2/pages/5/revisions?per_page=100" | \
  jq 'length'
```

### Get Latest Revision

```bash
curl "https://example.com/wp-json/wp/v2/pages/5/revisions?per_page=1&order=desc&orderby=date"
```

### Filter Revisions by Author

```bash
# Get all revisions, then filter by author ID
curl "https://example.com/wp-json/wp/v2/pages/5/revisions" | \
  jq '.[] | select(.author == 1)'
```

### Get Revisions Modified After Date

```bash
curl "https://example.com/wp-json/wp/v2/pages/5/revisions?after=2024-01-01T00:00:00"
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
  "code": "rest_post_invalid_parent",
  "message": "Invalid parent page ID.",
  "data": {
    "status": 404
  }
}
```

### 400 Bad Request

```json
{
  "code": "rest_invalid_param",
  "message": "Invalid parameter(s): force",
  "data": {
    "status": 400,
    "params": {
      "force": "The force parameter must be true."
    }
  }
}
```

---

## Best Practices

1. **Don't Store Revisions Permanently**: Revisions are meant for temporary history tracking
2. **Limit Revision Storage**: Use WordPress filters or plugins to limit the number of revisions stored
3. **Use Autosaves for Drafts**: Autosaves are specifically designed for in-progress work
4. **Compare Before Restoring**: Always review revision content before restoring
5. **Clean Up Periodically**: Remove old revisions to maintain database performance

---

## Related Endpoints

- [Pages API Documentation](./wordpress-pages-api-documentation.md)
- [Post Revisions API Documentation](./wordpress-post-revisions-api-documentation.md)
- [Posts API Documentation](./wordpress-posts-api-documentation.md)

---

*Documentation generated from the official WordPress REST API Reference*
