#!/usr/bin/env python3
"""
Start both the FastAPI backend and frontend server for GitHub Smart Authentication
"""

import subprocess
import sys
import time
import webbrowser
import threading
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def start_frontend():
    """Start the frontend server"""
    print("🌐 Starting frontend server...")
    try:
        subprocess.run([sys.executable, "serve_frontend.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    """Main function to start both servers"""
    print("🎯 GitHub Smart Authentication - Full App Starter")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Please run this script from the decode-backend root directory")
        return
    
    print("📋 Starting both servers...")
    print("✅ Backend: http://localhost:8000")
    print("✅ Frontend: http://localhost:3000")
    print("✅ API Docs: http://localhost:8000/docs")
    print("\n💡 Press Ctrl+C to stop both servers")
    print("=" * 60)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Start frontend in the main thread
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Both servers stopped")

if __name__ == "__main__":
    main()
