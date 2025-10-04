# 🚀 Quick Start Guide - GitHub Smart Authentication

Get your GitHub Smart Authentication system up and running in minutes!

## ⚡ Quick Start (5 Minutes)

### 1. Set Environment Variables

Create a `.env` file in the decode-backend root directory:

```bash
# GitHub App Authentication
GITHUB_APP_ID="your-app-id-here"
GITHUB_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
your-private-key-content-here
-----END RSA PRIVATE KEY-----"
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Full App

```bash
python start_full_app.py
```

This will start both the backend (port 8000) and frontend (port 3000) automatically.

### 4. Test the System

The frontend will automatically open in your browser. You can also manually visit:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs

## 🎯 What You'll See

### Frontend Interface
- **Installation Tab**: Check GitHub App installation status
- **Smart Auth Tab**: Test smart authentication (recommended)
- **Basic Auth Tab**: Test traditional authentication
- **Custom Tests Tab**: Test any endpoint with custom parameters

### Backend API
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **GitHub Smart Auth**: http://localhost:8000/api/v1/github-smart-auth/

## 🧪 Testing Workflow

### Step 1: Check Installation
1. Go to the "Installation" tab
2. Click "Check Status"
3. If not installed, follow the installation guide

### Step 2: Test Smart Auth
1. Go to the "Smart Auth" tab
2. Click "App Info" to verify configuration
3. Click "Get Installations" to see installed apps
4. Click "Get Repositories" to see accessible repositories

### Step 3: Test Specific Repository
1. Enter a repository like `octocat/Hello-World`
2. Click "Test Repository"
3. See repository details and contents

## 🔧 Manual Setup (Alternative)

If you prefer to start servers manually:

### Start Backend Only
```bash
python main.py
```

### Start Frontend Only
```bash
python serve_frontend.py
```

### Test Authentication
```bash
python test_github_smart_auth.py
```

## 📋 Common Issues & Solutions

### Issue: "GitHub App ID is not configured"
**Solution**: Set `GITHUB_APP_ID` in your `.env` file

### Issue: "GitHub private key must be provided"
**Solution**: Set `GITHUB_PRIVATE_KEY` in your `.env` file

### Issue: "Cannot connect to API server"
**Solution**: Make sure the backend is running on port 8000

### Issue: "No installations found"
**Solution**: Install your GitHub App on your account/organization

## 🎉 Success Indicators

You'll know everything is working when you see:

✅ **Frontend**: "Connected to API server successfully! GitHub Smart Auth is ready."
✅ **Backend**: "App-level authentication successful!"
✅ **Installations**: Shows your installed GitHub Apps
✅ **Repositories**: Lists accessible repositories

## 📚 Next Steps

Once everything is working:

1. **Explore the API**: Use the interactive docs at http://localhost:8000/docs
2. **Test Different Repositories**: Try accessing different repositories
3. **Create Issues**: Test creating issues in repositories
4. **Webhook Testing**: Set up webhooks for real-time events
5. **Production Deployment**: Deploy to your preferred cloud platform

## 🆘 Need Help?

- **Setup Guide**: See `GITHUB_SMART_AUTH_SETUP.md` for detailed setup
- **Frontend Guide**: See `FRONTEND_SETUP.md` for frontend usage
- **API Documentation**: Visit http://localhost:8000/docs
- **Test Script**: Run `python test_github_smart_auth.py`

## 🎯 Key Features

- **Smart Authentication**: No manual installation ID management
- **Context-Aware**: Automatically finds the right installation
- **Webhook-Ready**: Handles GitHub webhooks automatically
- **Beautiful UI**: Modern, responsive frontend interface
- **Real-time Testing**: Test endpoints with instant feedback
- **Comprehensive Logging**: Detailed error messages and debugging

Your GitHub Smart Authentication system is now ready to use! 🚀
