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
from pykeyboard import PyKeyboard
from pymouse import PyMouse
from pynput import keyboard as Keyboard
from pynput.keyboard import Key


SWIPE_COMMAND = 'ssh lpn@uat.mit.edu'
CIRCLE_COMMAND = 'neofetch'


def macOS_alert(message):
    os.system("""
        osascript -e 'display notification "%s" with title "%s"'
        """ % (message, 'GesTerm'))


args = sys.argv
if len(args) >= 3:
    if args[1] == 'circle':
        CIRCLE_COMMAND = args[2]
        macOS_alert('You just set your circle command to: %s.' % args[2])
    if args[1] == 'swipe':
        SWIPE_COMMAND = args[2]
        macOS_alert('You just set your swipe command to: %s.' % args[2])
    if len(args) == 5:
        if args[3] == 'swipe':
            SWIPE_COMMAND = args[4]
            macOS_alert('You just set your swipe command to: %s.' % args[4])
        if args[3] == 'circle':
            CIRCLE_COMMAND = args[4]
            macOS_alert('You just set your circle command to: %s.' % args[4])


class GesTermListener(Leap.Listener):

    def on_exit(self, controller):
        print('Exited Leap Motion.')

    def on_disconnect(self, controller):
        print('Disconnected from Leap Motion controller.')


class Listener(GesTermListener):

    def __print_frame_info__(self, f):
        print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            f.id, f.timestamp, len(f.hands), len(f.fingers)))

    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)

        # Variable settings for thresholds.
        controller.config.set("Gesture.Circle.MinRadius", 50.0)
        controller.config.set("Gesture.Circle.MinArc", 0.8 * 3.14)
        controller.config.save()

        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

        # Variable settings for thresholds.
        controller.config.set("Gesture.Swipe.MinLength", 200.0)
        controller.config.set("Gesture.Swipe.MinVelocity", 200)
        controller.config.save()
        print("Connected to the Leap Motion sensor.")

        self.circle = False
        self.swipe = False

    def on_frame(self, controller):
        global keyboard
        global CURRENT_CIRCLE_ID
        frame = controller.frame()
        prev_frame = controller.frame(1)
        gestures = frame.gestures()
        for gesture in gestures:
            # CIRCLE
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                if self.swipe:
                    return
                self.circle = True
                circle = Leap.CircleGesture(gesture)
                state = circle.state
                if state == Leap.Gesture.STATE_START:
                    macOS_alert('Started circle gesture.')
                if state == Leap.Gesture.STATE_STOP:
                    macOS_alert('Circle gesture completed.')
                    time.sleep(0.3)
                    k.type_string(CIRCLE_COMMAND)
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)
                    self.circle = False
            # SWIPE
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                if self.circle:
                    return
                self.swipe = True
                swipe = Leap.SwipeGesture(gesture)
                state = swipe.state
                if state == Leap.Gesture.STATE_START:
                    macOS_alert('Started swipe gesture.')
                if state == Leap.Gesture.STATE_STOP:
                    macOS_alert('Swipe gesture in direction %s completed.' %
                          swipe.direction)
                    time.sleep(0.3)
                    k.type_string(SWIPE_COMMAND)
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)
                    self.swipe = False


def main():

    # Set up the Leap Motion sensor.
    listener = Listener()
    controller = Leap.Controller()
    # Allow background data collection.
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(Leap.Controller.POLICY_IMAGES)

    # controller.config.save()
    # Have the listener receive events from the controller.
    controller.add_listener(listener)

    controller.config.save()

    # Set up the pynput controller.
    global keyboard
    keyboard = Keyboard.Controller()
    global k
    k = PyKeyboard()

    while True:
        time.sleep(100)


if __name__ == "__main__":
    main()
