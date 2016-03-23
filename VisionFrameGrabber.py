import cv2
import logging
import os
import numpy as np
from threading import Thread
from VisionConfiguration import VisionConfiguration

logger = logging.getLogger('VisionFrameGrabber')

READ_FAILS_TIL_SHUTDOWN = 5

def get_start_point(directory=None):
    if directory is None:
        directory = '.'

    files = [os.path.splitext(f)[0] for f in os.listdir(directory) if
             os.path.isfile(f) and os.path.splitext(f)[1] == '.jpg']
    numbers = []

    # Grab the numbers from the .jpg
    for f in files:
        words = f.split()
        try:
            numbers.append(int(words[len(words) - 1]))
        except ValueError:
            logger.log('Invalid conversion')

    return 0 if len(numbers) == 0 else max(numbers) + 1


class VisionFrameGrabber:
    '''
    This is for grabbing frames in a separate thread
    '''

    def __init__(self, src=0, save_frames=0):
        self.stopped = False
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, frame) = self.stream.read()
        self.frame = cv2.flip(frame, 0)
        self.should_save_frames = False
        self.current_frame = 0
        self.start_frame = 0
        self.read_fails = 0

        if save_frames > 0:
            self.start_frame = get_start_point()
            self.should_save_frames = True
            self.save_frames = save_frames + self.start_frame

    def start(self):
        '''
        This starts the frame grabber process
        '''
        Thread(target=self.update, args=()).start()
        return self

    def read(self):
        '''
        This grabs the latest frame from the frame grabber
        '''
        return self.frame

    def update(self):
        '''
        This is called to update the frame grabber
        '''
        while True:
            if self.stopped:
                break

            (self.grabbed, self.frame) = self.stream.read()

            # Keep track if we are actually reading frames, and if not, shutdown after
            # Five failed reads
            if not self.grabbed:
                self.read_fails += 1
            else:
                self.read_fails = 0

            if self.read_fails > READ_FAILS_TIL_SHUTDOWN:
                self.stop()

            # See if we should save frames
            if self.should_save_frames:
                # Save those frames until a certain point
                path = 'image %d%s' % (self.current_frame, '.jpg')
                cv2.imwrite(path, self.frame)

                self.current_frame += 1

                if self.current_frame > self.save_frames:
                    self.current_frame = self.save_frames
                    temp = self.save_frames
                    self.save_frames += self.save_frames - self.start_frame
                    self.start_frame = temp
                    self.should_save_frames = False

        self.stream.release()

    def stop(self):
        '''
        This stops the frame grabber
        '''
        self.stopped = True
