import cv2
import logging
import numpy as np
import VisionConfiguration

'''
This module is for Processing the image into an image that we can calculate where the target is.
'''

logger = logging.getLogger('VisionProcessor')

BIGGEST_HULL_COLOR = (0, 0, 255)
OTHER_HULL_COLOR = (255, 255, 255)

class VisionProcessor:
    """
    This is used to process the image to bring out the target clearly
    """
    def __init__(self, config=None):
        if config is None:
            config = VisionConfiguration.VisionConfiguration('settings.conf')

        self.config = config

    def process_frame(self, frame, config=None, copy=False):
        """
        Processes the image given to bring out just the target
        :param frame: The image to process
        :param config: The config file to use, if need to change
        :param copy: If we should copy the frame before processing
        :return: The processed image
        """
        image = frame
        if copy:
            image = frame.copy()

        if config is not None:
            self.config = config

        smooth_image = self.__smooth(image)
        range_image = self.__threshold(smooth_image)

        return range_image

    def hull_frame(self, frame, config=None, draw_all_hulls=True, copy=False):
        """
        Make the frame come together, right now, over me. (Open Morph -> Close Morph -> Fill Contour hulls)
        :param frame: The frame to convex hull
        :param config: The config file to use, if not specified, then it will use the one last given
        :param copy: If the frame should be copied
        :param draw_all_hulls: Should we draw all of the hulls
        :return: The image, The biggest hull
        """
        image = frame
        if copy:
            image = frame.copy()

        if config is not None:
            self.config = config

        # Perform operations to clean up image
        open_image = self.__open(image)
        close_image = self.__close(open_image)
        crap, contours, h = cv2.findContours(close_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get size of image and create blacks
        width, height = close_image.shape
        hull_image = np.zeros((width, height, 3), dtype=np.uint8)

        # Create the hulls of the image and get the biggest hull
        biggest_hull = None
        for c in contours:
            hull = cv2.convexHull(c)

            if biggest_hull is None or cv2.contourArea(biggest_hull) < cv2.contourArea(hull):
                # Set the largest hull
                biggest_hull = hull

            if draw_all_hulls:
                # Draw the hull if we want all of the hulls
                hull_image = cv2.drawContours(hull_image, [hull], -1, OTHER_HULL_COLOR, -1)

        # Draw the largest hull if we aren't drawing all of the hulls and it isn't None
        if biggest_hull is not None:
            hull_image = cv2.drawContours(hull_image, [biggest_hull], -1, BIGGEST_HULL_COLOR, -1)

        return hull_image, biggest_hull

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

    def __threshold(self, image):
        # If we should use HSV, convert it here
        if self.config.get_should_use_hsv():
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # For now just use a color range
        range_image = cv2.inRange(image, self.config.get_low_range(), self.config.get_high_range())
        return range_image

    def __smooth(self, image):
        if not self.config.get_should_smooth():
            return image

        # Only smooth image if needed
        smooth_image = cv2.bilateralFilter(image, self.config.get_kernel_size_smooth(), 150, 150)
        return smooth_image
