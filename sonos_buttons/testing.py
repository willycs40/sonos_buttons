from buttons import *
import parameters as params
import time

# Set up the buttons. Make a button set and add buttons,
# retaining handles to each one, for use later.
button_set = Buttons()
BTN_1 = button_set.add('Button 1', 7)
BTN_2 = button_set.add('Button 2', 13)
BTN_3 = button_set.add('Button 3', 17)
BTN_4 = button_set.add('Button 4', 21)
BTN_5 = button_set.add('Button 5', 24)
BTN_6 = button_set.add('Button 6', 29)

def get_pressed_buttons():

    pressed_buttons = 0

    for button in button_set:
        if gpio_test_pin(button.pin_number):
            pressed_buttons += button

    return pressed_buttons

def gpio_test_pin(pin_number):
    #raise NotImplementedError("Nick to implement this")
    if pin_number == 17:
        return True
    else:
        return False

def monitor_buttons():

    while True:

        button_event = get_button_event()
        if button_event:

            trigger_action(button_event)

            # don't resume looping until all 
            # buttons are released
            while get_pressed_buttons():
                pass

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

    if button_event.buttons == BTN_3:
        print('Button 3 pressed for {} seconds'.format(duration))
    elif button_event.buttons == BTN_4 + BTN_6:
        print('Buttons 4 and 6 pressed for {} seconds'.format(duration))

def main():
    monitor_buttons()

