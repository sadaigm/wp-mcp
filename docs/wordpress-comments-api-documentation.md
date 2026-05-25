# WordPress REST API: Comments Endpoint Documentation

This documentation covers the WordPress REST API Comments endpoint (`/wp/v2/comments`), which allows you to programmatically manage WordPress comments.

## Table of Contents

- [Authentication](#authentication)
- [Comment Schema](#comment-schema)
- [List Comments](#list-comments)
- [Retrieve a Comment](#retrieve-a-comment)
- [Create a Comment](#create-a-comment)
- [Update a Comment](#update-a-comment)
- [Delete a Comment](#delete-a-comment)
- [Common Use Cases](#common-use-cases)

---

## Authentication

For read operations (GET requests), authentication is typically not required for approved comments on public posts. However, write operations and viewing unapproved comments require authentication.

### Authentication Methods

1. **Cookie Authentication**: Use when making requests from the WordPress admin area
2. **OAuth2 Authentication**: Use for third-party applications
3. **Basic Authentication**: Use with Application Passwords for simple cases
4. **JWT Authentication**: Use JSON Web Tokens for stateless authentication

### Example: Basic Authentication with Application Password

```bash
curl -u username:application_password https://example.com/wp-json/wp/v2/comments
```

---

## Comment Schema

The schema defines all fields available in a comment record:

| Field | Type | Context | Description |
|-------|------|---------|-------------|
| `id` | integer | view, edit, embed | Unique identifier (read-only) |
| `author` | integer | view, edit, embed | User ID if author is registered user |
| `author_email` | string | edit | Email address for comment author |
| `author_ip` | string | edit | IP address for comment author |
| `author_name` | string | view, edit, embed | Display name for comment author |
| `author_url` | string | view, edit, embed | URL for comment author |
| `author_user_agent` | string | edit | User agent for comment author |
| `content` | object | view, edit, embed | Comment content |
| `date` | string | view, edit, embed | Date published (site timezone) |
| `date_gmt` | string | view, edit | Date published (GMT) |
| `link` | string | view, edit, embed | URL to the comment (read-only) |
| `parent` | integer | view, edit, embed | Parent comment ID (for threaded comments) |
| `post` | integer | view, edit | Associated post ID |
| `status` | string | view, edit | Comment status |
| `type` | string | view, edit, embed | Comment type (read-only) |
| `author_avatar_urls` | object | view, edit, embed | Avatar URLs for comment author (read-only) |
| `meta` | object | view, edit | Meta fields |

### Comment Status Values

| Status | Description |
|--------|-------------|
| `approve` | Approved comment |
| `hold` | Unapproved/pending comment |
| `spam` | Spam comment |
| `trash` | Trashed comment |

---

## List Comments

Retrieve a collection of comments with optional filtering and pagination.

### Endpoint

```
GET /wp/v2/comments
```

### Example Request

```bash
# Basic request
curl https://example.com/wp-json/wp/v2/comments

# With query parameters
curl "https://example.com/wp-json/wp/v2/comments?per_page=20&post=42"
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `context` | string | `view` | Scope of request: `view`, `embed`, `edit` |
| `page` | integer | `1` | Current page of the collection |
| `per_page` | integer | `10` | Maximum items per page (max 100) |
| `search` | string | - | Limit results to matching string |
| `after` | string | - | ISO8601 date - comments published after |
| `before` | string | - | ISO8601 date - comments published before |
| `author` | array | - | Limit to specific user IDs (requires auth) |
| `author_exclude` | array | - | Exclude specific user IDs (requires auth) |
| `author_email` | string | - | Limit to specific author email (requires auth) |
| `exclude` | array | - | Exclude specific comment IDs |
| `include` | array | - | Include only specific comment IDs |
| `offset` | integer | - | Offset result set |
| `order` | string | `desc` | `asc` or `desc` |
| `orderby` | string | `date_gmt` | `date`, `date_gmt`, `id`, `include`, `post`, `parent`, `type` |
| `parent` | array | - | Limit to specific parent comment IDs |
| `parent_exclude` | array | - | Exclude specific parent comment IDs |
| `post` | integer | - | Limit to comments for specific post ID |
| `status` | string | `approve` | Comment status (requires auth for non-approved) |
| `type` | string | `comment` | Comment type (requires auth) |
| `password` | string | - | Password for protected parent post |

### Example Response

```json
[
  {
    "id": 156,
    "post": 42,
    "parent": 0,
    "author": 0,
    "author_name": "John Doe",
    "author_url": "https://example.com",
    "date": "2024-01-20T14:30:00",
    "date_gmt": "2024-01-20T19:30:00",
    "content": {
      "rendered": "<p>Great article! Very informative.</p>",
      "raw": "Great article! Very informative."
    },
    "link": "https://example.com/post-title/#comment-156",
    "status": "approved",
    "type": "comment",
    "author_avatar_urls": {
      "24": "https://secure.gravatar.com/avatar/...",
      "48": "https://secure.gravatar.com/avatar/...",
      "96": "https://secure.gravatar.com/avatar/..."
    },
    "meta": [],
    "_links": {
      "self": [{"href": "https://example.com/wp-json/wp/v2/comments/156"}],
      "collection": [{"href": "https://example.com/wp-json/wp/v2/comments"}]
    }
  }
]
```

---

## Retrieve a Comment

Retrieve a specific comment by its ID.

### Endpoint

```
GET /wp/v2/comments/<id>
```

### Example Request

```bash
curl https://example.com/wp-json/wp/v2/comments/156
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Unique identifier for the comment |
| `context` | string | No | `view`, `embed`, `edit` (default: `view`) |
| `password` | string | No | Password for protected parent post |

### Example Response

```json
{
  "id": 156,
  "post": 42,
  "parent": 0,
  "author": 0,
  "author_name": "John Doe",
  "author_url": "https://example.com",
  "date": "2024-01-20T14:30:00",
  "date_gmt": "2024-01-20T19:30:00",
  "content": {
    "rendered": "<p>Great article! Very informative.</p>",
    "raw": "Great article! Very informative."
  },
  "link": "https://example.com/post-title/#comment-156",
  "status": "approved",
  "type": "comment",
  "author_avatar_urls": {
    "24": "https://secure.gravatar.com/avatar/...",
    "48": "https://secure.gravatar.com/avatar/...",
    "96": "https://secure.gravatar.com/avatar/..."
  },
  "meta": []
}
```

---

## Create a Comment

Create a new comment. Requires authentication for registered users, but guests can post if comments are open.

### Endpoint

```
POST /wp/v2/comments
```

### Example Request

```bash
# As a guest
curl -X POST https://example.com/wp-json/wp/v2/comments \
  -H "Content-Type: application/json" \
  -d '{
    "post": 42,
    "author_name": "Jane Smith",
    "author_email": "jane@example.com",
    "content": "Thanks for sharing this!",
    "parent": 0
  }'

# As authenticated user
curl -X POST https://example.com/wp-json/wp/v2/comments \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "post": 42,
    "content": "My comment as a registered user",
    "parent": 156
  }'
```

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `post` | integer | Yes | Associated post ID |
| `content` | string/object | Yes | Comment content |
| `author_name` | string | Conditional* | Display name for comment author |
| `author_email` | string | Conditional* | Email address for comment author |
| `author_url` | string | No | URL for comment author |
| `author` | integer | No | User ID if author is registered user |
| `author_ip` | string | No | IP address for comment author |
| `author_user_agent` | string | No | User agent for comment author |
| `date` | string | No | Publication date (site timezone) |
| `date_gmt` | string | No | Publication date (GMT) |
| `parent` | integer | No | Parent comment ID (0 for top-level) |
| `status` | string | No | Comment status |
| `meta` | object | No | Meta fields |

*Required for guest comments if not using cookie authentication

### Creating a Reply (Threaded Comments)

```bash
curl -X POST https://example.com/wp-json/wp/v2/comments \
  -H "Content-Type: application/json" \
  -d '{
    "post": 42,
    "parent": 156,
    "author_name": "Reply Author",
    "author_email": "reply@example.com",
    "content": "This is a reply to the previous comment."
  }'
```

### Example Response

```json
{
  "id": 157,
  "post": 42,
  "parent": 156,
  "author": 0,
  "author_name": "Jane Smith",
  "author_email": "jane@example.com",
  "author_url": "",
  "date": "2024-01-20T15:00:00",
  "date_gmt": "2024-01-20T20:00:00",
  "content": {
    "rendered": "<p>Thanks for sharing this!</p>",
    "raw": "Thanks for sharing this!"
  },
  "link": "https://example.com/post-title/#comment-157",
  "status": "hold",
  "type": "comment",
  "author_avatar_urls": {
    "24": "https://secure.gravatar.com/avatar/...",
    "48": "https://secure.gravatar.com/avatar/...",
    "96": "https://secure.gravatar.com/avatar/..."
  },
  "meta": []
}
```

---

## Update a Comment

Update an existing comment. Requires authentication.

### Endpoint

```
POST /wp/v2/comments/<id>
```

### Example Request

```bash
curl -X POST https://example.com/wp-json/wp/v2/comments/157 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "content": "Updated comment content",
    "status": "approve"
  }'
```

### Parameters

All parameters from [Create a Comment](#create-a-comment) are supported. Only include the fields you want to update.

### Approving a Comment

```bash
curl -X POST https://example.com/wp-json/wp/v2/comments/157 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "status": "approve"
  }'
```

### Marking as Spam

```bash
curl -X POST https://example.com/wp-json/wp/v2/comments/157 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "status": "spam"
  }'
```

### Example Response

```json
{
  "id": 157,
  "post": 42,
  "parent": 156,
  "author": 0,
  "author_name": "Jane Smith",
  "author_email": "jane@example.com",
  "date": "2024-01-20T15:00:00",
  "date_gmt": "2024-01-20T20:00:00",
  "content": {
    "rendered": "<p>Updated comment content</p>",
    "raw": "Updated comment content"
  },
  "link": "https://example.com/post-title/#comment-157",
  "status": "approve",
  "type": "comment",
  "author_avatar_urls": {
    "24": "https://secure.gravatar.com/avatar/...",
    "48": "https://secure.gravatar.com/avatar/...",
    "96": "https://secure.gravatar.com/avatar/..."
  },
  "meta": []
}
```

---

## Delete a Comment

Delete an existing comment. Requires authentication.

### Endpoint

```
DELETE /wp/v2/comments/<id>
```

### Example Request

```bash
# Move to trash (default)
curl -X DELETE https://example.com/wp-json/wp/v2/comments/157 \
  -u username:application_password

# Force delete permanently
curl -X DELETE "https://example.com/wp-json/wp/v2/comments/157?force=true" \
  -u username:application_password
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Comment ID |
| `force` | boolean | No | Bypass trash and force deletion (default: false) |
| `password` | string | No | Password for protected parent post |

### Example Response

```json
{
  "deleted": true,
  "previous": {
    "id": 157,
    "post": 42,
    "parent": 156,
    "author": 0,
    "author_name": "Jane Smith",
    "status": "approve"
  }
}
```

---

## Common Use Cases

### Get Comments for a Specific Post

```bash
curl "https://example.com/wp-json/wp/v2/comments?post=42"
```

### Get Threaded Comments (Top-level Only)

```bash
curl "https://example.com/wp-json/wp/v2/comments?post=42&parent=0"
```

### Get All Replies to a Comment

```bash
curl "https://example.com/wp-json/wp/v2/comments?parent=156"
```

### Get Pending Comments

```bash
curl "https://example.com/wp-json/wp/v2/comments?status=hold" \
  -u username:application_password
```

### Get Comments by Author Email

```bash
curl "https://example.com/wp-json/wp/v2/comments?author_email=jane@example.com" \
  -u username:application_password
```

### Get Recent Comments

```bash
curl "https://example.com/wp-json/wp/v2/comments?orderby=date_gmt&order=desc&per_page=10"
```

### Search Comments

```bash
curl "https://example.com/wp-json/wp/v2/comments?search=great"
```

### Bulk Approve Pending Comments

```bash
# Get all pending comments
curl "https://example.com/wp-json/wp/v2/comments?status=hold&per_page=100" \
  -u username:application_password | \
  jq -r '.[].id' | \
  while read comment_id; do
    curl -X POST "https://example.com/wp-json/wp/v2/comments/$comment_id" \
      -H "Content-Type: application/json" \
      -u username:application_password \
      -d '{"status": "approve"}'
  done
```

### Bulk Delete Spam Comments

```bash
# Delete all spam comments permanently
curl "https://example.com/wp-json/wp/v2/comments?status=spam&per_page=100" \
  -u username:application_password | \
  jq -r '.[].id' | \
  while read comment_id; do
    curl -X DELETE "https://example.com/wp-json/wp/v2/comments/$comment_id?force=true" \
      -u username:application_password
  done
```

### Get Comment Count by Post

```bash
curl "https://example.com/wp-json/wp/v2/comments?post=42&per_page=100" \
  -u username:application_password | \
  jq 'length'
```

### Get Comments with Specific Date Range

```bash
curl "https://example.com/wp-json/wp/v2/comments?after=2024-01-01T00:00:00&before=2024-01-31T23:59:59"
```

### Build Comment Thread Tree

```bash
# Get all comments for a post and organize by parent
curl "https://example.com/wp-json/wp/v2/comments?post=42&per_page=100" | \
  jq 'group_by(.parent) | map({parent: (.[0].parent | tostring), comments: [.[] | {id, content, author_name, date}]}) | from_entries'
```

### Get Comments for Moderation Queue

```bash
# Get unapproved comments with author info for moderation
curl "https://example.com/wp-json/wp/v2/comments?status=hold&context=edit&per_page=50" \
  -u username:application_password
```

### Track Comment Activity

```bash
# Get comments count by status
curl "https://example.com/wp-json/wp/v2/comments?per_page=100" \
  -u username:application_password | \
  jq '[
    {
      total: length,
      approved: [.[] | select(.status == "approved")] | length,
      pending: [.[] | select(.status == "hold")] | length,
      spam: [.[] | select(.status == "spam")] | length,
      trash: [.[] | select(.status == "trash")] | length
    }
  ]'
```

### Create Comments Programmatically

```bash
# Post comments to multiple posts
POSTS=(42 43 44 45)

for post_id in "${POSTS[@]}"; do
  curl -X POST https://example.com/wp-json/wp/v2/comments \
    -H "Content-Type: application/json" \
    -u username:application_password \
    -d "{
      \"post\": $post_id,
      \"content\": \"Great content!\",
      \"status\": \"approve\"
    }"
done
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
  "code": "rest_comment_invalid_id",
  "message": "Invalid comment ID.",
  "data": {
    "status": 404
  }
}
```

### 400 Bad Request

```json
{
  "code": "rest_comment_author_data_required",
  "message": "Invalid comment author data.",
  "data": {
    "status": 400
  }
}
```

### Comments Closed

```json
{
  "code": "rest_comment_closed",
  "message": "Sorry, comments are closed for this item.",
  "data": {
    "status": 403
  }
}
```

---

## Best Practices

1. **Implement Moderation**: Always review and moderate comments before publishing
2. **Use Threaded Comments**: Organize discussions with parent-child relationships
3. **Handle Spam**: Implement spam detection and filtering
4. **Rate Limiting**: Limit comment frequency to prevent spam
5. **Sanitize Input**: Always sanitize user-provided content
6. **Email Notifications**: Send notifications for new comments requiring moderation
7. **Pagination**: Use pagination for posts with many comments
8. **Cache Results**: Cache comment queries for better performance
9. **Guest vs Registered**: Differentiate between guest and registered user comments
10. **Respect Settings**: Honor WordPress discussion settings

---

## Comment Moderation Workflow

```bash
# 1. Get pending comments
PENDING=$(curl "https://example.com/wp-json/wp/v2/comments?status=hold&per_page=100" \
  -u username:application_password)

# 2. Review each comment
echo "$PENDING" | jq -r '.[] | "\(.id): \(.author_name) - \(.content.raw)"'

# 3. Approve legitimate comments
curl -X POST "https://example.com/wp-json/wp/v2/comments/157" \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{"status": "approve"}'

# 4. Mark spam as spam
curl -X POST "https://example.com/wp-json/wp/v2/comments/158" \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{"status": "spam"}'

# 5. Delete inappropriate comments
curl -X DELETE "https://example.com/wp-json/wp/v2/comments/159?force=true" \
  -u username:application_password
```

---

## Related Endpoints

- [Posts API Documentation](./wordpress-posts-api-documentation.md)
- [Pages API Documentation](./wordpress-pages-api-documentation.md)
- [Authentication Documentation](./wordpress-authentication-documentation.md)

---

*Documentation generated from the official WordPress REST API Reference*
