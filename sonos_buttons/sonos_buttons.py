from classes import *
import parameters as params
from sonosmemorycontroller import SonosMemoryController
import time
import logging

# Set up the buttons. Make a button set and add buttons,
# retaining handles to each one, for use later.
buttons = ButtonList()
BTN_1 = buttons.add('Button 1', 11)
BTN_2 = buttons.add('Button 2', 13)

#leds = LEDList()
#LED_1 = leds.add('LED Left', 14)
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
    smc.cancel_running_thread()

    # check for playlist button short and long presses
    playlist_buttons = [BTN_1, BTN_2]
    for playlist_button in playlist_buttons:
        if button_event.buttons == playlist_button:
            if button_event.is_long_press():
                logging.info('Saving station current queue to playlist ({})'.format(button.name))
                smc.save_playlist(playlist_button.name)
            else:
                smc.load_playlist_threaded(playlist_button.name)

    if button_event.buttons == BTN_4 + BTN_6:
        print('Buttons 4 and 6 pressed for {} seconds'.format(button_event.duration))
    else:
        print('Unknown button combination held for {} seconds.'.format(button_event.duration))
        for button in buttons:
            print('Button: {}. Pressed: {}.'.format(button.name, button_event.is_button_pressed(button)))

if __name__=='__main__':

    logging.basicConfig(
        format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=logging.INFO)

    monitor_buttons()
