#created nick howard 13.02.15
#allows control of buttons attached to gpio pins

# import modules
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) # Use board pin numbering

# Button class
class but:
    def __init__(self, pin):
        self.pin = pin
        self.status = "OPEN"
        GPIO.setup(self.pin, GPIO.IN) # set designated pin to input
    
    def get_button_status(self):
        if GPIO.input(self.pin):
            self.status = "CLOSED"
        else:
            self.status = "OPEN"
        return self.status
        