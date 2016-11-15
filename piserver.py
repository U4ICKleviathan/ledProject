try:
    import led_actions_pigpio as led_actions
except ImportError:
    print "This machine cannot access GPIO, therefore we will simulate GPIO actions"
    import led_action_simulator as led_actions
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import logging
from pprint import pprint

PORT_NUMBER = 8080
ACTION_KEY = "action"
VARIABLES_KEY = "variables"

server_log = logging.getLogger()


# This class will handle any incoming request
class PiServer(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print '{0:s} - - [{1:s}] {2:s}\n'.format(self.client_address[0], self.log_date_time_string(), format % args)
        return

    # Handler for the GET requests
    def do_GET(self):
        request_path = self.path
        command = "NOT FOUND"
        print("\n----- Request Start ----->\n")
        for index, value in enumerate(request_path):
            if value == "/":
                command = request_path[index + 1:]
                break
        print command
        if "brightness" in command:
            brightness_level = float(command[11:])

        led_actions.change_brightness(brightness_level)
        self.send_response(200)
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        print(request_headers)
        print(self.rfile.read(length))
        print("<----- Request End -----\n")

        self.end_headers()
        # Send the html message
        self.wfile.write("Server Is Online")
        return

    def do_POST(self):
        # Extract and print the contents of the POST
        raw_data = self.rfile.read(int(self.headers['Content-Length']))
        request_data = json.loads(raw_data)
        print request_data
        action = extract_action(request_data)
        action_variables = extract_variables(request_data)
        try:
            action_dict[action](**action_variables)
        except Exception:
            print "something went wrong"
            print Exception

        self.send_response(200)
        self.end_headers()


def extract_action(request_data):
    try:
        return request_data[ACTION_KEY]
    except Exception:
        print "No action set"
        print str(Exception)


def extract_variables(request_data):
    try:
        return request_data[VARIABLES_KEY]
    except Exception:
        print "No action set"
        print str(Exception)


def parse_path(request_path):
    command = None
    print("\n----- Request Start ----->\n")
    for index, value in enumerate(request_path):
        if value == "/" and request_path[index + 1] == "?":
            command = request_path[index + 2:]
            break
    print command
    if "brightness" in command:
        brightness_level = command[11:]
    print("<----- Request End -----\n")


def change_brightness(**kwargs):
    led_actions.change_brightness(**kwargs)
    pass


def change_color(**kwargs):
    led_actions.change_color(**kwargs)
    pass

action_dict = {
    "customColor": change_color,
    "changeBrightness": change_brightness
}

def main():
    server = None
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        SocketServer.TCPServer.allow_reuse_address = True
        server = HTTPServer(('', PORT_NUMBER), PiServer)
        print 'Started http server on port ', PORT_NUMBER
        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print "shutting down the server"
        server.socket.close()
        led_actions.kill_thread()


if __name__ == "__main__":
    main()
