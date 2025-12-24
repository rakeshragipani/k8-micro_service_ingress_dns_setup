from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        backend_url = os.environ.get('BACKEND_URL', 'http://backend')
        
        try:
            # Internal call to backend service
            with urllib.request.urlopen(backend_url) as response:
                backend_data = json.loads(response.read().decode('utf-8'))
            
            result = {
                "message": "Hello from Frontend (Container)!", 
                "service": "frontend",
                "upstream_response": backend_data
            }
        except Exception as e:
            result = {
                "message": "Hello from Frontend (Container)!",
                "service": "frontend",
                "upstream_error": str(e)
            }
        
        self.wfile.write(json.dumps(result).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Handler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Frontend running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
