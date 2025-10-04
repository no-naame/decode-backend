#!/usr/bin/env python3
"""
Simple HTTP server to serve the GitHub App Authentication Tester frontend
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def serve_frontend():
    """Serve the frontend HTML file"""
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Set up the server
    PORT = 3000
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Create static directory if it doesn't exist
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    
    # Change to static directory to serve files
    os.chdir(static_dir)
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🌐 Frontend server running at http://localhost:{PORT}")
            print(f"📁 Serving files from: {static_dir.absolute()}")
            print("🚀 Opening browser...")
            
            # Open browser
            webbrowser.open(f"http://localhost:{PORT}")
            
            print("\n" + "="*50)
            print("🎯 GitHub App Authentication Tester")
            print("="*50)
            print("✅ Frontend: http://localhost:3000")
            print("✅ Backend:  http://localhost:8000")
            print("\n📋 Instructions:")
            print("1. Make sure your FastAPI app is running on port 8000")
            print("2. Use the frontend to test your GitHub authentication")
            print("3. Press Ctrl+C to stop the frontend server")
            print("="*50)
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Trying port {PORT + 1}")
            serve_frontend_port(PORT + 1)
        else:
            raise

def serve_frontend_port(port):
    """Serve frontend on a specific port"""
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"🌐 Frontend server running at http://localhost:{port}")
            webbrowser.open(f"http://localhost:{port}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")

if __name__ == "__main__":
    serve_frontend()
