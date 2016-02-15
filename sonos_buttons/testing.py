from buttons import *
import parameters as params
from sonosmemorycontroller import SonosMemoryController
import logging
import time

# Set up the buttons. Make a button set and add buttons,
# retaining handles to each one, for use later.
buttons = ButtonList()

BTN_1 = buttons.add('Button 1', 7)
BTN_2 = buttons.add('Button 2', 13)
BTN_3 = buttons.add('Button 3', 17)
BTN_4 = buttons.add('Button 4', 21)
BTN_5 = buttons.add('Button 5', 24)
BTN_6 = buttons.add('Button 6', 29)

smc = SonosMemoryController()

def get_pressed_buttons():

    return sum([button.mask for button in buttons if gpio_test_pin(button.pin_number)])

def gpio_test_pin(pin_number):
    #raise NotImplementedError("Nick to implement this")
    if pin_number in [17]:
        return True
    else:
        return False

def get_button_event():

    initial_buttons = get_pressed_buttons()
    if initial_buttons:

        start_time = time.time()

        while True:

            current_buttons = get_pressed_buttons()
            if initial_buttons > current_buttons:
                # buttons were released, so return the event
                return ButtonEvent(initial_buttons, duration)
            elif initial_buttons < current_buttons:
                # more buttons pressed, so start again
                return get_button_event()
            duration = time.time() - start_time
            if duration > params.MAX_PRESS_DURATION:
                # max duration exceeded, so return the event
                return ButtonEvent(initial_buttons, duration)

    else:

        return None


def trigger_action(button_event):

    # This is why we kept handles to the buttons earlier.
    # You can compare  pressed_buttons to the buttons, or 
    # sets of buttons. This will do bitwise matching against the buttons'
    # mask values.

    # self.current_worker.stop()
    # self.current_worker.

    smc.cancel_running_thread()

    if button_event.buttons == BTN_3:
        print('Button 3 pressed for {} seconds'.format(button_event.duration))
        
        if button_event.is_long_press():
            smc.save_playlist('Beach')
        else:
            smc.load_playlist_threaded('Beach')

    elif button_event.buttons == BTN_4 + BTN_6:
        print('Buttons 4 and 6 pressed for {} seconds'.format(button_event.duration))
    else:
        print('Unknown button combination held for {} seconds.'.format(button_event.duration))
        for button in buttons:
            print('Button: {}. Pressed: {}.'.format(button.name, button_event.is_button_pressed(button)))


def monitor_buttons():

    while True:

        button_event = get_button_event()
        if button_event:

            logging.info("Button press detected.")

            trigger_action(button_event)

            # don't resume looping until all 
            # buttons are released
            while get_pressed_buttons():
                pass

if __name__=='__main__':

    logging.basicConfig(
        format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=logging.INFO)

    monitor_buttons()
