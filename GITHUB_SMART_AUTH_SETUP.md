# GitHub Smart Authentication Setup Guide

This guide will help you set up the GitHub Smart Authentication system in the decode-backend project.

## 🎯 Overview

The GitHub Smart Authentication system provides intelligent GitHub App authentication that works like Vercel, Lovable, and other popular GitHub Apps. It automatically discovers and uses the right installation without manual management.

## 🚀 Features

- **No Manual Installation ID Management**: Automatically discovers and uses the right installation
- **Context-Aware Authentication**: Works with webhooks, repository context, user context
- **Fallback Support**: Falls back to app-level when installation-specific isn't available
- **Webhook-Ready**: Automatically extracts installation ID from webhook payloads

## 📋 Prerequisites

1. **GitHub Account**: You need a GitHub account to create a GitHub App
2. **Python Environment**: Python 3.8+ with pip
3. **GitHub App**: A GitHub App with appropriate permissions

## 🔧 Setup Steps

### Step 1: Create a GitHub App

1. Go to [GitHub Developer Settings](https://github.com/settings/apps)
2. Click "New GitHub App"
3. Fill in the required information:
   - **GitHub App name**: `decode-backend-smart-auth` (or your preferred name)
   - **Homepage URL**: `http://localhost:8000` (for development)
   - **Webhook URL**: `http://localhost:8000/api/v1/github-smart-auth/webhooks/github` (for development)
   - **Webhook secret**: Generate a random string (optional but recommended)

4. **Set Permissions**:
   - **Repository permissions**:
     - Contents: Read
     - Issues: Read & Write
     - Pull requests: Read
     - Metadata: Read
   - **Account permissions**:
     - None required for basic functionality

5. **Subscribe to events** (optional):
   - Issues
   - Pull requests
   - Push

6. Click "Create GitHub App"

### Step 2: Get App Credentials

1. After creating the app, go to the app's settings page
2. Note down the **App ID** (you'll need this for `GITHUB_APP_ID`)
3. Scroll down to "Private keys" section
4. Click "Generate a private key"
5. Download the `.pem` file and note its location

### Step 3: Install the GitHub App

1. Go to your GitHub App's settings page
2. Click "Install App" in the left sidebar
3. Choose to install on your account or organization
4. Select the repositories you want to give access to
5. Click "Install"

### Step 4: Set Environment Variables

Create a `.env` file in the decode-backend root directory:

```bash
# GitHub App Authentication
GITHUB_APP_ID="your-app-id-here"
GITHUB_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
your-private-key-content-here
-----END RSA PRIVATE KEY-----"

# Optional: GitHub Token (for fallback)
GITHUB_TOKEN="your-personal-access-token"
```

**Important**: 
- Replace `your-app-id-here` with your actual App ID
- Replace the private key content with the actual content from your `.pem` file
- The private key should include the `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----` lines

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Test the Implementation

Run the test script to verify everything is working:

```bash
python test_github_smart_auth.py
```

If successful, you should see:
```
✅ App-level authentication successful!
✅ Found X installations
✅ Found Y repositories
🎉 All tests completed successfully!
```

### Step 7: Start the Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔗 API Endpoints

### App-Level Operations
- `GET /api/v1/github-smart-auth/app/info` - Get GitHub App information
- `GET /api/v1/github-smart-auth/app/installations` - Get all installations

### Smart Repository Operations
- `GET /api/v1/github-smart-auth/repositories` - Get repositories
- `GET /api/v1/github-smart-auth/repositories/{owner}/{repo}` - Get repository details
- `GET /api/v1/github-smart-auth/repositories/{owner}/{repo}/contents` - Get repository contents
- `GET /api/v1/github-smart-auth/repositories/{owner}/{repo}/file` - Get file content
- `GET /api/v1/github-smart-auth/repositories/{owner}/{repo}/branches` - Get branches
- `GET /api/v1/github-smart-auth/repositories/{owner}/{repo}/commits` - Get commits
- `GET /api/v1/github-smart-auth/repositories/{owner}/{repo}/issues` - Get issues
- `POST /api/v1/github-smart-auth/repositories/{owner}/{repo}/issues` - Create issue

### Webhook Support
- `POST /api/v1/github-smart-auth/webhooks/github` - Handle GitHub webhooks

## 🧪 Testing Examples

### Get All Repositories
```bash
curl -X GET "http://localhost:8000/api/v1/github-smart-auth/repositories"
```

### Get Repository Details
```bash
curl -X GET "http://localhost:8000/api/v1/github-smart-auth/repositories/octocat/Hello-World"
```

### Create an Issue
```bash
curl -X POST "http://localhost:8000/api/v1/github-smart-auth/repositories/octocat/Hello-World/issues" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Issue",
    "body": "This is a test issue created via the smart auth API"
  }'
```

## 🔒 Security Considerations

1. **Private Key Security**: Never commit your private key to version control
2. **Environment Variables**: Use `.env` files and add them to `.gitignore`
3. **Webhook Security**: Implement webhook signature verification in production
4. **Token Management**: The system automatically manages token expiration and refresh

## 🐛 Troubleshooting

### Common Issues

1. **"GitHub App ID is not configured"**
   - Check that `GITHUB_APP_ID` is set in your `.env` file
   - Verify the App ID is correct

2. **"GitHub private key must be provided"**
   - Check that `GITHUB_PRIVATE_KEY` is set in your `.env` file
   - Verify the private key format is correct (including BEGIN/END lines)

3. **"App-level authentication failed"**
   - Verify your GitHub App is properly configured
   - Check that the private key matches the app
   - Ensure the app has the required permissions

4. **"No installations found"**
   - Make sure you've installed the GitHub App on your account/organization
   - Check that the app has access to repositories

### Debug Mode

To enable debug logging, set the log level in your environment:

```bash
export LOG_LEVEL=DEBUG
```

## 📖 Additional Resources

- [GitHub App Documentation](https://docs.github.com/en/developers/apps)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [JWT Token Documentation](https://jwt.io/)

## 🤝 Support

If you encounter any issues:

1. Check the logs for error messages
2. Verify your environment variables
3. Test with the provided test script
4. Check the GitHub App settings and permissions

The GitHub Smart Authentication system is now ready to use! 🎉
