import os
import sys
import inspect
import time
from imports import *


CURRENT_CIRCLE_ID = None
CONNECTED = False


def new_iterm_pane():
    global keyboard
    keyboard.press(Key.cmd)
    keyboard.press(Key.shift)
    keyboard.press('d')
    keyboard.release('d')
    keyboard.release(Key.shift)
    keyboard.release(Key.cmd)


def next_iterm_pane():
    global keyboard
    keyboard.press(Key.cmd)
    keyboard.press(']')
    keyboard.release(']')
    keyboard.release(Key.cmd)
    time.sleep(0.25)


class CircleListener(Leap.Listener):

    def __print_frame_info__(self, f):
        print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            f.id, f.timestamp, len(f.hands), len(f.fingers)))

    def on_connect(self, controller):
        CONNECTED = True
        print("Connected to the Leap Motion sensor.")

    def on_frame(self, controller):
        global keyboard
        global CURRENT_CIRCLE_ID
        frame = controller.frame()
        prev_frame = controller.frame(1)
        # self.__print_frame_info__(frame)
        gestures = frame.gestures()
        for gesture in gestures:
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gesture)
                state = circle.state
                if state == Leap.Gesture.STATE_START:
                    CURRENT_CIRCLE_ID = circle.id
                    print('Started circle gesture.')
                if state == Leap.Gesture.STATE_STOP:

                    next_iterm_pane()
                    time.sleep(1.5)

                    # keyboard.type('ssh lpn@uat.mit.edu')
                    keyboard.type('echo succesfully triggered an echo command based on a circular gesture.')
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)
                    time.sleep(0.25)

                    next_iterm_pane()

                    print('Circle gesture #%d completed.'
                          % CURRENT_CIRCLE_ID)


def main():

    # Set up the Leap Motion sensor.
    listener = CircleListener()
    controller = Leap.Controller()
    controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)

    '''
    UNCOMMENT TO SET CIRCLE GESTURE PARAMETERS.
    # controller.config.set("Gesture.Circle.MinRadius", 10.0)
    # controller.config.set("Gesture.Circle.MinArc", .5)
    '''
    
    controller.config.save()
    # Have the listener receive events from the controller.
    controller.add_listener(listener)

    # Set up the pynput controller.
    global keyboard
    keyboard = Keyboard.Controller()

    # Wait for the Leap Motion sensor to come online.
    while not CONNECTED:
        time.sleep(2)

    # Keep this process running until Enter is pressed
    print('Note that gesture IDs may not be incremental.')
    print('TODO: Fix keypress generation to support uppercase letters and special characters.')
    print("Running now, press Enter to quit at any time...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
