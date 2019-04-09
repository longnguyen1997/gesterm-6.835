import os, sys, inspect, time
from Leap import *
import Leap

class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print("Connected")

    def on_frame(self, controller):
        print("Frame available")

def main():
	controller = Leap.Controller()

	# Keep this process running until Enter is pressed
	print("Press Enter to quit...")
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
    main()
