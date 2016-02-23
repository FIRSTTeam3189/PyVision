import cv2
import logging
import numpy as np
import VisionConfiguration

'''
This module is for Processing the image into an image that we can calculate where the target is.
'''

logger = logging.getLogger('VisionProcessor')

class VisionProcessor:
    """
    This is used to process the image to bring out the target clearly
    """
    def __init__(self, config=None):
        if config is None:
            config = VisionConfiguration.VisionConfiguration('settings.conf')

        self.config = config

    def process_frame(self, image, config=None):
        """
        Processes the image given to bring out just the target
        :param image: The image to process
        :param config: The config file to use, if need to change
        :return: The processed image
        """
        if config is not None:
            self.config = config

        return self.__threshold(image)

    def __threshold(self, image):
        # If we should use HSV, convert it here
        if self.config.get_should_use_hsv():
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        logger.debug('Threshold Image')

        # For now just use a color range
        range_image = cv2.inRange(image, self.config.get_low_range(), self.config.get_high_range())
        return range_image

    def __smooth(self, image):
        pass

    def __remove_noise(self, image):
        pass
