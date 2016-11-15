from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 8080

# This class will handles any incoming request from
# the browser

class controlerServer(object):
    def __init__(self):
        self.handler = self.myHandler()

    class myHandler(BaseHTTPRequestHandler):
        def __init__(self):
            pass
        # Handler for the GET requests
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Send the html message
            self.wfile.write("Hello World !")
            return

    def start_server(self):
        try:
            # Create a web server and define the handler to manage the
            # incoming request
            server = HTTPServer(('', PORT_NUMBER), self.handler)
            print( 'Started httpserver on port ', PORT_NUMBER)
            # Wait forever for incoming http requests
            server.serve_forever()

        except KeyboardInterrupt:
            print ('shutting down server')
            server.socket.close()


def main():
    cs = controlerServer()
    cs.start_server()

if __name__ == '__main__':
    main()


