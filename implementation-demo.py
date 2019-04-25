import inspect
import os
import sys
import time

from GRTPy3 import GRT
from LeapSDKPy3 import Leap
from LeapSDKPy3.Leap import CircleGesture
from LeapSDKPy3.Leap import KeyTapGesture
from LeapSDKPy3.Leap import ScreenTapGesture
from LeapSDKPy3.Leap import SwipeGesture
from imports import *
from pykeyboard import PyKeyboard
from pymouse import PyMouse
from pynput import keyboard as Keyboard
from pynput.keyboard import Key


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


def prev_iterm_pane():
    global keyboard
    keyboard.press(Key.cmd)
    keyboard.press('[')
    keyboard.release('[')
    keyboard.release(Key.cmd)
    time.sleep(0.25)


class GesTermListener(Leap.Listener):

    def on_exit(self, controller):
        print('Exited Leap Motion.')

    def on_disconnect(self, controller):
        print('Disconnected from Leap Motion controller.')


class CircleListener(GesTermListener):

    def __print_frame_info__(self, f):
        print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            f.id, f.timestamp, len(f.hands), len(f.fingers)))

    def on_connect(self, controller):
        print("Connected to the Leap Motion sensor.")

    def on_frame(self, controller):
        global keyboard
        global CURRENT_CIRCLE_ID
        frame = controller.frame()
        prev_frame = controller.frame(1)
        gestures = frame.gestures()
        for gesture in gestures:
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gesture)
                state = circle.state
                if state == Leap.Gesture.STATE_START:
                    CURRENT_CIRCLE_ID = circle.id
                    print('Started circle gesture.')
                if state == Leap.Gesture.STATE_STOP:
                    print('Circle gesture completed.')
                    time.sleep(0.3)
                    k.type_string('ssh lpn@uat.mit.edu')
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)


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
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    controller.config.save()

    # Set up the pynput controller.
    global keyboard
    keyboard = Keyboard.Controller()
    global k
    k = PyKeyboard()

    while True:
        time.sleep(5)


if __name__ == "__main__":
    main()
