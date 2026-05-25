# WordPress REST API: Post Revisions Endpoint Documentation

This documentation covers the WordPress REST API Post Revisions endpoints, which allow you to manage revision history for WordPress posts.

## Table of Contents

- [Authentication](#authentication)
- [Revision Schema](#revision-schema)
- [List Post Revisions](#list-post-revisions)
- [Retrieve a Post Revision](#retrieve-a-post-revision)
- [Delete a Post Revision](#delete-a-post-revision)
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
curl -u username:application_password https://example.com/wp-json/wp/v2/posts/<parent>/revisions
```

---

## Revision Schema

The schema defines all fields available in a post revision record:

| Field | Type | Context | Description |
|-------|------|---------|-------------|
| `author` | integer | view, edit, embed | ID of the revision author |
| `date` | string | view, edit, embed | Date revision was created (site timezone) |
| `date_gmt` | string | view, edit | Date revision was created (GMT) |
| `guid` | object | view, edit | Globally unique identifier (read-only) |
| `id` | integer | view, edit, embed | Unique identifier for the revision |
| `modified` | string | view, edit | Date last modified (site timezone) |
| `modified_gmt` | string | view, edit | Date last modified (GMT) |
| `parent` | integer | view, edit, embed | Parent post ID |
| `slug` | string | view, edit, embed | URL slug |
| `title` | object | view, edit, embed | Revision title |
| `content` | object | view, edit | Revision content |
| `excerpt` | object | view, edit, embed | Revision excerpt |

---

## List Post Revisions

Retrieve all revisions for a specific post.

### Endpoint

```
GET /wp/v2/posts/<parent>/revisions
```

### Example Request

```bash
# Get all revisions for post ID 42
curl https://example.com/wp-json/wp/v2/posts/42/revisions

# With pagination
curl "https://example.com/wp-json/wp/v2/posts/42/revisions?per_page=10&page=1"
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `parent` | integer | - | Parent post ID (required in URL) |
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
    "id": 312,
    "modified": "2024-01-20T14:30:00",
    "modified_gmt": "2024-01-20T19:30:00",
    "parent": 42,
    "slug": "my-blog-post",
    "title": {
      "rendered": "My Updated Blog Post",
      "raw": "My Updated Blog Post"
    },
    "content": {
      "rendered": "<p>Updated blog content with new information...</p>",
      "raw": "Updated blog content with new information..."
    },
    "excerpt": {
      "rendered": "<p>Updated blog content with new information...</p>",
      "raw": "Updated blog content with new information..."
    }
  },
  {
    "author": 1,
    "date": "2024-01-15T10:00:00",
    "date_gmt": "2024-01-15T15:00:00",
    "id": 298,
    "modified": "2024-01-15T10:00:00",
    "modified_gmt": "2024-01-15T15:00:00",
    "parent": 42,
    "slug": "my-blog-post",
    "title": {
      "rendered": "My Blog Post",
      "raw": "My Blog Post"
    },
    "content": {
      "rendered": "<p>Original blog content...</p>",
      "raw": "Original blog content..."
    },
    "excerpt": {
      "rendered": "<p>Original blog content...</p>",
      "raw": "Original blog content..."
    }
  }
]
```

---

## Retrieve a Post Revision

Retrieve a specific post revision by its ID.

### Endpoint

```
GET /wp/v2/posts/<parent>/revisions/<id>
```

### Example Request

```bash
# Get revision ID 312 of post 42
curl https://example.com/wp-json/wp/v2/posts/42/revisions/312
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `parent` | integer | Yes | Parent post ID |
| `id` | integer | Yes | Revision ID |
| `context` | string | No | `view`, `embed`, `edit` (default: `view`) |

### Example Response

```json
{
  "author": 1,
  "date": "2024-01-20T14:30:00",
  "date_gmt": "2024-01-20T19:30:00",
  "guid": {
    "rendered": "https://example.com/?p=312"
  },
  "id": 312,
  "modified": "2024-01-20T14:30:00",
  "modified_gmt": "2024-01-20T19:30:00",
  "parent": 42,
  "slug": "my-blog-post",
  "title": {
    "rendered": "My Updated Blog Post",
    "raw": "My Updated Blog Post"
  },
  "content": {
    "rendered": "<p>Updated blog content with new information...</p>",
    "raw": "Updated blog content with new information..."
  },
  "excerpt": {
    "rendered": "<p>Updated blog content with new information...</p>",
    "raw": "Updated blog content with new information..."
  }
}
```

---

## Delete a Post Revision

Permanently delete a post revision. Requires authentication.

### Endpoint

```
DELETE /wp/v2/posts/<parent>/revisions/<id>
```

### Example Request

```bash
curl -X DELETE https://example.com/wp-json/wp/v2/posts/42/revisions/298 \
  -u username:application_password
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `parent` | integer | Yes | Parent post ID |
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
    "id": 298,
    "parent": 42,
    "title": {
      "rendered": "My Blog Post"
    }
  }
}
```

---

## Autosaves

Autosaves are automatic revisions created by WordPress when editing content. They allow users to recover work in case of browser crashes or lost connections.

### List Post Autosaves

Retrieve autosaves for a specific post.

```
GET /wp/v2/posts/<id>/autosaves
```

```bash
curl https://example.com/wp-json/wp/v2/posts/42/autosaves
```

### Retrieve a Post Autosave

Retrieve a specific autosave revision.

```
GET /wp/v2/posts/<parent>/autosaves/<id>
```

```bash
curl https://example.com/wp-json/wp/v2/posts/42/autosaves/313
```

### Create a Post Autosave

Create an autosave for a post. Requires authentication.

```
POST /wp/v2/posts/<id>/autosaves
```

```bash
curl -X POST https://example.com/wp-json/wp/v2/posts/42/autosaves \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "title": "Autosave draft",
    "content": "Work in progress blog post...",
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
| `password` | string | No | Post password |
| `title` | string/object | No | Post title |
| `content` | string/object | No | Post content |
| `author` | integer | No | Author ID |
| `excerpt` | string/object | No | Post excerpt |
| `featured_media` | integer | No | Featured media ID |
| `comment_status` | string | No | `open` or `closed` |
| `ping_status` | string | No | `open` or `closed` |
| `format` | string | No | Post format: `standard`, `aside`, `chat`, `gallery`, `link`, `image`, `quote`, `status`, `video`, `audio` |
| `meta` | object | No | Meta fields |
| `sticky` | boolean | No | Whether post should be sticky |
| `template` | string | No | Template file name |
| `categories` | array | No | Category IDs |
| `tags` | array | No | Tag IDs |

---

## Common Use Cases

### Compare Post Revisions

```bash
# Get two revisions to compare
curl https://example.com/wp-json/wp/v2/posts/42/revisions/312
curl https://example.com/wp-json/wp/v2/posts/42/revisions/298

# Compare the content fields programmatically
```

### Restore a Post Revision

To restore a revision, you need to update the parent post with the revision's content:

```bash
# 1. Get the revision
REVISION=$(curl https://example.com/wp-json/wp/v2/posts/42/revisions/312)

# 2. Extract title and content (using jq)
TITLE=$(echo $REVISION | jq -r '.title.raw')
CONTENT=$(echo $REVISION | jq -r '.content.raw')

# 3. Update the parent post
curl -X POST https://example.com/wp-json/wp/v2/posts/42 \
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
curl "https://example.com/wp-json/wp/v2/posts/42/revisions?context=edit"
```

### Clean Up Old Revisions

```bash
# Get all revisions, then delete old ones
curl "https://example.com/wp-json/wp/v2/posts/42/revisions?per_page=100" | \
  jq -r '.[].id' | \
  while read rev_id; do
    curl -X DELETE "https://example.com/wp-json/wp/v2/posts/42/revisions/$rev_id?force=true" \
      -u username:application_password
  done
```

### Get Revision Count for a Post

```bash
curl "https://example.com/wp-json/wp/v2/posts/42/revisions?per_page=100" | \
  jq 'length'
```

### Get Latest Revision

```bash
curl "https://example.com/wp-json/wp/v2/posts/42/revisions?per_page=1&order=desc&orderby=date"
```

### Filter Revisions by Author

```bash
# Get all revisions, then filter by author ID
curl "https://example.com/wp-json/wp/v2/posts/42/revisions" | \
  jq '.[] | select(.author == 1)'
```

### Get Revisions Modified After Date

```bash
curl "https://example.com/wp-json/wp/v2/posts/42/revisions?after=2024-01-01T00:00:00"
```

### Track Post Edit History

```bash
# Get all revisions sorted by date
curl "https://example.com/wp-json/wp/v2/posts/42/revisions?orderby=date&order=desc" | \
  jq '.[] | {date, author, title: .title.rendered}'
```

### Create Revision Diff Summary

```bash
# Get revisions and create a summary
curl "https://example.com/wp-json/wp/v2/posts/42/revisions" | \
  jq '.[] | {
    id,
    date,
    author,
    title: .title.rendered,
    excerpt: .excerpt.rendered[0:100]
  }'
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
  "message": "Invalid parent post ID.",
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

## Post vs Page Revisions

| Feature | Post Revisions | Page Revisions |
|---------|----------------|----------------|
| Endpoint Path | `/wp/v2/posts/<parent>/revisions` | `/wp/v2/pages/<parent>/revisions` |
| Supports Categories | Yes | No |
| Supports Tags | Yes | No |
| Post Formats | Yes | No |
| Sticky Posts | Yes | No |
| Menu Order | No | Yes |
| Parent Hierarchies | No | Yes |

---

## Best Practices

1. **Don't Store Revisions Permanently**: Revisions are meant for temporary history tracking
2. **Limit Revision Storage**: Use WordPress filters or plugins to limit the number of revisions stored
3. **Use Autosaves for Drafts**: Autosaves are specifically designed for in-progress work
4. **Compare Before Restoring**: Always review revision content before restoring
5. **Clean Up Periodically**: Remove old revisions to maintain database performance
6. **Track Multiple Authors**: Use revision history to track changes by different authors
7. **Implement Revision Limits**: Consider setting limits on revisions per post to optimize database size

---

## WordPress Configuration

### Limit Revisions in wp-config.php

```php
// Limit to 5 revisions per post
define( 'WP_POST_REVISIONS', 5 );

// Disable revisions entirely
define( 'WP_POST_REVISIONS', false );
```

### Revisions for Custom Post Types

When registering custom post types, enable revisions support:

```php
$args = array(
    'supports' => array( 'title', 'editor', 'revisions' ),
    // ... other arguments
);
register_post_type( 'my_custom_post_type', $args );
```

---

## Related Endpoints

- [Posts API Documentation](./wordpress-posts-api-documentation.md)
- [Page Revisions API Documentation](./wordpress-page-revisions-api-documentation.md)
- [Pages API Documentation](./wordpress-pages-api-documentation.md)

---

*Documentation generated from the official WordPress REST API Reference*
