import cv2
from threading import Thread
import time
import struct

class SingleFrameGrabber:
    def __init__(self, file_path):
        self.frame = cv2.imread(file_path)
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def read(self):
        """
        Reads a frame from the frame grabber
        """
        return self.frame

    def update(self):
        while True:
            if self.stopped:
                break

            time.sleep(.1)

    def stop(self):
        self.stopped = True