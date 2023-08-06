class RaspberryGPIO(object):

    is_debug = False

    def __init__(self, mode=None):

        import RPi.GPIO as GPIO

        if mode is None:
            GPIO.setmode(GPIO.BCM)
        else:
            GPIO.setmode(mode)

        GPIO.setwarnings(False)
        GPIO.cleanup()

        self.GPIO = GPIO

    def setup(self, mode, n):
        return getattr(self, "setup_" + mode)(n)

    def setup_input(self, n):
        return self.GPIO.setup(n, self.GPIO.IN)

    def setup_input_pull_up(self, n):
        return self.GPIO.setup(n, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)

    def setup_input_pull_down(self, n):
        return self.GPIO.setup(n, self.GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)

    def setup_output(self, n):
        self.GPIO.setup(n, self.GPIO.OUT)

    def setup_output_high(self, n):
        self.GPIO.setup(n, self.GPIO.OUT)
        self.GPIO.output(n, self.GPIO.HIGH)

    def setup_output_low(self, n):
        self.GPIO.setup(n, self.GPIO.OUT)
        self.GPIO.output(n, self.GPIO.LOW)

    async def input(self, n):
        return self.GPIO.input(n)

    async def output(self, n, high=True):
        self.GPIO.output(n, high and self.GPIO.HIGH or self.GPIO.LOW)

class DebugGPIO(object):

    is_debug = True

    def __init__(self, mode=None):
        self.store = {}

    def setup(self, mode, n):
        pass

    async def input(self, n):
        return self.store.get(n, None)

    async def output(self, n, high=True):
        self.store[n] = high and 1 or 0
        return high and 1 or 0