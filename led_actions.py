import RPi.GPIO as GPIO
import time
import threading

led_pin = 12

class BrightnessThread(threading.Thread):

    def __init__(self, group=None, target=None, name='BrightnessThread',
                 args=(), kwargs=None, verbose=None):
        super(BrightnessThread, self).__init__(group=group, target=target,
                                       name=name, verbose=verbose)
        self._stop = False
        self.args = args
        self.kwargs = kwargs
        self.brightness = self.configure_brightness()
        self.new_level = 0
	return

    def configure_brightness(self):
        if 'brightness' in self.kwargs.keys():
            return float(self.kwargs['brightness'])
        else:
            return 0

    def run(self):
	setup()
	p = GPIO.PWM(led_pin, 50)
        p.start(self.brightness)
        self.new_level = self.brightness
        while True:
	    if self.brightness != self.new_level:
       	        p.ChangeDutyCycle(self.new_level)
		self.brightness = self.new_level
            if self._stop:
                print 'im turning off'
		p.stop()
		cleanup()
                break
        return

    def change_brightness(self, new_brightness):
        self.new_level = new_brightness
        pass

    def stop(self):
        self._stop = True


def start_thread(start_level):
    t = BrightnessThread(kwargs={'brightness': start_level})
    t.start()


def active_thread():
    active_threads = threading.enumerate()
    for t in active_threads:
        if 'Brightness' in t.getName():
            return True
    return False


def _update_brightness(new_value):
    bthread = retrieve_thread()
    bthread.change_brightness(new_value)
    

def retrieve_thread():
    for thread in threading.enumerate():
        if 'Brightness' in thread.getName():
            return thread
    return None

def kill_thread():
    if active_thread():
        thread = retrieve_thread()
        thread.stop()


def prep_new_action():
    kill_thread()
    time.sleep(.10)
    setup()



def setup():
    # set up board
    GPIO.setmode(GPIO.BOARD)
    # set pins
    GPIO.setup(led_pin, GPIO.OUT)


def cleanup():
    GPIO.cleanup()


def turn_on():
    GPIO.output(led_pin, 1)


def turn_off():
    GPIO.output(led_pin, 0)


def blink():
    print "bling command called"
    prep_new_action()
    for i in range(10):
        if i % 2 == 0:
            turn_on()
        else:
            turn_off()
        time.sleep(.25)
    cleanup()

def fade():
    print 'fade command called'
    prep_new_action()
    p = GPIO.PWM(led_pin, 500)
    p.start(0)
    for i in range(5):
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.025)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.025)
    p.stop()
    cleanup()

def change_brightness(level): 
    print "change_brightness", level
    if active_thread():
        _update_brightness(level)
    else:
        start_thread(level)

def main():
	setup() 
	change_brightness(30)
	time.sleep(5)
	change_brightness(90)
	time.sleep(5)
	prep_new_action()
	blink()

if __name__ == '__main__':
	main()
