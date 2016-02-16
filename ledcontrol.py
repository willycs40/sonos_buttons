#created nick howard 13.02.15
#designed to allow control of leds attached to gpio pins

#import modules
import RPi.GPIO as gpio

#LED class
class led:
    def __init__(self, pin):
        self.pin = pin
    
    #function to turn led on
    def turn_on(self):
        #some code
        
    