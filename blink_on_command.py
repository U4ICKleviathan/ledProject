import RPi.GPIO as GPIO
import time 
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer




led_pin=12

# set up board
GPIO.setmode(GPIO.BOARD)
# set pins 
GPIO.setup(led_pin, GPIO.OUT)

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("Hello World !")
		return

def turn_on():
	GPIO.output(led_pin, 1)

def turn_off():
	GPIO.output(led_pin, 0)

def blink():
	for i in range(10):
		if i%2==0:
			turn_on()
		else:
			turn_off()
		time.sleep(.25)

	turn_off()



def main():

	try:
	        #Create a web server and define the handler to manage the
	        #incoming request
	        server = HTTPServer(('', PORT_NUMBER), myHandler)
	        print 'Started httpserver on port ' , PORT_NUMBER

	        #Wait forever for incoming htto requests
	        server.serve_forever()

	except KeyboardInterrupt:
	        print '^C received, shutting down the web server'
	        server.socket.close()

if __name__ == "__main__":
	main()




