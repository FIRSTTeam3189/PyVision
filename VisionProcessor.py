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

        smooth_image = self.__smooth(image)
        range_image = self.__threshold(smooth_image)
        open_image = self.__open(range_image)
        close_image = self.__close(open_image)

        return close_image

    def convex_hull_image(self, image):
        contour_image, contours, hirarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        hull_image = contour_image
        for (i, c) in enumerate(contours):
            hull = cv2.convexHull(c)
            hull_image = cv2.drawContours(hull_image, hull, -1, (255, 255, 255), -1)

        return hull_image

    def __threshold(self, image):
        # If we should use HSV, convert it here
        if self.config.get_should_use_hsv():
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        logger.debug('Threshold Image')

        # For now just use a color range
        range_image = cv2.inRange(image, self.config.get_low_range(), self.config.get_high_range())
        return range_image

    def __smooth(self, image):
        if not self.config.get_should_smooth():
            return image

        # Only smooth image if needed
        smooth_image = cv2.bilateralFilter(image, self.config.get_kernel_size_smooth(), 150, 150)
        return smooth_image

    def __open(self, image):
        if not self.config.get_should_open():
            return image

        # Only open image if needed
        open_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, self.config.get_kernel_open())
        return open_image

    def __close(self, image):
        if not self.config.get_should_close():
            return image

        # Only close image if needed
        close_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, self.config.get_kernel_close())
        return close_image
