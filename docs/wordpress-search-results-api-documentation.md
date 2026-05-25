# WordPress REST API: Search Results Endpoint Documentation

This documentation covers the WordPress REST API Search Results endpoint (`/wp/v2/search`), which allows you to perform searches across multiple content types in WordPress.

## Table of Contents

- [Authentication](#authentication)
- [Search Result Schema](#search-result-schema)
- [List Search Results](#list-search-results)
- [Search Parameters](#search-parameters)
- [Common Use Cases](#common-use-cases)
- [Search Best Practices](#search-best-practices)

---

## Authentication

Search operations typically don't require authentication for public content. However, authentication may be needed to search private or restricted content.

### Authentication Methods

1. **Cookie Authentication**: Use when making requests from the WordPress admin area
2. **OAuth2 Authentication**: Use for third-party applications
3. **Basic Authentication**: Use with Application Passwords for simple cases
4. **JWT Authentication**: Use JSON Web Tokens for stateless authentication

### Example: Basic Authentication with Application Password

```bash
curl -u username:application_password "https://example.com/wp-json/wp/v2/search?search=keyword"
```

---

## Search Result Schema

The schema defines all fields available in a search result record:

| Field | Type | Context | Description |
|-------|------|---------|-------------|
| `id` | integer/string | view, embed | Unique identifier for the object (read-only) |
| `title` | string | view, embed | Title for the object (read-only) |
| `url` | string | view, embed | URL to the object (read-only) |
| `type` | string | view, embed | Object type: `post`, `term`, `post-format` |
| `subtype` | string | view, embed | Object subtype: `post`, `page`, `category`, `post_tag` |

### Searchable Content Types

The search endpoint can return results from multiple content types:

- **Posts**: Blog posts and custom post types
- **Pages**: Static pages
- **Categories**: Category taxonomy terms
- **Tags**: Tag taxonomy terms
- **Custom Post Types**: Any registered custom post types
- **Custom Taxonomies**: Any registered taxonomies

---

## List Search Results

Perform a search query across WordPress content.

### Endpoint

```
GET /wp/v2/search
```

### Example Request

```bash
# Basic search
curl "https://example.com/wp-json/wp/v2/search?search=wordpress"

# Search with pagination
curl "https://example.com/wp-json/wp/v2/search?search=tutorial&per_page=20&page=1"

# Search specific content types
curl "https://example.com/wp-json/wp/v2/search?search=javascript&type=post"
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `context` | string | `view` | Scope of request: `view`, `embed` |
| `page` | integer | `1` | Current page of the collection |
| `per_page` | integer | `10` | Maximum items per page (max 100) |
| `search` | string | - | Search query string |
| `type` | string | `post` | Object type: `post`, `term`, `post-format` |
| `subtype` | string | `any` | Object subtype: `post`, `page`, `category`, `post_tag` |
| `exclude` | array | - | Exclude specific IDs from results |
| `include` | array | - | Include only specific IDs in results |

### Example Response

```json
[
  {
    "id": 42,
    "title": "Getting Started with WordPress Development",
    "url": "https://example.com/getting-started-with-wordpress-development/",
    "type": "post",
    "subtype": "post"
  },
  {
    "id": 15,
    "title": "WordPress",
    "url": "https://example.com/category/wordpress/",
    "type": "term",
    "subtype": "category"
  },
  {
    "id": 5,
    "title": "WordPress Tutorial",
    "url": "https://example.com/wordpress-tutorial/",
    "type": "post",
    "subtype": "page"
  }
]
```

---

## Search Parameters

### Search Query

The `search` parameter accepts a string to search for in titles and content.

```bash
# Simple keyword search
curl "https://example.com/wp-json/wp/v2/search?search=javascript"

# Phrase search
curl "https://example.com/wp-json/wp/v2/search?search=react%20tutorial"

# Case-insensitive search
curl "https://example.com/wp-json/wp/v2/search?search=WordPress"
```

### Content Type Filtering

Filter results by specific content types:

```bash
# Search only posts
curl "https://example.com/wp-json/wp/v2/search?search=tutorial&type=post"

# Search only terms (categories/tags)
curl "https://example.com/wp-json/wp/v2/search?search=technology&type=term"

# Search only pages
curl "https://example.com/wp-json/wp/v2/search?search=about&subtype=page"

# Search specific categories
curl "https://example.com/wp-json/wp/v2/search?search=news&subtype=category"

# Search specific tags
curl "https://example.com/wp-json/wp/v2/search?search=javascript&subtype=post_tag"
```

### Subtype Filtering

Search within specific subtypes:

```bash
# Search multiple subtypes
curl "https://example.com/wp-json/wp/v2/search?search=tutorial&subtype[]=post&subtype[]=page"

# Search only custom post types
curl "https://example.com/wp-json/wp/v2/search?search=product&subtype=product"
```

---

## Common Use Cases

### Implement Site Search

```bash
# Basic site search functionality
curl "https://example.com/wp-json/wp/v2/search?search=$QUERY&per_page=20"
```

### Create Search Autocomplete

```javascript
// JavaScript autocomplete implementation
async function searchAutocomplete(query) {
    const response = await fetch(
        `https://example.com/wp-json/wp/v2/search?search=${encodeURIComponent(query)}&per_page=5`
    );
    const results = await response.json();
    
    return results.map(result => ({
        title: result.title,
        url: result.url,
        type: result.subtype
    }));
}

// Use with debouncing for better performance
const searchInput = document.getElementById('search-input');
let debounceTimer;

searchInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
        if (e.target.value.length > 2) {
            const results = await searchAutocomplete(e.target.value);
            displaySuggestions(results);
        }
    }, 300);
});
```

### Search with Pagination

```bash
# Get first page
curl "https://example.com/wp-json/wp/v2/search?search=wordpress&per_page=20&page=1"

# Get second page
curl "https://example.com/wp-json/wp/v2/search?search=wordpress&per_page=20&page=2"

# Get total result count (from headers)
curl -I "https://example.com/wp-json/wp/v2/search?search=wordpress"
```

### Filter Search by Content Type

```bash
# Search only posts
curl "https://example.com/wp-json/wp/v2/search?type=post&search=tutorial"

# Search only categories and tags
curl "https://example.com/wp-json/wp/v2/search?type=term&search=technology"
```

### Exclude Specific Items from Results

```bash
# Exclude specific post/page IDs
curl "https://example.com/wp-json/wp/v2/search?exclude[]=1&exclude[]=42"
```

### Include Only Specific Items

```bash
# Search within specific items only
curl "https://example.com/wp-json/wp/v2/search?include[]=10&include[]=20&include[]=30"
```

### Get Total Search Result Count

```bash
# Use X-WP-Total header to get total results
curl -I "https://example.com/wp-json/wp/v2/search?search=wordpress"
```

Response headers include:
```
X-WP-Total: 45
X-WP-TotalPages: 3
```

### Multi-Type Search Display

```bash
# Get all results and organize by type
curl "https://example.com/wp-json/wp/v2/search?search=tutorial&per_page=50" | \
  jq 'group_by(.subtype) | map({
    type: .[0].subtype,
    count: length,
    items: [.[] | {id, title, url}]
  })'
```

### Search with Result Caching

```javascript
// Implement client-side caching
const searchCache = new Map();

async function cachedSearch(query) {
    if (searchCache.has(query)) {
        return searchCache.get(query);
    }
    
    const response = await fetch(
        `https://example.com/wp-json/wp/v2/search?search=${encodeURIComponent(query)}`
    );
    const results = await response.json();
    
    searchCache.set(query, results);
    
    // Clear cache after 5 minutes
    setTimeout(() => searchCache.delete(query), 300000);
    
    return results;
}
```

### PHP Implementation

```php
<?php
function search_wordpress($query, $per_page = 10, $page = 1) {
    $url = home_url('/wp-json/wp/v2/search');
    $params = array(
        'search' => $query,
        'per_page' => $per_page,
        'page' => $page
    );
    
    $response = wp_remote_get(add_query_arg($params, $url));
    
    if (is_wp_error($response)) {
        return array();
    }
    
    $body = wp_remote_retrieve_body($response);
    return json_decode($body, true);
}

// Usage
$results = search_wordpress('wordpress tutorial');
foreach ($results as $result) {
    echo '<a href="' . esc_url($result['url']) . '">';
    echo esc_html($result['title']);
    echo '</a><br>';
}
```

### Python Implementation

```python
import requests

def search_wordpress(site_url, query, per_page=10, page=1):
    endpoint = f"{site_url}/wp-json/wp/v2/search"
    params = {
        'search': query,
        'per_page': per_page,
        'page': page
    }
    
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    
    return response.json()

# Usage
results = search_wordpress('https://example.com', 'tutorial')
for result in results:
    print(f"{result['title']}: {result['url']}")
```

### Advanced Search with Multiple Filters

```bash
# Search posts and pages, exclude specific IDs
curl "https://example.com/wp-json/wp/v2/search?\
search=tutorial&\
type=post&\
subtype[]=post&\
subtype[]=page&\
exclude[]=1&\
exclude[]=42&\
per_page=20"
```

---

## Search Best Practices

### Performance Optimization

1. **Use Pagination**: Always implement pagination for search results
2. **Limit Results**: Set reasonable `per_page` limits (10-50)
3. **Cache Results**: Implement caching for common search queries
4. **Debounce Input**: Add delays to prevent excessive API calls
5. **Index Content**: Ensure WordPress search indexing is enabled

### User Experience

1. **Show Result Count**: Display total results found
2. **Highlight Type**: Indicate content type in results
3. **Provide Context**: Show excerpt or context for matches
4. **Handle No Results**: Provide helpful message when no results found
5. **Search Suggestions**: Offer autocomplete or suggestions

### Security

1. **Sanitize Input**: Always sanitize search queries
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Access Control**: Respect user permissions for private content
4. **Escape Output**: Properly escape results in display

### Common Patterns

```javascript
// Comprehensive search implementation
class WordPressSearch {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.cache = new Map();
    }
    
    async search(query, options = {}) {
        const {
            type = null,
            subtype = null,
            perPage = 10,
            page = 1
        } = options;
        
        const params = new URLSearchParams({
            search: query,
            per_page: perPage,
            page: page
        });
        
        if (type) params.append('type', type);
        if (subtype) params.append('subtype', subtype);
        
        const url = `${this.baseUrl}/wp-json/wp/v2/search?${params}`;
        
        // Check cache
        if (this.cache.has(url)) {
            return this.cache.get(url);
        }
        
        try {
            const response = await fetch(url);
            const results = await response.json();
            const totalCount = response.headers.get('X-WP-Total');
            const totalPages = response.headers.get('X-WP-TotalPages');
            
            const data = {
                results,
                totalCount: parseInt(totalCount),
                totalPages: parseInt(totalPages)
            };
            
            // Cache for 5 minutes
            this.cache.set(url, data);
            setTimeout(() => this.cache.delete(url), 300000);
            
            return data;
        } catch (error) {
            console.error('Search error:', error);
            return { results: [], totalCount: 0, totalPages: 0 };
        }
    }
    
    clearCache() {
        this.cache.clear();
    }
}

// Usage
const wpSearch = new WordPressSearch('https://example.com');

async function handleSearch(query) {
    const data = await wpSearch.search(query, {
        perPage: 20,
        type: 'post'
    });
    
    console.log(`Found ${data.totalCount} results`);
    return data.results;
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "code": "rest_invalid_param",
  "message": "Invalid parameter(s): search",
  "data": {
    "status": 400
  }
}
```

### Empty Results

```json
[]
```

---

## Related Endpoints

- [Posts API Documentation](./wordpress-posts-api-documentation.md)
- [Pages API Documentation](./wordpress-pages-api-documentation.md)
- [Categories API Documentation](./wordpress-categories-api-documentation.md)
- [Tags API Documentation](./wordpress-tags-api-documentation.md)

---

## Additional Resources

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [Global Parameters](https://developer.wordpress.org/rest-api/using-the-rest-api/global-parameters/)
- [Pagination](https://developer.wordpress.org/rest-api/using-the-rest-api/pagination/)

---

*Documentation generated from the official WordPress REST API Reference*
