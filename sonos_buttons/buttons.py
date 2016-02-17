# import modules
import RPi.GPIO as GPIO
import parameters as params

GPIO.setmode(GPIO.BOARD) # Use board pin numbering

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

class Button():

    def __init__(self, name, pin_number, mask):
        self.name = name
        self.pin_number = pin_number
        self.mask = mask
        self.gpio_link()
        
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
    
    #link code button to physical gpio pin
    def gpio_link(self):
        GPIO.setup(self.pin_number, GPIO.IN)
    
    #gives status of button in real world.
    def status(self):
        if GPIO.input(self.pin_number):#i.e. if closed
            return "CLOSED"
        else:
            return "OPEN"
            

class ButtonEvent():

    def __init__(self, buttons, duration):
        self.buttons = buttons
        self.duration = duration

    def is_long_press(self):
        if self.duration > params.LONG_PRESS_DURATION:
            return True
        else:
            return False

    #Witchcraft
    def is_button_pressed(self, button):
        return bool(self.buttons & button.mask)