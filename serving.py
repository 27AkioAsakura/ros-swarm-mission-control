import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 10000))

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check if file exists, otherwise serve index.html (SPA routing)
        path = self.path.lstrip('/')
        if not path or (not os.path.exists(path) and "." not in path):
            self.path = "/index.html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    print(f"Starting frontend server on port {PORT}")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
