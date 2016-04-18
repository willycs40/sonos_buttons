#!/usr/bin/python

from classes import *
import parameters as params
from sonosmemorycontroller import SonosMemoryController
import time
import logging
import RPi.GPIO as GPIO

# Set up the buttons. Make a button set and add buttons,
# retaining handles to each one, for use later.
buttons = ButtonList()
BTN_1 = buttons.add('Button 1', 11)
BTN_2 = buttons.add('Button 2', 13)
BTN_3 = buttons.add('Button 3', 15)
BTN_4 = buttons.add('Button 4', 12)
BTN_5 = buttons.add('Button 5', 22)
BTN_6 = buttons.add('Button 6', 18)


leds = LEDList()
LED_1 = leds.add('LED Left', 40)
#LED_2 = leds.add('LED Right', 16)

smc = SonosMemoryController()

def monitor_buttons():

    while True:

        button_event = buttons.get_button_event()
        if button_event:

            logging.info("Button press detected.")

            trigger_action(button_event)

            # don't resume looping until all 
            # buttons are released
            while buttons.get_pressed_buttons():
                time.sleep(0.1)

def trigger_action(button_event):

    # This is why we kept handles to the buttons earlier.
    # You can compare  pressed_buttons to the buttons, or 
    # sets of buttons. This will do bitwise matching against the buttons'
    # mask values.

    # in case the smc still has a thread running from earlier, cancel it
    #smc.cancel_running_thread()

    # check for playlist button short and long presses
    playlist_buttons = [BTN_1, BTN_2, BTN_3, BTN_4, BTN_5, BTN_6]
    for playlist_button in playlist_buttons:
        if button_event.buttons == playlist_button:
            logging.info('Button ({}) pressed for {} seconds. Long press: {}'.format(playlist_button.name, button_event.duration, str(button_event.is_long_press())))
            if button_event.is_long_press():
                logging.info('Saving current queue to playlist ({})'.format(playlist_button.name))
                LED_1.flash(2,0.1)
                try:
                    smc.save_playlist(playlist_button.name)
                except:
                    LED_1.flash(3,0.1)
            else:
                logging.info('Loading playlist ({})'.format(playlist_button.name))
                LED_1.flash(1,0.3)
                try:
                    smc.load_playlist(playlist_button.name)
                except:
                    LED_1.flash(3, 0.1)


    #if button_event.buttons == BTN_1 + BTN_2:
    #    logging.info('Buttons 1 and 2 pressed for {} seconds. Long press: {}'.format(button_event.duration, str(button_event.is_long_press())))

if __name__=='__main__':

    logging.basicConfig(
        format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=logging.INFO)

    monitor_buttons()
