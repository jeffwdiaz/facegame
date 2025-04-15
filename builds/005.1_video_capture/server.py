from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import os

def run_server(port=8000):
    # Change to the directory where the script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create server
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    # Open browser
    webbrowser.open(f'http://localhost:{port}')
    
    print(f"Server running at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == '__main__':
    run_server() 