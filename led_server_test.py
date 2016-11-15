import RPi.GPIO as GPIO
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

led_pin = 12

# set up board
GPIO.setmode(GPIO.BOARD)
# set pins
GPIO.setup(led_pin, GPIO.OUT)

PORT_NUMBER = 8080

# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("Server Is Online")
        return
    

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
	for key in form.keys():
	    print(key,  form[key])
        for field in form.keys():
	    field_item = form[field]
	    if field == "command":
	        print "Received command " , field_item.value
                if field_item.value == 'blink':
		   blink()
        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')

        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                self.wfile.write('\tUploaded %s as "%s" (%d bytes)\n' % \
                        (field, field_item.filename, file_len))
            else:
                # Regular form value
                self.wfile.write('\t%s=%s\n' % (field, form[field].value))
        return        


def turn_on():
    GPIO.output(led_pin, 1)

def turn_off():
    GPIO.output(led_pin, 0)

def blink():
    for i in range(10):
        if i % 2 == 0:
            turn_on()
        else:
            turn_off()
        time.sleep(.25)

    turn_off()


def main():
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print 'Started httpserver on port ', PORT_NUMBER

        # Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print "shutting down the server"
        server.socket.close()
	GPIO.cleanup()
if __name__ == "__main__":
	main()
