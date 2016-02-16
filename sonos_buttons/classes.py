import parameters as params
#import RPi.GPIO as GPIO
import time

#GPIO.setmode(GPIO.BOARD)

class ButtonList(list):

    def __init__(self):        
        pass

    # Add a new button to this list of buttons, but also
    # return the new button, so we can capture a handle to it
    # in the calling module.

    def add(self, name, pin_number):
        item_count = len(self)
        button = Button(name, pin_number, 2**item_count)
        self.append(button)
        return button

    def get_pressed_buttons(self):
        '''Return the mask sum for all currently pressed buttons'''
        
        return sum([button.mask for button in self if button.is_pressed()])

    def get_button_event(self):
        '''Returns None if no buttons are pressed, or returns a ButtonEvent if buttons are pressed'''

        initial_buttons = self.get_pressed_buttons()
        if initial_buttons:

            start_time = time.time()

            while True:

                current_buttons = self.get_pressed_buttons()
                if initial_buttons > current_buttons:
                    # buttons were released, so return the event
                    return ButtonEvent(initial_buttons, duration)
                elif initial_buttons < current_buttons:
                    # more buttons pressed, so start again
                    return self.get_button_event()
                duration = time.time() - start_time
                if duration > params.MAX_PRESS_DURATION:
                    # max duration exceeded, so return the event
                    return ButtonEvent(initial_buttons, duration)

        else:

            return None

class Button():

    def __init__(self, name, pin_number, mask):
        self.name = name
        self.pin_number = pin_number
        self.mask = mask
        #GPIO.setup(self.pin_number, GPIO.IN)

    def is_pressed(self):
        '''Return True if button is currently pressed'''

        #return GPIO.input(self.pin_number)
        
        #Debugging stuff
        if self.pin_number in [17]:
            return True
        else:
            return False

    # Note that these magic functions allow us to use
    # the button's 'mask' value for == tests and + operations.

    def __eq__(self, other):
        if isinstance(other, Button):
            return (self.mask==other.mask)
        return (self.mask==other)

    def __add__(self, other):
        if isinstance(other, Button):
            return (self.mask + other.mask)
        else:
            return (self.mask + other)

    def __radd__(self, other):
        return self.__add__(other)

class ButtonEvent():

    def __init__(self, buttons, duration):
        self.buttons = buttons
        self.duration = duration

    def is_long_press(self):
        '''Return True if the button press duration was longer than the LONG_PRESS_DURATION'''

        return (self.duration > params.LONG_PRESS_DURATION)

    def is_button_pressed(self, button):
        '''Return True if the event included this button''' 

        return bool(self.buttons & button.mask)

class LEDList(list):

    def __init__(self):
        pass

    def add(self, name, pin_number):
        led = LED(name, pin_number)
        self.append(led)
        return led

class LED():

    def __init__(self, name, pin_number):
        self.name = name
        self.pin_number = pin_number
        self._is_on = False
        #GPIO.setup(self.pin_number, GPIO.OUT)
    
    def turn_on(self):
        #GPIO.output(self.pin_number,True)
        self._is_on = True
    
    def turn_off(self):
        #GPIO.output(self.pin_number, False)
        self._is_on = False

    def is_on(self):
        return self._is_on

    def flash(self, count=2, gap=0.1):
        if self.is_on():
            self.turn_off

        for i in range(0, count):
            self.turn_on()
            time.sleep(gap)
            self.turn_off()
            time.sleep(gap)