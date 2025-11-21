#!/usr/bin/env python3
"""
Simple HTTP Server for Local Testing

Usage:
    python3 scripts/local-test-server.py
    
Then open: http://localhost:8000

The server will serve files from the current directory.
Useful for testing HTML/JavaScript without CORS issues.
"""

import http.server
import socketserver
import os
import sys

# Configuration
PORT = 8000
DIRECTORY = "integration"  # Serve from integration folder

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Check if directory exists
    if not os.path.exists(DIRECTORY):
        print(f"⚠️  Warning: Directory '{DIRECTORY}' not found!")
        print(f"Creating directory...")
        os.makedirs(DIRECTORY, exist_ok=True)
        print(f"✅ Directory created. Add your HTML files to '{DIRECTORY}/'")
    
    # Start server
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"\n🚀 PCCM Integration Test Server")
        print(f"================================")
        print(f"\n📂 Serving files from: {os.path.abspath(DIRECTORY)}")
        print(f"🌐 Server running at: http://localhost:{PORT}")
        print(f"\n💡 Open your browser and navigate to the URL above")
        print(f"\n⏹️  Press Ctrl+C to stop the server\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
