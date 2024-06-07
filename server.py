from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/jokes':
            with open('jokes.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_error(404, "File not found")

if __name__ == "__main__":
    PORT = 8000
    server = HTTPServer(('localhost', PORT), MyHandler)
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()
