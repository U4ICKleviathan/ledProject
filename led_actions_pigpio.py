import pigpio
import time
import threading
# a big shout-out to pigpio library http://abyz.co.uk/rpi/pigpio/python.html
# led_pin = 12			# RPi.GPIO used BCM mapping to identify pins
led_pin = 18  			# pigpio uses BROADCOM numbers for GPIO
MAX_DC_VALUE = 255		# this is the max duty cycle for PWM.  This value relates to the RGB color value


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
            return convert_brightness_percentage(float(self.kwargs['brightness']))
        else:
            return 0

    def run(self):
        pi = setup()
        pi = setup_pwm(pi)
        pi.set_PWM_dutycycle(led_pin, self.brightness)
        self.new_level = self.brightness
        while True:
            if self.brightness != self.new_level:
                pi.set_PWM_dutycycle(led_pin, self.new_level)
                self.brightness = self.new_level
            if self._stop:
                print 'im turning off'
                cleanup(pi)
                break

    def change_brightness(self, new_brightness):
        self.new_level = convert_brightness_percentage(new_brightness)
        pass

    def stop(self):
        self._stop = True


def convert_brightness_percentage(percentage):
    return round((percentage / 100.0) * MAX_DC_VALUE)


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
    pi = setup()
    return pi


def setup():
    # set up board
    pi = pigpio.pi()
    # set pins
    pi.set_mode(led_pin, pigpio.OUTPUT)
    return pi


def cleanup(pi):
    pi.set_mode(led_pin, pigpio.INPUT)
    pi.stop()


def turn_on(pi):
    pi.write(led_pin, 1)


def turn_off(pi):
    pi.write(led_pin, 0)


def blink():
    print "blink command called"
    pi = prep_new_action()
    for i in range(10):
        if i % 2 == 0:
            turn_on(pi)
        else:
            turn_off(pi)
        time.sleep(.25)
    cleanup(pi)


def setup_pwm(pi):
    pi.set_PWM_frequency(led_pin, 100)
    return pi


def fade():
    print 'fade command called'
    pi = prep_new_action()
    pi = setup_pwm(pi)
    for i in range(5):
        for dc in range(0, 255, 5):
            pi.set_PWM_dutycycle(led_pin, dc)
            time.sleep(0.025)
        for dc in range(255, -1, -5):
            pi.set_PWM_dutycycle(led_pin, dc)
            time.sleep(0.025)
    cleanup(pi)


def change_brightness(level):
    print "change_brightness", level
    if active_thread():
        _update_brightness(level)
    else:
        start_thread(level)


def main():
    pi = setup()
    turn_on(pi)
    time.sleep(3)
    turn_off(pi)
    time.sleep(1)
    fade()
    cleanup(pi)


if __name__ == '__main__':
    main()
