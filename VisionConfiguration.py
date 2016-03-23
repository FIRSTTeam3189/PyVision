import ConfigParser as cP
import numpy as np
import logging

"""
This Module is for retrieving and setting the configuration of the vision processing
module of the Raspberry Pi Vision System
"""

# Keys for Threshold section
THRESHOLD_SECTION = "color_ranges"
THREE_LOW_KEY = "three_low"
THREE_HIGH_KEY = "three_high"
TWO_LOW_KEY = "two_low"
TWO_HIGH_KEY = "two_high"
ONE_LOW_KEY = "one_low"
ONE_HIGH_KEY = "one_high"

# Keys for Processing section
PROCESSING_SECTION = "processing"
SHOULD_CLOSE_KEY = "should_close"
SHOULD_OPEN_KEY = "should_open"
SHOULD_USE_HSV_KEY = "should_use_hsv"
SHOULD_SMOOTH_KEY = "use_smooth"
OPEN_KERNEL_KEY = "open_kernel_size"
CLOSE_KERNEL_KEY = "close_kernel_size"
SMOOTH_KERNEL_KEY = "smooth_kernel_size"

# Range values for color range
MIN_COLOR_VALUE = 0
MAX_COLOR_VALUE = 255

# Range values for kernel size
MIN_KERNEL_VALUE = 1
MAX_KERNEL_VALUE = 100

# Default values for Processing variables
DEFAULT_CLOSE_VALUE = 50
DEFAULT_OPEN_VALUE = 5
DEFAULT_FILTER_VALUE = 2

# Logger variable
logger = logging.getLogger("VisionConfiguration")


def clamp(x, low, high, debug_with=None):
    """
    Clamps a value between low and high
    :param x: Value to clamp
    :param low: Low value
    :param high: High Value
    :param debug_with: If specified it will debug with the given version
    :return: The clamped value
    """
    if x < low:
        x = low

        if debug_with is not None:
            logger.debug("%s hit low", debug_with)
    elif x > high:
        x = high

        if debug_with is not None:
            logger.debug("%s hit high", debug_with)

    return x


# noinspection PyAttributeOutsideInit
class VisionConfiguration:
    """
    This class is for the configuration of the vision system of the Raspberry Pi
    """

    def __init__(self, file_location):
        # Configuration file loading
        self.__config = cP.RawConfigParser()
        self.__config.read(file_location)
        self.__sync()
        self.__default_location = file_location

    def set_one_low(self, one):
        """
        Sets the blue/hue low value of the configuration
        :param one: The new blue/hue value
        """
        if one > self.__one_high:
            one = self.__one_high

        self.__one_low = one

    def set_one_high(self, one):
        """
        Sets the blue/hue high value of the configuration
        :param one: The new blue/hue value
        """
        if one < self.__one_low:
            one = self.__one_low

        self.__one_high = one

    def set_two_low(self, two):
        """
        Sets the green/saturation low value of the configuration
        :param two: The new green/saturation value
        """
        if two > self.__two_high:
            two = self.__two_high

        self.__two_low = two

    def set_two_high(self, two):
        """
        Sets the green/saturation high value of the configuration
        :param two: The new green/saturation value
        """
        if two < self.__two_low:
            two = self.__two_low

        self.__two_high = two

    def set_three_low(self, three):
        """
        Sets the red/value low value of the configuration
        :param three: The new red/value value
        """
        if three > self.__three_high:
            three = self.__three_high

        self.__three_low = three

    def set_three_high(self, three):
        """
        Sets the red/value high value of the configuration
        :param three: The new red/value value
        """
        if three < self.__three_low:
            three = self.__three_low

        self.__three_high = three

    def set_kernel_close_size(self, size):
        """
        Sets the kernel close size
        :param size: The size of the kernel size close
        """
        self.__kernel_size_close = size

    def set_kernel_open_size(self, size):
        """
        Sets the kernel open size
        :param size: The size of the kernel size open
        """
        self.__kernel_size_open = size

    def set_kernel_smoothing_size(self, size):
        """
        Sets the kernel smoothing size
        :param size: The size of the kernel size smooth
        """
        self.__kernel_size_smooth = size

    def set_should_close(self, should_close):
        """
        Sets if the vision should run the morphology close operation after open
        :param should_close: To close the threshold
        """
        self.__should_close = should_close

    def set_should_open(self, should_open):
        """
        Sets if the vision should run the morphology open operation
        :param should_open: To close the threshold
        """
        self.__should_open = should_open

    def set_should_use_hsv(self, should_use_hsv):
        """
        Sets if the vision should use HSV Ranges instead of RGB
        :param should_use_hsv: Use HSV Ranges
        """
        self.__should_use_hsv = should_use_hsv

    def set_should_use_smoothing(self, should_smooth):
        """
        Sets if the vision should use smoothing
        :param should_smooth: If the vision should smooth
        """
        self.__should_use_smoothing = should_smooth

    def get_low_range(self):
        """
        Gets the value of the low range as a numpy array of uint8
        :return: The numpy array for the low values
        """
        return np.array([self.__one_low, self.__two_low, self.__three_low], dtype=np.uint8)

    def get_high_range(self):
        """
        Gets the value of the high range as a numpy array of uint8
        :return: The numpy array for the high values
        """
        return np.array([self.__one_high, self.__two_high, self.__three_high], dtype=np.uint8)

    def get_kernel_close(self):
        """
        Gets the value of the kernel size as a numpy matrix of 1's of the kernel size by kernel size
        :return: The numpy matrix of the kernel
        """
        return np.ones((self.__kernel_size_close, self.__kernel_size_close), dtype=np.uint8)

    def get_kernel_size_close(self):
        """
        Gets the size of the close kernel
        :return: The size
        """
        return self.__kernel_size_close

    def get_kernel_open(self):
        """
        Gets the value of the kernel size as a numpy matrix of 1's of the kernel size by the kernel size
        :return: The numpy matrix of the kernel
        """
        return np.ones((self.__kernel_size_open, self.__kernel_size_open), dtype=np.uint8)

    def get_kernel_size_open(self):
        """
        Gets the size of the open kernel
        :return: The size
        """
        return self.__kernel_size_open

    def get_kernel_smooth(self):
        """
        Gets the value of the kernel size as a numpy matrix of 1's of the kernel size by the kernel size
        :return: The numpy matrix of the smoothing kernel
        """
        return np.ones((self.__kernel_size_smooth, self.__kernel_size_smooth), dtype=np.uint8)

    def get_kernel_size_smooth(self):
        """
        Gets the size of the smoothing kernel
        :return: The size of the smoothing kernel
        """
        return self.__kernel_size_smooth

    def get_should_close(self):
        """
        Gets if the vision should run the close morphology operation after opening operation
        :return: If the vision should run the close morphology operation
        """
        return self.__should_close

    def get_should_open(self):
        """
        Gets of the vision should run the open morphology operation
        :return: If the vision should run the open morphology operation
        """
        return self.__should_open

    def get_should_use_hsv(self):
        """
        Gets if the vision should use HSV Values instead of RGB
        :return: If the vision should use hsv
        """
        return self.__should_use_hsv

    def get_should_smooth(self):
        """
        Gets if the vision should use a smoothing operation
        :return: If the vision should smooth
        """
        return self.__should_use_smoothing

    def save(self, file_location=None, validate=True):
        """
        Saves the config file to the given location, or the same file read from if not given
        :param file_location: The file location to save to
        :param validate: If we should validate the file
        """
        if file_location is None:
            file_location = self.__default_location

        if validate:
            self.validate()

        # Write the changes to the config object
        self.__sync(False)

        with open(file_location, 'wb') as config_file:
            self.__config.write(config_file)

    def validate(self):
        """
        Sets the ranges to their proper values if they aren't already
        """
        # Validate types
        if type(self.__two_low) is not int:
            self.__two_low = MIN_COLOR_VALUE
            logger.debug("Green/Saturation low not int, setting to 0")

        if type(self.__three_low) is not int:
            self.__three_low = MIN_COLOR_VALUE
            logger.debug("Red/Value low not int, setting to 0")

        if type(self.__one_low) is not int:
            self.__one_low = MIN_COLOR_VALUE
            logger.debug("Blue/Hue low not int, setting to 0")

        if type(self.__two_high) is not int:
            self.__two_high = MAX_COLOR_VALUE
            logger.debug("Green/Saturation high not int, setting to 255")

        if type(self.__three_high) is not int:
            self.__three_high = MAX_COLOR_VALUE
            logger.debug("Red/Value high not int, setting to 255")

        if type(self.__one_high) is not int:
            self.__one_high = MAX_COLOR_VALUE
            logger.debug("Blue/Hue high not int, setting to 255")

        if type(self.__kernel_size_close) is not int:
            self.__kernel_size_close = DEFAULT_CLOSE_VALUE
            logger.debug("Kernel size close not int, setting to 0")

        if type(self.__kernel_size_open) is not int:
            self.__kernel_size_open = DEFAULT_OPEN_VALUE
            logger.debug("Kernel size open not int, setting to 0")

        if type(self.__kernel_size_smooth) is not int:
            self.__kernel_size_smooth = DEFAULT_FILTER_VALUE
            logger.debug("Kernel size smooth not int, setting to 0")

        if type(self.__should_close) is not bool:
            self.__should_close = True
            logger.debug("Kernel Should Close not bool, setting to True")

        if type(self.__kernel_size_open) is not bool:
            self.__should_open = True
            logger.debug("Kernel Should Open not bool, setting to True")

        if type(self.__should_use_hsv) is not bool:
            self.__should_use_hsv = True
            logger.debug("Should use HSV not bool, setting to True")

        if type(self.__should_use_smoothing) is not bool:
            self.__should_use_smoothing = True
            logger.debug("Should use smoothing not bool, setting to True")

        # Clamp Values
        self.__two_low = clamp(self.__two_low, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Green/Saturation Low")
        self.__one_low = clamp(self.__one_low, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Blue/Hue Low")
        self.__three_low = clamp(self.__three_low, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Red/Value Low")
        self.__two_high = clamp(self.__two_high, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Green/Saturation High")
        self.__one_high = clamp(self.__one_high, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Blue/Hue High")
        self.__three_high = clamp(self.__three_high, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Red/Value High")
        self.__kernel_size_close = clamp(self.__kernel_size_close, MIN_KERNEL_VALUE, MAX_KERNEL_VALUE,
                                         "Kernel Size Close")
        self.__kernel_size_open = clamp(self.__kernel_size_open, MIN_KERNEL_VALUE, MAX_KERNEL_VALUE, "Kernel Size Open")
        self.__kernel_size_smooth = clamp(self.__kernel_size_smooth, MIN_KERNEL_VALUE, MAX_KERNEL_VALUE,
                                          "Kernel Size Smooth")

    def __add_section(self, section):
        # Try to add the section if it doesnt exit
        try:
            self.__config.add_section(section)
        except cP.DuplicateSectionError:
            pass

    def __sync(self, read_from_config=True):
        if read_from_config:
            # Get the values from the config
            self.__two_low = self.__try_get_key(THRESHOLD_SECTION, TWO_LOW_KEY, MIN_COLOR_VALUE)
            self.__two_high = self.__try_get_key(THRESHOLD_SECTION, TWO_HIGH_KEY, MAX_COLOR_VALUE)
            self.__three_low = self.__try_get_key(THRESHOLD_SECTION, THREE_LOW_KEY, MIN_COLOR_VALUE)
            self.__three_high = self.__try_get_key(THRESHOLD_SECTION, THREE_HIGH_KEY, MAX_COLOR_VALUE)
            self.__one_low = self.__try_get_key(THRESHOLD_SECTION, ONE_LOW_KEY, MIN_COLOR_VALUE)
            self.__one_high = self.__try_get_key(THRESHOLD_SECTION, ONE_HIGH_KEY, MAX_COLOR_VALUE)
            self.__kernel_size_close = self.__try_get_key(PROCESSING_SECTION, CLOSE_KERNEL_KEY, DEFAULT_CLOSE_VALUE)
            self.__kernel_size_open = self.__try_get_key(PROCESSING_SECTION, OPEN_KERNEL_KEY, DEFAULT_OPEN_VALUE)
            self.__kernel_size_smooth = self.__try_get_key(PROCESSING_SECTION, SMOOTH_KERNEL_KEY, DEFAULT_FILTER_VALUE)
            self.__should_close = self.__try_get_key(PROCESSING_SECTION, SHOULD_CLOSE_KEY, False, True)
            self.__should_open = self.__try_get_key(PROCESSING_SECTION, SHOULD_OPEN_KEY, True, True)
            self.__should_use_hsv = self.__try_get_key(PROCESSING_SECTION, SHOULD_USE_HSV_KEY, True, True)
            self.__should_use_smoothing = self.__try_get_key(PROCESSING_SECTION, SHOULD_SMOOTH_KEY, False, True)
        else:
            # Sets the values to the config
            self.__set_key(THRESHOLD_SECTION, TWO_LOW_KEY, self.__two_low)
            self.__set_key(THRESHOLD_SECTION, TWO_HIGH_KEY, self.__two_high)
            self.__set_key(THRESHOLD_SECTION, THREE_LOW_KEY, self.__three_low)
            self.__set_key(THRESHOLD_SECTION, THREE_HIGH_KEY, self.__three_high)
            self.__set_key(THRESHOLD_SECTION, ONE_LOW_KEY, self.__one_low)
            self.__set_key(THRESHOLD_SECTION, ONE_HIGH_KEY, self.__one_high)
            self.__set_key(PROCESSING_SECTION, CLOSE_KERNEL_KEY, self.__kernel_size_close)
            self.__set_key(PROCESSING_SECTION, OPEN_KERNEL_KEY, self.__kernel_size_open)
            self.__set_key(PROCESSING_SECTION, SMOOTH_KERNEL_KEY, self.__kernel_size_smooth)
            self.__set_key(PROCESSING_SECTION, SHOULD_CLOSE_KEY, self.__should_close)
            self.__set_key(PROCESSING_SECTION, SHOULD_OPEN_KEY, self.__should_open)
            self.__set_key(PROCESSING_SECTION, SHOULD_USE_HSV_KEY, self.__should_use_hsv)
            self.__set_key(PROCESSING_SECTION, SHOULD_SMOOTH_KEY, self.__should_use_smoothing)

    def __set_key(self, section, key, value):
        # Tries to add the section if needed then setting the value
        self.__add_section(section)
        self.__config.set(section, key, value)

    def __try_get_key(self, section, key, default_value=None, is_bool=False):
        try:
            if is_bool:
                return self.__config.getboolean(section, key)
            else:
                return self.__config.getint(section, key)
        except cP.NoSectionError:
            pass
        except cP.NoOptionError:
            pass

        return default_value
