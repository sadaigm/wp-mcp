# WordPress REST API: Tags Endpoint Documentation

This documentation covers the WordPress REST API Tags endpoint (`/wp/v2/tags`), which allows you to programmatically manage WordPress tags.

## Table of Contents

- [Authentication](#authentication)
- [Tag Schema](#tag-schema)
- [List Tags](#list-tags)
- [Retrieve a Tag](#retrieve-a-tag)
- [Create a Tag](#create-a-tag)
- [Update a Tag](#update-a-tag)
- [Delete a Tag](#delete-a-tag)
- [Common Use Cases](#common-use-cases)

---

## Authentication

For read operations (GET requests), authentication is typically not required for public tags. However, write operations (POST, PUT, DELETE) require authentication.

### Authentication Methods

1. **Cookie Authentication**: Use when making requests from the WordPress admin area
2. **OAuth2 Authentication**: Use for third-party applications
3. **Basic Authentication**: Use with Application Passwords for simple cases
4. **JWT Authentication**: Use JSON Web Tokens for stateless authentication

### Example: Basic Authentication with Application Password

```bash
curl -u username:application_password https://example.com/wp-json/wp/v2/tags
```

---

## Tag Schema

The schema defines all fields available in a tag record:

| Field | Type | Context | Description |
|-------|------|---------|-------------|
| `id` | integer | view, edit, embed | Unique identifier (read-only) |
| `count` | integer | view, edit | Number of published posts (read-only) |
| `description` | string | view, edit | HTML description of the tag |
| `link` | string | view, edit, embed | URL of the tag (read-only) |
| `name` | string | view, edit, embed | HTML title for the tag |
| `slug` | string | view, edit, embed | URL-friendly identifier |
| `taxonomy` | string | view, edit, embed | Type attribution (always "post_tag") |
| `meta` | object | view, edit | Meta fields |

### Tags vs Categories

Tags differ from categories in that they are **non-hierarchical** (flat structure) and are typically used for more specific, granular labeling of content, while categories are used for broader grouping.

---

## List Tags

Retrieve a collection of tags with optional filtering and pagination.

### Endpoint

```
GET /wp/v2/tags
```

### Example Request

```bash
# Basic request
curl https://example.com/wp-json/wp/v2/tags

# With query parameters
curl "https://example.com/wp-json/wp/v2/tags?per_page=20&hide_empty=true"
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `context` | string | `view` | Scope of request: `view`, `embed`, `edit` |
| `page` | integer | `1` | Current page of the collection |
| `per_page` | integer | `10` | Maximum items per page (max 100) |
| `search` | string | - | Limit results to matching string |
| `exclude` | array | - | Exclude specific tag IDs |
| `include` | array | - | Include only specific tag IDs |
| `offset` | integer | - | Offset result set |
| `order` | string | `asc` | `asc` or `desc` |
| `orderby` | string | `name` | `id`, `include`, `name`, `slug`, `include_slugs`, `term_group`, `description`, `count` |
| `hide_empty` | boolean | - | Whether to hide tags not assigned to any posts |
| `post` | integer | - | Limit to tags assigned to a specific post |
| `slug` | array | - | Limit to specific slugs |

### Example Response

```json
[
  {
    "id": 15,
    "count": 28,
    "description": "Posts about JavaScript programming",
    "link": "https://example.com/tag/javascript/",
    "name": "JavaScript",
    "slug": "javascript",
    "taxonomy": "post_tag",
    "meta": [],
    "_links": {
      "self": [{"href": "https://example.com/wp-json/wp/v2/tags/15"}],
      "collection": [{"href": "https://example.com/wp-json/wp/v2/tags"}],
      "about": [{"href": "https://example.com/wp-json/wp/v2/taxonomies/post_tag"}]
    }
  },
  {
    "id": 22,
    "count": 42,
    "description": "Web development tutorials",
    "link": "https://example.com/tag/tutorial/",
    "name": "Tutorial",
    "slug": "tutorial",
    "taxonomy": "post_tag",
    "meta": [],
    "_links": {
      "self": [{"href": "https://example.com/wp-json/wp/v2/tags/22"}],
      "collection": [{"href": "https://example.com/wp-json/wp/v2/tags"}],
      "about": [{"href": "https://example.com/wp-json/wp/v2/taxonomies/post_tag"}],
      "wp:post_type": [{"href": "https://example.com/wp-json/wp/v2/posts?tags=22"}]
    }
  }
]
```

---

## Retrieve a Tag

Retrieve a specific tag by its ID.

### Endpoint

```
GET /wp/v2/tags/<id>
```

### Example Request

```bash
curl https://example.com/wp-json/wp/v2/tags/15
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Unique identifier for the tag |
| `context` | string | No | `view`, `embed`, `edit` (default: `view`) |

### Example Response

```json
{
  "id": 15,
  "count": 28,
  "description": "Posts about JavaScript programming",
  "link": "https://example.com/tag/javascript/",
  "name": "JavaScript",
  "slug": "javascript",
  "taxonomy": "post_tag",
  "meta": [],
  "_links": {
    "self": [{"href": "https://example.com/wp-json/wp/v2/tags/15"}],
    "collection": [{"href": "https://example.com/wp-json/wp/v2/tags"}],
    "about": [{"href": "https://example.com/wp-json/wp/v2/taxonomies/post_tag"}],
    "wp:post_type": [{"href": "https://example.com/wp-json/wp/v2/posts?tags=15"}]
  }
}
```

---

## Create a Tag

Create a new tag. Requires authentication.

### Endpoint

```
POST /wp/v2/tags
```

### Example Request

```bash
curl -X POST https://example.com/wp-json/wp/v2/tags \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "name": "React",
    "description": "Posts about React JavaScript library",
    "slug": "react"
  }'
```

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Tag name |
| `description` | string | No | HTML description of the tag |
| `slug` | string | No | URL-friendly identifier |
| `meta` | object | No | Meta fields |

### Creating Tags Programmatically

```bash
# Create multiple tags at once
for tag in "Vue.js" "Angular" "Svelte"; do
  curl -X POST https://example.com/wp-json/wp/v2/tags \
    -H "Content-Type: application/json" \
    -u username:application_password \
    -d "{\"name\": \"$tag\", \"description\": \"Posts about $tag framework\"}"
done
```

### Example Response

```json
{
  "id": 45,
  "count": 0,
  "description": "Posts about React JavaScript library",
  "link": "https://example.com/tag/react/",
  "name": "React",
  "slug": "react",
  "taxonomy": "post_tag",
  "meta": [],
  "_links": {
    "self": [{"href": "https://example.com/wp-json/wp/v2/tags/45"}],
    "collection": [{"href": "https://example.com/wp-json/wp/v2/tags"}],
    "about": [{"href": "https://example.com/wp-json/wp/v2/taxonomies/post_tag"}],
    "wp:post_type": [{"href": "https://example.com/wp-json/wp/v2/posts?tags=45"}]
  }
}
```

---

## Update a Tag

Update an existing tag. Requires authentication.

### Endpoint

```
POST /wp/v2/tags/<id>
```

### Example Request

```bash
curl -X POST https://example.com/wp-json/wp/v2/tags/45 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "name": "React.js",
    "description": "Posts about React.js library and ecosystem"
  }'
```

### Parameters

All parameters from [Create a Tag](#create-a-tag) are supported. Only include the fields you want to update.

### Renaming a Tag

```bash
# Rename a tag (useful for consolidating similar tags)
curl -X POST https://example.com/wp-json/wp/v2/tags/45 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "name": "React Development",
    "slug": "react-development"
  }'
```

### Example Response

```json
{
  "id": 45,
  "count": 0,
  "description": "Posts about React.js library and ecosystem",
  "link": "https://example.com/tag/react-development/",
  "name": "React.js",
  "slug": "react-development",
  "taxonomy": "post_tag",
  "meta": []
}
```

---

## Delete a Tag

Delete an existing tag. Requires authentication.

### Endpoint

```
DELETE /wp/v2/tags/<id>
```

### Example Request

```bash
curl -X DELETE https://example.com/wp-json/wp/v2/tags/45 \
  -u username:application_password
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Tag ID |
| `force` | boolean | Yes | Must be `true` (tags don't support trash) |

### Example Response

```json
{
  "deleted": true,
  "previous": {
    "id": 45,
    "count": 0,
    "description": "Posts about React.js library and ecosystem",
    "link": "https://example.com/tag/react-development/",
    "name": "React.js",
    "slug": "react-development",
    "taxonomy": "post_tag"
  }
}
```

---

## Common Use Cases

### Get All Non-Empty Tags

```bash
curl "https://example.com/wp-json/wp/v2/tags?hide_empty=true"
```

### Get Tags for a Specific Post

```bash
# Get tags assigned to post ID 42
curl "https://example.com/wp-json/wp/v2/tags?post=42"
```

### Search Tags

```bash
curl "https://example.com/wp-json/wp/v2/tags?search=javascript"
```

### Sort Tags by Post Count

```bash
curl "https://example.com/wp-json/wp/v2/tags?orderby=count&order=desc&per_page=50"
```

### Get Popular Tags (Most Used)

```bash
# Get top 10 most used tags
curl "https://example.com/wp-json/wp/v2/tags?orderby=count&order=desc&per_page=10"
```

### Get Tags by Slug

```bash
curl "https://example.com/wp-json/wp/v2/tags?slug[]=javascript&slug[]=react"
```

### Filter Tags by Count Range

```bash
# Get tags with more than 5 posts
curl "https://example.com/wp-json/wp/v2/tags" | \
  jq '.[] | select(.count > 5)'
```

### Create Tag Cloud Data

```bash
# Get all tags with their counts for a tag cloud
curl "https://example.com/wp-json/wp/v2/tags?hide_empty=true&per_page=100" | \
  jq '.[] | {name, slug, count, link}'
```

### Assign Tags to Multiple Posts

```bash
# First create the tag
TAG_RESPONSE=$(curl -X POST https://example.com/wp-json/wp/v2/tags \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{"name": "JavaScript", "description": "JavaScript programming posts"}')

TAG_ID=$(echo $TAG_RESPONSE | jq -r '.id')

# Then assign to posts
curl -X POST https://example.com/wp-json/wp/v2/posts/42 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{\"tags\": [$TAG_ID]}"

curl -X POST https://example.com/wp-json/wp/v2/posts/43 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{\"tags\": [$TAG_ID]}"
```

### Bulk Create Tags from List

```bash
# Create multiple tags from a list
TAGS=("TypeScript" "Node.js" "Express" "MongoDB" "GraphQL")

for tag in "${TAGS[@]}"; do
  curl -X POST https://example.com/wp-json/wp/v2/tags \
    -H "Content-Type: application/json" \
    -u username:application_password \
    -d "{\"name\": \"$tag\", \"description\": \"$tag related posts\"}"
done
```

### Merge Duplicate Tags

```bash
# 1. Get posts with old tag
POSTS=$(curl "https://example.com/wp-json/wp/v2/posts?tags=25" | jq -r '.[].id')

# 2. Update each post to use new tag instead
for post_id in $POSTS; do
  # Get existing tags for the post
  EXISTING_TAGS=$(curl "https://example.com/wp-json/wp/v2/posts/$post_id?context=edit" | jq -r '.tags | join(",")')

  # Add new tag ID (assuming new tag is ID 30)
  curl -X POST "https://example.com/wp-json/wp/v2/posts/$post_id" \
    -H "Content-Type: application/json" \
    -u username:application_password \
    -d "{\"tags\": [30, $EXISTING_TAGS]}"
done

# 3. Delete old tag
curl -X DELETE "https://example.com/wp-json/wp/v2/tags/25?force=true" \
  -u username:application_password
```

### Clean Up Unused Tags

```bash
# Delete all tags with zero posts
curl "https://example.com/wp-json/wp/v2/tags?hide_empty=false&per_page=100" | \
  jq -r '.[] | select(.count == 0) | .id' | \
  while read tag_id; do
    curl -X DELETE "https://example.com/wp-json/wp/v2/tags/$tag_id?force=true" \
      -u username:application_password
  done
```

### Generate Tag Statistics

```bash
# Get statistics about tag usage
curl "https://example.com/wp-json/wp/v2/tags?per_page=100" | \
  jq '[
    {
      total_tags: length,
      with_posts: [.[] | select(.count > 0)] | length,
      empty: [.[] | select(.count == 0)] | length,
      total_posts: [.[] | .count] | add,
      avg_posts: (.[] | .count | add / length)
    }
  ]'
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
  "code": "rest_term_invalid",
  "message": "Invalid tag ID.",
  "data": {
    "status": 404
  }
}
```

### 400 Bad Request

```json
{
  "code": "rest_missing_callback_param",
  "message": "Missing parameter(s): name",
  "data": {
    "status": 400,
    "params": ["name"]
  }
}
```

### Duplicate Tag

```json
{
  "code": "term_exists",
  "message": "A tag with the name provided already exists.",
  "data": {
    "status": 400,
    "term_id": 15
  }
}
```

---

## Tags vs Categories

| Feature | Tags | Categories |
|---------|------|-----------|
| Hierarchical | No (flat structure) | Yes (parent-child) |
| Endpoint | `/wp/v2/tags` | `/wp/v2/categories` |
| Required for Posts | No | No |
| Purpose | Specific labeling | Broad grouping |
| URL Structure | Tag base | Category base |
| Multiple Parents | N/A | No (single parent) |
| Best Practices | Use many tags per post | Use few categories per post |
| Example | "javascript", "tutorial", "2024" | "Technology", "Tutorials" |

---

## Best Practices

1. **Use Tags for Specific Topics**: Tags should be more specific than categories
2. **Keep Names Consistent**: Use consistent naming conventions (e.g., lowercase)
3. **Limit Tag Count**: Don't create too many tags for a single post (5-10 is reasonable)
4. **Use Descriptive Names**: Make tag names clear and meaningful
5. **Regular Cleanup**: Remove unused tags periodically
6. **Optimize Slugs**: Create SEO-friendly URL slugs
7. **Avoid Redundancy**: Don't create tags that duplicate categories
8. **Use for Cross-Categorization**: Tags help connect posts across different categories

---

## Tag Meta Fields

WordPress allows you to add custom meta fields to tags for additional functionality.

### Adding Meta to a Tag

```bash
curl -X POST https://example.com/wp-json/wp/v2/tags/15 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "meta": {
      "tag_color": "#f7df1e",
      "tag_icon": "fab fa-js",
      "featured": true,
      "priority": 5
    }
  }'
```

### Note on Meta Fields

Meta fields require proper registration in WordPress to be accessible via the REST API. Use the `register_meta` function or plugins that support REST API meta field registration.

---

## Working with Posts

### Adding Tags to a Post

```bash
curl -X POST https://example.com/wp-json/wp/v2/posts/42 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "tags": [15, 22, 45]
  }'
```

### Getting Posts by Tag

```bash
# Get posts with tag ID 15
curl "https://example.com/wp-json/wp/v2/posts?tags[]=15"

# Get posts with multiple tags (AND logic - posts must have all tags)
curl "https://example.com/wp-json/wp/v2/posts?tags[]=15&tags[]=22"
```

---

## Related Endpoints

- [Posts API Documentation](./wordpress-posts-api-documentation.md)
- [Categories API Documentation](./wordpress-categories-api-documentation.md)
- [Taxonomies API Documentation](https://developer.wordpress.org/rest-api/reference/taxonomies/)

---

*Documentation generated from the official WordPress REST API Reference*
