from GRTPy3 import GRT
from LeapSDKPy3 import Leap

import argparse
import ctypes
import numpy as np
import sys

'''
Implementation plan:
CLI for user to do a gesture and save it to some command.
Script saves training data to a file and trains GRT in the background.
Deletes file when complete, but maybe users should be able to see what they have stored.
Add parsing options to see what you have stored.

for tracking user movement:
only start recording frames once 1 hand is detected
stop and save as training data when no hands detected (finished)
'''
class GestureListener(Leap.Listener):

    def __get_image_info__(self, i):
        return i.width, i.height, i.bytes_per_pixel

    def __get_num_points__(self, i):
        w, h, b = self.__get_image_info__(i)
        return w * h * b

    def __print_frame_info__(self, f):
        print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
            f.id, f.timestamp, len(f.hands), len(f.fingers)))

    def on_connect(self, controller):
        # CONNECTED = True
        print("Connected to the Leap Motion sensor.")
        self.gesture_in_progress = False
        self.frames = []
        self.cur_gest = []

    def begin_macro(self):
        self.gesture_in_progress = True

    def on_frame(self, controller):
 
        frame = controller.frame()

        if frame.hands.is_empty and self.gesture_in_progress:
            self.gesture_in_progress = False
            self.frames.append(cur_gest)
        # Only work with data if we detect a hand in the frame.
        if len(frame.hands) != 1:
            return
        if not self.gesture_in_progress:
            self.begin_macro()

        images = frame.images
        # For now, let's just work with one image from stereo.
        image = images[1]
        image_data = image.data
        num_points = self.__get_num_points__(image)
        frame_data = []
        for i in range(num_points):
            frame_data.append(image_data[i])
        frame_data = np.array(frame_data)
        if self.gesture_in_progress:
            self.cur_gest.append(frame_data)


'''
PARSING SECTION
parser = argparse.ArgumentParser(description='.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='interger list')
parser.add_argument('--sum', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
args = parser.parse_args()
'''

def main():

    # Set up the Leap Motion sensor.
    listener = GestureListener()
    controller = Leap.Controller()
    # Have the listener receive events from the controller.
    controller.add_listener(listener)
    # MUST allow frames and images or no data will be received.
    # https://developer-archive.leapmotion.com/documentation/python/api/Leap.Controller.html#Leap.Controller.set_policy
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    controller.config.save()

    commands = {}
    while True:
        train = input('Would you like to train a new gestural macro?')
        if 'y' in train or 'yes' in train or 'Yes' in train or 'Y' in train:
            cmd = input('Please enter the command you would like to train:\n > ')
            commands[cmd] = [] # Set up the data frames for the command.
            print('We will have you train the system three times.')

        else:
            break
    # Remove the sample listener when done.
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()



