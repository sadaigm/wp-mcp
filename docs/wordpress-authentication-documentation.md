# WordPress REST API: Authentication Documentation

This documentation covers the various authentication methods available for the WordPress REST API, including implementation examples and guidance on when to use each method.

## Table of Contents

- [Overview](#overview)
- [Cookie Authentication](#cookie-authentication)
- [Basic Authentication with Application Passwords](#basic-authentication-with-application-passwords)
- [OAuth 1.0a Authentication](#oauth-10a-authentication)
- [JWT Authentication](#jwt-authentication)
- [Choosing an Authentication Method](#choosing-an-authentication-method)
- [Security Best Practices](#security-best-practices)

---

## Overview

The WordPress REST API supports multiple authentication methods to accommodate different use cases, from internal plugin development to external third-party applications. Each method has specific advantages and is designed for particular scenarios.

### Authentication Methods Summary

| Method | Best For | Complexity | Security | External Access |
|--------|----------|------------|----------|-----------------|
| **Cookie Authentication** | Plugins/themes inside WordPress | Low | High (with nonces) | No |
| **Application Passwords** | Remote scripts, CLI tools, mobile apps | Low | High | Yes (HTTPS) |
| **OAuth 1.0a** | Third-party applications | High | High | Yes |
| **JWT** | Single Page Applications (SPAs), mobile apps | Medium | High | Yes |

---

## Cookie Authentication

Cookie authentication is the standard authentication method included with WordPress. It's designed for use within WordPress administration area and is automatically handled by the built-in JavaScript API.

### How It Works

When you log in to the WordPress dashboard, cookies are set up automatically. The REST API uses nonces (Number Used Once) to prevent CSRF (Cross-Site Request Forgery) attacks.

### Use Cases

- ✅ **Plugins and themes** running inside WordPress
- ✅ **Admin dashboard** custom functionality
- ✅ **AJAX requests** from within WordPress admin
- ❌ **Remote applications** or external services
- ❌ **Mobile apps** or desktop applications

### Implementation

#### Using WordPress Built-in JavaScript API

The built-in JavaScript client handles nonces automatically:

```php
// In your plugin or theme
wp_localize_script( 'wp-api', 'wpApiSettings', array(
    'root'  => esc_url_raw( rest_url() ),
    'nonce' => wp_create_nonce( 'wp_rest' )
) );
```

#### Manual AJAX with jQuery

```javascript
$.ajax( {
    url: wpApiSettings.root + 'wp/v2/posts/1',
    method: 'POST',
    beforeSend: function ( xhr ) {
        xhr.setRequestHeader( 'X-WP-Nonce', wpApiSettings.nonce );
    },
    data: {
        'title': 'Hello Moon'
    }
} ).done( function ( response ) {
    console.log( response );
} );
```

#### Using Fetch API

```javascript
fetch( wpApiSettings.root + 'wp/v2/posts/1', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-WP-Nonce': wpApiSettings.nonce
    },
    body: JSON.stringify( {
        title: 'Hello Moon'
    } )
} )
.then( response => response.json() )
.then( data => console.log( data ) );
```

#### Passing Nonce via URL Parameter

For GET requests, you can pass the nonce as a query parameter:

```javascript
fetch( wpApiSettings.root + 'wp/v2/posts?_wpnonce=' + wpApiSettings.nonce )
    .then( response => response.json() )
    .then( data => console.log( data ) );
```

### Important Notes

- Nonces are automatically validated by `rest_cookie_check_errors()`
- No manual nonce verification is needed in custom endpoints
- The nonce must be passed with every request
- Using the `X-WP-Nonce` header is the most reliable approach
- User must be logged into WordPress with appropriate capabilities

---

## Basic Authentication with Application Passwords

As of WordPress 5.6, Application Passwords are built into WordPress core and provide a secure way to authenticate remote applications without exposing user passwords.

### How It Works

Application Passwords are unique credentials generated for each application. They can be created from the WordPress admin interface and are used with Basic Authentication over HTTPS.

### Use Cases

- ✅ **Mobile applications** connecting to WordPress
- ✅ **Desktop applications** and CLI tools
- ✅ **Remote scripts** and automation
- ✅ **Third-party integrations** requiring API access
- ❌ **Browser-based applications** (credentials would be exposed)
- ❌ **HTTP-only connections** (requires HTTPS)

### Creating Application Passwords

1. Navigate to **Users > [Edit User]**
2. Scroll down to **Application Passwords** section
3. Enter a name for your application
4. Click **Add New Application Password**
5. Copy the generated password (shown only once)

### Implementation

#### Using cURL

```bash
curl --user "username:password" \
  https://example.com/wp-json/wp/v2/users?context=edit
```

#### Using JavaScript Fetch API

```javascript
const credentials = btoa( 'username:password' );

fetch( 'https://example.com/wp-json/wp/v2/posts', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + credentials
    },
    body: JSON.stringify( {
        title: 'New Post',
        content: 'Post content here...'
    } )
} )
.then( response => response.json() )
.then( data => console.log( data ) );
```

#### Using Python requests

```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get(
    'https://example.com/wp-json/wp/v2/users?context=edit',
    auth=HTTPBasicAuth('username', 'password')
)
print(response.json())
```

#### Using PHP

```php
$credentials = base64_encode( 'username:password' );

$response = wp_remote_get( 'https://example.com/wp-json/wp/v2/users?context=edit', array(
    'headers' => array(
        'Authorization' => 'Basic ' . $credentials
    )
) );
```

#### Using Node.js with Axios

```javascript
const axios = require( 'axios' );

axios.get( 'https://example.com/wp-json/wp/v2/users?context=edit', {
    auth: {
        username: 'username',
        password: 'password'
    }
} )
.then( response => console.log( response.data ) );
```

### Important Notes

- **HTTPS is required** for secure transmission
- Application Passwords are shown only once when created
- Each application should have its own unique password
- Passwords can be revoked from the Application Passwords section
- No plugin installation required (built into WordPress 5.6+)

---

## OAuth 1.0a Authentication

OAuth 1.0a is a complex authentication protocol that allows third-party applications to access WordPress resources without sharing user credentials.

### How It Works

OAuth 1.0a uses a token-based system with consumer keys, secrets, and access tokens. The authentication flow involves multiple steps including request token generation and user authorization.

### Use Cases

- ✅ **Third-party applications** requiring OAuth
- ✅ **Enterprise integrations** with existing OAuth systems
- ✅ **Public applications** where users grant access
- ❌ **Simple integrations** (Application Passwords are easier)
- ❌ **Internal WordPress plugins** (use Cookie auth)

### Implementation

#### Required Plugin

Install the [REST API OAuth 1.0a Server](https://wordpress.org/plugins/rest-api-oauth1/) plugin.

#### Authentication Flow

1. **Register your application** to get consumer key and secret
2. **Obtain request token** from `/oauth1/request`
3. **Authorize the request** by directing user to `/oauth1/authorize`
4. **Exchange for access token** at `/oauth1/access`
5. **Make authenticated requests** using OAuth signature

#### Example with JavaScript (using oauth-1.0a)

```javascript
const OAuth = require( 'oauth-1.0a' );
const crypto = require( 'crypto' );

const oauth = OAuth( {
    consumer: {
        key: 'your_consumer_key',
        secret: 'your_consumer_secret'
    },
    signature_method: 'HMAC-SHA1',
    hash_function: ( baseString, key ) => {
        return crypto.createHmac( 'sha1', key ).update( baseString ).digest( 'base64' );
    }
} );

const request_data = {
    url: 'https://example.com/wp-json/wp/v2/posts',
    method: 'GET'
};

const token = {
    key: 'access_token_key',
    secret: 'access_token_secret'
};

fetch( request_data.url, {
    headers: oauth.toHeader( oauth.authorize( request_data, token ) )
} )
.then( response => response.json() )
.then( data => console.log( data ) );
```

### Important Notes

- Requires plugin installation
- More complex to implement than Application Passwords
- Suitable for scenarios requiring OAuth specifically
- Provides ability to revoke access without changing passwords

---

## JWT Authentication

JSON Web Tokens (JWT) provide a stateless authentication mechanism that's popular for Single Page Applications (SPAs) and mobile applications.

### How It Works

JWT authentication generates a token upon login that is then sent with each subsequent request. The token contains encoded user information and is verified using a secret key.

### Use Cases

- ✅ **Single Page Applications** (React, Vue, Angular)
- ✅ **Mobile applications** (iOS, Android)
- ✅ **Headless WordPress** implementations
- ✅ **Decoupled architectures** with separate frontend
- ❌ **Traditional WordPress** plugins/themes (use Cookie auth)
- ❌ **Simple integrations** (Application Passwords are simpler)

### Implementation

#### Required Plugin

Install a JWT authentication plugin such as [JWT Authentication for WP REST API](https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/).

#### Authentication Flow

1. **Login to get token**: Send credentials to `/wp-json/jwt-auth/v1/token`
2. **Receive JWT token**: Server returns access token
3. **Include token in requests**: Add `Authorization: Bearer <token>` header

#### Login Request

```bash
curl -X POST https://example.com/wp-json/jwt-auth/v1/token \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

Response:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_email": "user@example.com",
  "user_nicename": "user",
  "user_display_name": "User Name"
}
```

#### Making Authenticated Requests

```javascript
const token = 'eyJ0eXAiOiJKV1QiLCJhbGc...';

fetch( 'https://example.com/wp-json/wp/v2/posts', {
    headers: {
        'Authorization': 'Bearer ' + token
    }
} )
.then( response => response.json() )
.then( data => console.log( data ) );
```

#### Token Refresh

Many JWT implementations support token refresh:

```javascript
// Refresh token before it expires
fetch( 'https://example.com/wp-json/jwt-auth/v1/token/refresh', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer ' + currentToken
    }
} )
.then( response => response.json() )
.then( data => {
    newToken = data.token;
} );
```

### Important Notes

- Requires plugin installation
- Token expiration must be handled
- Store tokens securely (not in localStorage for sensitive apps)
- Different plugins may have varying implementations
- Verify plugin compatibility with your WordPress version

---

## Choosing an Authentication Method

Select the appropriate authentication method based on your use case:

### Decision Tree

```
Is your code running inside WordPress admin?
├─ Yes → Use Cookie Authentication
└─ No → Is it a mobile/desktop app or remote script?
    ├─ Yes → Use Application Passwords (recommended)
    └─ No → Is it a SPA or decoupled frontend?
        ├─ Yes → Use JWT Authentication
        └─ No → Do you need OAuth specifically?
            ├─ Yes → Use OAuth 1.0a
            └─ No → Use Application Passwords
```

### Method Comparison

| Scenario | Recommended Method |
|----------|-------------------|
| WordPress admin plugin | Cookie Authentication |
| Browser-based dashboard | Cookie Authentication |
| Mobile app | Application Passwords or JWT |
| Desktop application | Application Passwords |
| CLI script | Application Passwords |
| SPA (React/Vue) | JWT |
| Third-party service | Application Passwords |
| OAuth required | OAuth 1.0a |

---

## Security Best Practices

### General Security

- **Always use HTTPS** for authenticated requests
- **Never expose credentials** in client-side code
- **Implement rate limiting** for API endpoints
- **Use least privilege principle** - grant minimum necessary permissions
- **Regular security audits** of authentication implementations

### Cookie Authentication Security

- **Always include nonces** in authenticated requests
- **Validate user capabilities** before performing actions
- **Use WordPress nonce functions** - don't implement custom nonces
- **Keep WordPress updated** for security patches

### Application Passwords Security

- **Use unique passwords** for each application
- **Rotate passwords periodically**
- **Revoke unused passwords**
- **Monitor application password usage**
- **Never share passwords** via email or chat

### OAuth Security

- **Store consumer secrets** securely
- **Use HTTPS callback URLs**
- **Implement proper state management** to prevent CSRF
- **Validate OAuth signatures** on server-side
- **Re compromised tokens immediately**

### JWT Security

- **Set appropriate token expiration times**
- **Use strong secret keys**
- **Implement refresh token mechanisms**
- **Validate tokens on every request**
- **Don't store tokens in localStorage** for sensitive applications

### Common Security Mistakes

❌ **DON'T**: Send credentials over HTTP
❌ **DON'T**: Embed credentials in client-side JavaScript
❌ **DON'T**: Use the same password for multiple applications
❌ **DON'T**: Ignore token expiration
❌ **DON'T**: Skip nonce validation in Cookie authentication

✅ **DO**: Use HTTPS for all authenticated requests
✅ **DO**: Implement proper error handling
✅ **DO**: Log authentication attempts for monitoring
✅ **DO**: Use WordPress built-in functions when possible
✅ **DO**: Keep authentication mechanisms updated

---

## Troubleshooting

### Common Issues

#### Cookie Authentication Issues

**Problem**: Requests returning 401 Unauthorized despite being logged in

**Solutions**:
- Verify nonce is being sent in `X-WP-Nonce` header
- Check that user has appropriate capabilities
- Clear browser cookies and re-login
- Verify REST API is not disabled

#### Application Password Issues

**Problem**: Authentication failing with Application Password

**Solutions**:
- Ensure HTTPS is being used
- Verify credentials are correctly encoded in Basic Auth
- Check that Application Password hasn't been revoked
- Confirm user account has necessary permissions

#### OAuth Issues

**Problem**: OAuth signature validation failing

**Solutions**:
- Verify system clock is synchronized (timestamps matter)
- Check consumer key and secret are correct
- Ensure all OAuth parameters are included
- Verify callback URL matches registered URL

#### JWT Issues

**Problem**: Token validation failing

**Solutions**:
- Check token hasn't expired
- Verify secret key configuration
- Ensure `Authorization` header format is correct: `Bearer <token>`
- Check for plugin compatibility issues

### Debugging Tips

```javascript
// Enable debug mode in WordPress
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );

// Log authentication attempts
add_filter( 'rest_authentication_errors', function( $result ) {
    if ( ! empty( $result ) ) {
        error_log( 'REST API Authentication Error: ' . $result->get_error_message() );
    }
    return $result;
} );
```

---

## Additional Resources

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [Application Passwords Integration Guide](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/)
- [WordPress Nonces Documentation](https://developer.wordpress.org/apis/security/nonces/)
- [OAuth 1.0a Specification](https://oauth.net/core/1.0a/)
- [JWT Specification](https://tools.ietf.org/html/rfc7519)

---

*Documentation generated from the official WordPress REST API Handbook*
