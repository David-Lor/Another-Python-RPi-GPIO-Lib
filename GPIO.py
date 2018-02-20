
import os
import atexit
import threading
from time import sleep

#Arduino-Like alias and keywords
OUT = "out"
OUTPUT = OUT
IN = "in"
INPUT = IN
HIGH = True
LOW = False
FALLING = 0
RISING = 1
BOTH = 2

class Pin(object):
    def __init__(self, pin, mode, default_value=False):
        self.pin = int(pin) #GPIO Pin number
        self.mode = mode #GPIO mode (IN or OUT)
        if self.mode not in (IN, OUT): #Check "mode" param
            raise(self.WrongInput("Pin Mode must be IN or OUT"))
        self.on = True #Is the pin enabled? (ready to use) (exported)
        os.popen("echo {} > /sys/class/gpio/export".format(pin)) #Enable pin (export)
        if mode == OUTPUT: #If pin is OUTPUT
            HIGHLOW = {True : "high", False : "low"}
            os.popen("echo {} > /sys/class/gpio/gpio{}/direction".format(HIGHLOW[default_value], pin)) #Set initial output value
        else: #If pin is INPUT
            os.popen("echo in > /sys/class/gpio/gpio{}/direction".format(pin))
        @atexit.register
        def atexit_f(): #Deactivate the pin at exit (unexport)
            self.deactivate()
    def write(self, value):
        """Write a digital value to an OUT pin
        :param value: bool value to write (True/False)
        """
        if self.mode == INPUT:
            raise(self.InvalidOperation("Pin is set as INPUT, not OUTPUT!"))
        value = int(value)
        os.popen("echo {} > /sys/class/gpio/gpio{}/value".format(value, self.pin))
    def read(self):
        """Read a digital value from an IN pin
        :return: bool value of the pin (True/False)
        """
        if self.mode == OUTPUT:
            raise(self.InvalidOperation("Pin is set as OUTPUT, not INPUT!"))
        out = os.popen("cat /sys/class/gpio/gpio{}/value".format(self.pin)).read()
        return bool(int(out))
    def deactivate(self):
        """Free up (unexport) the pin"""
        if self.on:
            os.popen("echo {} > /sys/class/gpio/unexport".format(self.pin))
            self.on = False
    def attach_interrupt(self, callback, edge, frequency=100):
        """
        :param callback: Target function
        :param edge: Interruption edge (FALLING, RISING, BOTH)
        :param frequency: Pin value polling frequency in ms
        """
        if self.mode == OUTPUT:
            raise(self.InvalidOperation("Pin is set as OUTPUT, not INPUT!"))
        class Interrupt(object):
            def __init__(self, pin, callback, edge, frequency):
                """
                :param pin: Pin object
                :param callback: Target function
                :param edge: Interruption edge (FALLING, RISING, BOTH)
                :param frequency: Pin value polling frequency in ms
                """
                self.pin = pin
                self.callback = callback #TODO soporte a parametros en funcion callback
                self.edge = edge
                if self.edge not in (RISING, FALLING, BOTH):
                    raise(ValueError("Edge must be RISING, FALLING or BOTH"))
                self.frequency = frequency #Freq in ms
                self.sleep_value = frequency/1000.0 #Freq in seconds (used by time.sleep)
            def start(self):
                self.thread = threading.Thread(target=self.thread_f)
                self.thread.daemon = True
                self.thread.start()
            def thread_f(self):
                before = self.pin.read() #Get initial value
                sleep(self.sleep_value)
                while True:
                    now = self.pin.read()
                    #if (self.edge = RISING and (not before and now)) or (self.edge = FALLING and (before and not now)) or (self.edge = BOTH and (before != now)):
                    #TODO conseguir usar el if
                    trigger = False
                    trigger = bool(self.edge == RISING and bool(not before and now))
                    trigger = bool(self.edge == FALLING and bool(before and not now))
                    trigger = bool(self.edge == BOTH and bool(before != now))
                    if trigger:
                        before = now
                        self.callback()
                    sleep(self.sleep_value)
        return Interrupt(self, callback, edge, frequency)
    class WrongInput(Exception):
        pass
    class InvalidOperation(Exception):
        pass
