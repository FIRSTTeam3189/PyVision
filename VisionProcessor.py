import cv2
import numpy as np
import VisionConfiguration

'''
This module is for Processing the image into an image that we can calculate where the target is.
'''


class VisionProcessor:
    def __init__(self, config=None):
        if config is None:
            config = VisionConfiguration.VisionConfiguration('settings.conf')

        self.config = config

    def process_frame(self, image):
        pass

    def __threshold(self, image):
        range_image = cv2.inRange(image, self.config.get_low_range(), self.config.get_high_range())
        return range_image
