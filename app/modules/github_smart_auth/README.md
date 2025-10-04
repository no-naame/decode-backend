# GitHub Smart Authentication Module

This module provides intelligent GitHub App authentication that works like Vercel, Lovable, and other popular GitHub Apps.

## Features

- **No Manual Installation ID Management**: Automatically discovers and uses the right installation
- **Context-Aware Authentication**: Works with webhooks, repository context, user context
- **Fallback Support**: Falls back to app-level when installation-specific isn't available
- **Webhook-Ready**: Automatically extracts installation ID from webhook payloads

## API Endpoints

### App-Level Operations (No Installation ID Required)
- `GET /github-smart-auth/app/info` - Get GitHub App information
- `GET /github-smart-auth/app/installations` - Get all installations

### Smart Repository Operations (Automatically Finds Installation)
- `GET /github-smart-auth/repositories` - Get repositories
- `GET /github-smart-auth/repositories/{owner}/{repo}` - Get repository details
- `GET /github-smart-auth/repositories/{owner}/{repo}/contents` - Get repository contents
- `GET /github-smart-auth/repositories/{owner}/{repo}/file` - Get file content
- `GET /github-smart-auth/repositories/{owner}/{repo}/branches` - Get branches
- `GET /github-smart-auth/repositories/{owner}/{repo}/commits` - Get commits
- `GET /github-smart-auth/repositories/{owner}/{repo}/issues` - Get issues
- `POST /github-smart-auth/repositories/{owner}/{repo}/issues` - Create issue

### Webhook Support
- `POST /github-smart-auth/webhooks/github` - Handle GitHub webhooks

## Environment Variables

```bash
GITHUB_APP_ID="your-app-id"
GITHUB_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----..."
```

## Usage Examples

### Get All Repositories (Smart)
```bash
curl -X GET "http://localhost:8000/api/v1/github-smart-auth/repositories"
```

### Get Repository Details (Smart)
```bash
curl -X GET "http://localhost:8000/api/v1/github-smart-auth/repositories/octocat/Hello-World"
```

### Create Issue (Smart)
```bash
curl -X POST "http://localhost:8000/api/v1/github-smart-auth/repositories/octocat/Hello-World/issues" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Issue",
    "body": "This is a test issue"
  }'
```

## How It Works

1. **Context-Aware Authentication**: The service determines the right authentication method based on context
2. **Automatic Installation Discovery**: For repository operations, it finds which installation has access to the repository
3. **Webhook-Driven**: Webhook events automatically extract installation ID from payload
4. **Fallback to App-Level**: When no specific installation is found, it uses app-level authentication

## Security

- **Installation Isolation**: Each installation can only access its own repositories
- **Automatic Token Management**: Tokens are cached and refreshed automatically
- **Context Validation**: Ensures the right installation is used for each operation
- **Webhook Security**: Validates webhook payloads and extracts installation ID safely
