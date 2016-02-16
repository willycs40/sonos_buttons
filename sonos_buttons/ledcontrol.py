#created nick howard 13.02.15
#allows control of leds attached to gpio pins

# import modules
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) # Use board pin numbering

# LED class
class led:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT) # set designated pin to OUT
    
    #function to turn led on
    def turn_on(self):
        GPIO.output(self.pin,True) 
    
    #function to turn led off
    def turn_off(self):
        GPIO.output(self.pin, False)

        
    