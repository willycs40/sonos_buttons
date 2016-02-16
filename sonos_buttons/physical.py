#created nick howard 13.02.15
#controls physical hardware connected to gpio pins

#import python modulus
import time

#impot other modulus
import ledcontrol
import butcontrol

#ALL PIN NUMBERS ARE BOARD PIN NUMBERS

#~~~~~~~~~~~~ LED SETUP ~~~~~~~~~~
#define led pins
#led1_pin = 3 #aka GPIO2

#create led objects
#led1 = ledcontrol.led(led1_pin)


#~~~~~~~~~~~~ BUTTON SETUP ~~~~~~~~~~
#define button pins
but1_pin = 11 
but2_pin = 13

#create button objects
but1 = butcontrol.but(but1_pin)
but2 = butcontrol.but(but2_pin)

#led2 = ledcontrol.led(but1_pin)
#led2.turn_on()
#time.sleep(10)
#led2.turn_off()

count = 0
while count < 10:
    but1.get_button_status()
    print ("B1",but1.status)
    but2.get_button_status()
    print ("B2",but2.status)

    time.sleep(0.1)
    count += 0.1