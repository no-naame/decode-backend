# Frontend Setup for GitHub Smart Authentication

This guide will help you set up and use the frontend testing interface for the GitHub Smart Authentication system.

## 🎯 Overview

The frontend provides a beautiful, interactive web interface to test your GitHub App authentication. It's designed to work like the interfaces you'd find in Vercel, Lovable, and other popular GitHub Apps.

## 🚀 Features

- **Interactive Testing**: Test all GitHub Smart Auth endpoints with a beautiful UI
- **Installation Management**: Check installation status and get installation guides
- **Smart Authentication**: Test repository access without manual installation ID management
- **Custom Testing**: Test any endpoint with custom parameters
- **Real-time Results**: See API responses in real-time with syntax highlighting

## 📋 Prerequisites

1. **Backend Running**: Your FastAPI backend must be running on port 8000
2. **GitHub App Configured**: Your GitHub App must be set up with proper environment variables
3. **Python Environment**: Python 3.8+ for running the frontend server

## 🔧 Setup Steps

### Step 1: Start the Backend

First, make sure your FastAPI backend is running:

```bash
# In the decode-backend directory
python main.py
```

The backend should be running at `http://localhost:8000`

### Step 2: Start the Frontend

In a new terminal, run the frontend server:

```bash
# In the decode-backend directory
python serve_frontend.py
```

The frontend will automatically open in your browser at `http://localhost:3000`

### Step 3: Test the Connection

The frontend will automatically test the connection to your backend when it loads. You should see:

- ✅ **Success**: "Connected to API server successfully! GitHub Smart Auth is ready."
- ❌ **Error**: Connection issues or configuration problems

## 🎮 Using the Frontend

### Installation Tab

**Purpose**: Check GitHub App installation status and get installation guidance

**Features**:
- **Check Status**: Verify if your GitHub App is installed
- **Install GitHub App**: Get instructions for manual installation
- **Installation Guide**: Step-by-step setup instructions

### Smart Auth Tab (Recommended)

**Purpose**: Test the smart authentication system (like Vercel/Lovable)

**Features**:
- **App Info**: Get GitHub App information
- **Get Installations**: List all app installations
- **Get Repositories**: List repositories from all installations
- **Test Specific Repository**: Test access to a specific repository

**Example Usage**:
1. Click "App Info" to verify your app configuration
2. Click "Get Installations" to see installed apps
3. Click "Get Repositories" to see accessible repositories
4. Enter a repository like `octocat/Hello-World` and click "Test Repository"

### Basic Auth Tab

**Purpose**: Test traditional GitHub authentication (for comparison)

**Features**:
- Test basic authentication endpoints
- Compare with smart authentication

### Custom Tests Tab

**Purpose**: Test any endpoint with custom parameters

**Features**:
- **Custom Endpoint**: Test any API endpoint
- **Query Parameters**: Add custom query parameters
- **Flexible Testing**: Test edge cases and specific scenarios

**Example Usage**:
1. Enter endpoint: `/api/v1/github-smart-auth/repositories/octocat/Hello-World/contents`
2. Add query parameters: `path=README.md&limit=10`
3. Click "Test Custom Endpoint"

## 🧪 Testing Scenarios

### Scenario 1: First-Time Setup

1. **Check Installation Status**: Verify no installations yet
2. **Install GitHub App**: Follow the installation guide
3. **Check Status Again**: Verify installation
4. **Test Smart Auth**: Try getting repositories

### Scenario 2: Repository Access

1. **Get Repositories**: See all accessible repositories
2. **Test Specific Repository**: Test access to a known repository
3. **Test Repository Contents**: Browse repository files
4. **Test Repository Issues**: Check issues and create new ones

### Scenario 3: Custom Testing

1. **Test Branches**: Get repository branches
2. **Test Commits**: Get recent commits
3. **Test File Content**: Get specific file content
4. **Test Issue Creation**: Create a test issue

## 🔍 Understanding Results

### Success Responses

```json
{
  "success": true,
  "count": 5,
  "repositories": [...]
}
```

### Error Responses

```json
{
  "success": false,
  "error": "GitHub App ID is not configured",
  "message": "Please set GITHUB_APP_ID environment variable"
}
```

### Common Error Messages

- **"GitHub App ID is not configured"**: Set `GITHUB_APP_ID` in your `.env` file
- **"GitHub private key must be provided"**: Set `GITHUB_PRIVATE_KEY` in your `.env` file
- **"App-level authentication failed"**: Check your GitHub App configuration
- **"No installations found"**: Install your GitHub App on your account/organization

## 🛠️ Troubleshooting

### Frontend Won't Start

**Error**: `Port 3000 is already in use`

**Solution**: The script will automatically try port 3001. If that's also in use, kill the process using port 3000:

```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>
```

### Backend Connection Issues

**Error**: `Cannot connect to API server`

**Solutions**:
1. Make sure your FastAPI backend is running on port 8000
2. Check that the backend is accessible at `http://localhost:8000`
3. Verify your environment variables are set correctly

### GitHub App Issues

**Error**: `App-level authentication failed`

**Solutions**:
1. Check your `GITHUB_APP_ID` is correct
2. Verify your `GITHUB_PRIVATE_KEY` is properly formatted
3. Ensure your GitHub App has the required permissions
4. Check that your private key matches your app

### Installation Issues

**Error**: `No installations found`

**Solutions**:
1. Install your GitHub App on your account/organization
2. Grant access to the repositories you want to test
3. Check that the app has the required permissions

## 🎨 Customization

### Styling

The frontend uses a modern, responsive design with:
- **Gradient backgrounds**: Beautiful color schemes
- **Interactive buttons**: Hover effects and animations
- **Syntax highlighting**: Code blocks with proper formatting
- **Responsive design**: Works on desktop and mobile

### Adding New Endpoints

To test new endpoints:

1. **Add to Smart Auth Tab**: Add buttons for new smart auth endpoints
2. **Add to Custom Tests**: Use the custom testing interface
3. **Modify JavaScript**: Add new functions in the `<script>` section

### Adding New Features

To add new features:

1. **New Tab**: Add a new tab in the HTML
2. **New Functions**: Add JavaScript functions for new functionality
3. **New Endpoints**: Add corresponding backend endpoints

## 📱 Mobile Support

The frontend is fully responsive and works on:
- **Desktop**: Full feature set with large interface
- **Tablet**: Optimized layout for touch interaction
- **Mobile**: Compact interface with essential features

## 🔒 Security Notes

- **No Sensitive Data**: The frontend doesn't store or transmit sensitive information
- **Local Testing**: Designed for local development and testing
- **Environment Variables**: Keep your GitHub credentials secure
- **HTTPS**: Use HTTPS in production environments

## 🚀 Production Deployment

For production use:

1. **Static Hosting**: Deploy the static files to a CDN or static host
2. **Backend API**: Deploy your FastAPI backend to a cloud service
3. **Environment Variables**: Set production environment variables
4. **HTTPS**: Use HTTPS for both frontend and backend
5. **CORS**: Configure CORS for your production domain

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub App Documentation](https://docs.github.com/en/developers/apps)
- [JavaScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

## 🤝 Support

If you encounter issues:

1. **Check the Console**: Open browser developer tools for error messages
2. **Check Backend Logs**: Look at your FastAPI server logs
3. **Test Manually**: Use curl or Postman to test endpoints directly
4. **Verify Configuration**: Double-check your environment variables

The frontend is now ready to help you test and debug your GitHub Smart Authentication system! 🎉
