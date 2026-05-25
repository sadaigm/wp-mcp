# WordPress REST API: Categories Endpoint Documentation

This documentation covers the WordPress REST API Categories endpoint (`/wp/v2/categories`), which allows you to programmatically manage WordPress categories.

## Table of Contents

- [Authentication](#authentication)
- [Category Schema](#category-schema)
- [List Categories](#list-categories)
- [Retrieve a Category](#retrieve-a-category)
- [Create a Category](#create-a-category)
- [Update a Category](#update-a-category)
- [Delete a Category](#delete-a-category)
- [Common Use Cases](#common-use-cases)

---

## Authentication

For read operations (GET requests), authentication is typically not required for public categories. However, write operations (POST, PUT, DELETE) require authentication.

### Authentication Methods

1. **Cookie Authentication**: Use when making requests from the WordPress admin area
2. **OAuth2 Authentication**: Use for third-party applications
3. **Basic Authentication**: Use with Application Passwords for simple cases
4. **JWT Authentication**: Use JSON Web Tokens for stateless authentication

### Example: Basic Authentication with Application Password

```bash
curl -u username:application_password https://example.com/wp-json/wp/v2/categories
```

---

## Category Schema

The schema defines all fields available in a category record:

| Field | Type | Context | Description |
|-------|------|---------|-------------|
| `id` | integer | view, edit, embed | Unique identifier (read-only) |
| `count` | integer | view, edit | Number of published posts (read-only) |
| `description` | string | view, edit | HTML description of the category |
| `link` | string | view, edit, embed | URL of the category (read-only) |
| `name` | string | view, edit, embed | HTML title for the category |
| `slug` | string | view, edit, embed | URL-friendly identifier |
| `taxonomy` | string | view, edit, embed | Type attribution (always "category") |
| `parent` | integer | view, edit | Parent category ID for hierarchical structure |
| `meta` | object | view, edit | Meta fields |

### Hierarchical Categories

Categories in WordPress support hierarchical relationships, allowing you to create parent-child category structures.

---

## List Categories

Retrieve a collection of categories with optional filtering and pagination.

### Endpoint

```
GET /wp/v2/categories
```

### Example Request

```bash
# Basic request
curl https://example.com/wp-json/wp/v2/categories

# With query parameters
curl "https://example.com/wp-json/wp/v2/categories?per_page=20&hide_empty=true"
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `context` | string | `view` | Scope of request: `view`, `embed`, `edit` |
| `page` | integer | `1` | Current page of the collection |
| `per_page` | integer | `10` | Maximum items per page (max 100) |
| `search` | string | - | Limit results to matching string |
| `exclude` | array | - | Exclude specific category IDs |
| `include` | array | - | Include only specific category IDs |
| `order` | string | `asc` | `asc` or `desc` |
| `orderby` | string | `name` | `id`, `include`, `name`, `slug`, `include_slugs`, `term_group`, `description`, `count` |
| `hide_empty` | boolean | - | Whether to hide categories not assigned to any posts |
| `parent` | integer | - | Limit to categories with specific parent ID |
| `post` | integer | - | Limit to categories assigned to a specific post |
| `slug` | array | - | Limit to specific slugs |

### Example Response

```json
[
  {
    "id": 1,
    "count": 42,
    "description": "Uncategorized posts",
    "link": "https://example.com/category/uncategorized/",
    "name": "Uncategorized",
    "slug": "uncategorized",
    "taxonomy": "category",
    "parent": 0,
    "meta": [],
    "_links": {
      "self": [{"href": "https://example.com/wp-json/wp/v2/categories/1"}],
      "collection": [{"href": "https://example.com/wp-json/wp/v2/categories"}],
      "about": [{"href": "https://example.com/wp-json/wp/v2/taxonomies/category"}]
    }
  },
  {
    "id": 5,
    "count": 15,
    "description": "Technology and programming posts",
    "link": "https://example.com/category/technology/",
    "name": "Technology",
    "slug": "technology",
    "taxonomy": "category",
    "parent": 0,
    "meta": [],
    "_links": {
      "self": [{"href": "https://example.com/wp-json/wp/v2/categories/5"}],
      "collection": [{"href": "https://example.com/wp-json/wp/v2/categories"}],
      "about": [{"href": "https://example.com/wp-json/wp/v2/taxonomies/category"}],
      "up": [{"embeddable": true, "href": "https://example.com/wp-json/wp/v2/categories/0"}]
    }
  }
]
```

---

## Retrieve a Category

Retrieve a specific category by its ID.

### Endpoint

```
GET /wp/v2/categories/<id>
```

### Example Request

```bash
curl https://example.com/wp-json/wp/v2/categories/5
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Unique identifier for the category |
| `context` | string | No | `view`, `embed`, `edit` (default: `view`) |

### Example Response

```json
{
  "id": 5,
  "count": 15,
  "description": "Technology and programming posts",
  "link": "https://example.com/category/technology/",
  "name": "Technology",
  "slug": "technology",
  "taxonomy": "category",
  "parent": 0,
  "meta": [],
  "_links": {
    "self": [{"href": "https://example.com/wp-json/wp/v2/categories/5"}],
    "collection": [{"href": "https://example.com/wp-json/wp/v2/categories"}],
    "about": [{"href": "https://example.com/wp-json/wp/v2/taxonomies/category"}],
    "up": [{"embeddable": true, "href": "https://example.com/wp-json/wp/v2/categories/0"}],
    "wp:post_type": [{"href": "https://example.com/wp-json/wp/v2/posts?categories=5"}]
  }
}
```

---

## Create a Category

Create a new category. Requires authentication.

### Endpoint

```
POST /wp/v2/categories
```

### Example Request

```bash
curl -X POST https://example.com/wp-json/wp/v2/categories \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "name": "Web Development",
    "description": "Posts about web development, HTML, CSS, and JavaScript",
    "slug": "web-development",
    "parent": 5
  }'
```

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Category name |
| `description` | string | No | HTML description of the category |
| `slug` | string | No | URL-friendly identifier |
| `parent` | integer | No | Parent category ID |
| `meta` | object | No | Meta fields |

### Creating Child Categories

```bash
# Create a child category under "Technology"
curl -X POST https://example.com/wp-json/wp/v2/categories \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "name": "JavaScript",
    "description": "JavaScript programming posts",
    "parent": 5
  }'
```

### Example Response

```json
{
  "id": 18,
  "count": 0,
  "description": "Posts about web development, HTML, CSS, and JavaScript",
  "link": "https://example.com/category/web-development/",
  "name": "Web Development",
  "slug": "web-development",
  "taxonomy": "category",
  "parent": 5,
  "meta": [],
  "_links": {
    "self": [{"href": "https://example.com/wp-json/wp/v2/categories/18"}],
    "collection": [{"href": "https://example.com/wp-json/wp/v2/categories"}],
    "about": [{"href": "https://example.com/wp-json/wp/v2/taxonomies/category"}],
    "up": [{"embeddable": true, "href": "https://example.com/wp-json/wp/v2/categories/5"}],
    "wp:post_type": [{"href": "https://example.com/wp-json/wp/v2/posts?categories=18"}]
  }
}
```

---

## Update a Category

Update an existing category. Requires authentication.

### Endpoint

```
POST /wp/v2/categories/<id>
```

### Example Request

```bash
curl -X POST https://example.com/wp-json/wp/v2/categories/18 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "name": "Web Development & Design",
    "description": "Updated description covering web development and design topics"
  }'
```

### Parameters

All parameters from [Create a Category](#create-a-category) are supported. Only include the fields you want to update.

### Changing Category Hierarchy

```bash
# Move a category to become a child of another category
curl -X POST https://example.com/wp-json/wp/v2/categories/18 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "parent": 10
  }'
```

### Example Response

```json
{
  "id": 18,
  "count": 0,
  "description": "Updated description covering web development and design topics",
  "link": "https://example.com/category/web-development-design/",
  "name": "Web Development & Design",
  "slug": "web-development-design",
  "taxonomy": "category",
  "parent": 10,
  "meta": []
}
```

---

## Delete a Category

Delete an existing category. Requires authentication.

### Endpoint

```
DELETE /wp/v2/categories/<id>
```

### Example Request

```bash
curl -X DELETE https://example.com/wp-json/wp/v2/categories/18 \
  -u username:application_password
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Category ID |
| `force` | boolean | Yes | Must be `true` (categories don't support trash) |

### Example Response

```json
{
  "deleted": true,
  "previous": {
    "id": 18,
    "count": 0,
    "description": "Updated description covering web development and design topics",
    "link": "https://example.com/category/web-development-design/",
    "name": "Web Development & Design",
    "slug": "web-development-design",
    "taxonomy": "category",
    "parent": 10
  }
}
```

---

## Common Use Cases

### Get All Top-Level Categories

```bash
curl "https://example.com/wp-json/wp/v2/categories?parent=0&hide_empty=false"
```

### Get All Child Categories

```bash
# Get all children of category ID 5
curl "https://example.com/wp-json/wp/v2/categories?parent=5"
```

### Get Categories for a Specific Post

```bash
# Get categories assigned to post ID 42
curl "https://example.com/wp-json/wp/v2/categories?post=42"
```

### Get Only Non-Empty Categories

```bash
curl "https://example.com/wp-json/wp/v2/categories?hide_empty=true"
```

### Search Categories

```bash
curl "https://example.com/wp-json/wp/v2/categories?search=tech"
```

### Sort Categories by Post Count

```bash
curl "https://example.com/wp-json/wp/v2/categories?orderby=count&order=desc"
```

### Get Categories by Slug

```bash
curl "https://example.com/wp-json/wp/v2/categories?slug[]=technology&slug[]=web-development"
```

### Build Category Tree

```bash
# Get all categories and build a tree structure
curl "https://example.com/wp-json/wp/v2/categories?per_page=100&hide_empty=false" | \
  jq 'group_by(.parent) | map({parent: (.[0].parent | tostring), categories: .}) | from_entries'
```

### Get Category with Most Posts

```bash
curl "https://example.com/wp-json/wp/v2/categories?per_page=1&orderby=count&order=desc"
```

### Filter Categories by Count Range

```bash
# Get categories with more than 10 posts
curl "https://example.com/wp-json/wp/v2/categories" | \
  jq '.[] | select(.count > 10)'
```

### Assign Category to Multiple Posts

```bash
# First create the category
CATEGORY_RESPONSE=$(curl -X POST https://example.com/wp-json/wp/v2/categories \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{"name": "News", "description": "News and updates"}')

CATEGORY_ID=$(echo $CATEGORY_RESPONSE | jq -r '.id')

# Then assign to posts
curl -X POST https://example.com/wp-json/wp/v2/posts/42 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{\"categories\": [$CATEGORY_ID]}"

curl -X POST https://example.com/wp-json/wp/v2/posts/43 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{\"categories\": [$CATEGORY_ID]}"
```

### Create Category Hierarchy

```bash
# 1. Create parent category
PARENT_RESPONSE=$(curl -X POST https://example.com/wp-json/wp/v2/categories \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{"name": "Programming", "description": "Programming articles"}')

PARENT_ID=$(echo $PARENT_RESPONSE | jq -r '.id')

# 2. Create child categories
curl -X POST https://example.com/wp-json/wp/v2/categories \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{\"name\": \"Python\", \"parent\": $PARENT_ID}"

curl -X POST https://example.com/wp-json/wp/v2/categories \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{\"name\": \"JavaScript\", \"parent\": $PARENT_ID}"

curl -X POST https://example.com/wp-json/wp/v2/categories \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d "{\"name\": \"PHP\", \"parent\": $PARENT_ID}"
```

### Bulk Update Categories

```bash
# Update multiple categories at once
for id in 5 10 15; do
  curl -X POST "https://example.com/wp-json/wp/v2/categories/$id" \
    -H "Content-Type: application/json" \
    -u username:application_password \
    -d '{"description": "Updated description"}'
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
  "code": "rest_term_invalid",
  "message": "Invalid category ID.",
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

### Duplicate Category

```json
{
  "code": "term_exists",
  "message": "A category with the name provided already exists.",
  "data": {
    "status": 400,
    "term_id": 5
  }
}
```

---

## Categories vs Tags

| Feature | Categories | Tags |
|---------|-----------|------|
| Hierarchical | Yes (parent-child) | No (flat structure) |
| Endpoint | `/wp/v2/categories` | `/wp/v2/tags` |
| Required for Posts | No | No |
| Purpose | Broad grouping | Specific labeling |
| URL Structure | Category base | Tag base |
| Multiple Parents | No | N/A |

---

## Best Practices

1. **Use Hierarchical Structure**: Create logical parent-child relationships for better organization
2. **Keep Names Concise**: Use short, descriptive category names
3. **Optimize Slugs**: Create SEO-friendly URL slugs
4. **Use Descriptions**: Provide meaningful descriptions for each category
5. **Avoid Empty Categories**: Consider hiding empty categories or populate them with content
6. **Limit Depth**: Keep category hierarchy to 2-3 levels for better UX
7. **Consistent Naming**: Use consistent naming conventions across categories
8. **Regular Cleanup**: Remove unused categories periodically

---

## Category Meta Fields

WordPress allows you to add custom meta fields to categories for additional functionality.

### Adding Meta to a Category

```bash
curl -X POST https://example.com/wp-json/wp/v2/categories/5 \
  -H "Content-Type: application/json" \
  -u username:application_password \
  -d '{
    "meta": {
      "category_icon": "fas fa-code",
      "category_color": "#3498db",
      "featured": true
    }
  }'
```

### Note on Meta Fields

Meta fields require proper registration in WordPress to be accessible via the REST API. Use the `register_meta` function or plugins that support REST API meta field registration.

---

## Related Endpoints

- [Posts API Documentation](./wordpress-posts-api-documentation.md)
- [Tags API Documentation](./wordpress-tags-api-documentation.md)
- [Taxonomies API Documentation](https://developer.wordpress.org/rest-api/reference/taxonomies/)

---

*Documentation generated from the official WordPress REST API Reference*
