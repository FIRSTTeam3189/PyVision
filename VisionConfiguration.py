import ConfigParser as cP
import numpy as np
import logging

"""
This Module is for retrieving and setting the configuration of the vision processing
module of the Raspberry Pi Vision System
"""

# Keys for Threshold section
THRESHOLD_SECTION = "color_ranges"
RED_LOW_KEY = "red_low"
RED_HIGH_KEY = "red_high"
GREEN_LOW_KEY = "green_low"
GREEN_HIGH_KEY = "green_high"
BLUE_LOW_KEY = "blue_low"
BLUE_HIGH_KEY = "blue_high"

# Keys for Processing section
PROCESSING_SECTION = "processing"
SHOULD_CLOSE_KEY = "should_close"
SHOULD_OPEN_KEY = "should_open"
OPEN_KERNEL_KEY = "open_kernel_size"
CLOSE_KERNEL_KEY = "close_kernel_size"

# Range values for color range
MIN_COLOR_VALUE = 0
MAX_COLOR_VALUE = 255

# Range values for kernel size
MIN_KERNEL_VALUE = 1
MAX_KERNEL_VALUE = 10

# Logger variable
logger = logging.getLogger("VisionConfiguration")


def clamp(x, low, high, debug_with=None):
    """
    Clamps a value between low and high
    :param x: Value to clamp
    :param low: Low value
    :param high: High Value
    :param debugWith: If specified it will debug with the given version
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


class VisionConfiguration:
    """
    This class is for the configuration of the vision system of the Raspberry Pi
    """

    def __init__(self, file_location):
        # Config values
        self.__red_low = 0
        self.__red_high = 255
        self.__blue_low = 0
        self.__blue_high = 255
        self.__green_low = 0
        self.__green_high = 255
        self.__kernel_size_close = 1
        self.__kernel_size_open = 1
        self.__should_close = True
        self.__should_open = True

        # Configuration file loading
        self.__config = cP.RawConfigParser()
        self.__config.read(file_location)
        self.__default_location = file_location

    def set_red_low(self, red):
        """
        Sets the red low value of the configuration
        :param red: The new red value
        """
        if red > self.__red_high:
            red = self.__red_high

        self.__red_low = red

    def set_red_high(self, red):
        """
        Sets the red high value of the configuration
        :param red: The new red value
        """
        if red < self.__red_low:
            red = self.__red_low

        self.__red_high = red

    def set_green_low(self, green):
        """
        Sets the green low value of the configuration
        :param green: The new green value
        """
        if green > self.__green_high:
            green = self.__green_high

        self.__green_low = green

    def set_green_high(self, green):
        """
        Sets the green high value of the configuration
        :param green: The new green value
        """
        if green < self.__green_low:
            green = self.__green_low

        self.__green_high = green

    def set_blue_low(self, blue):
        """
        Sets the blue low value of the configuration
        :param blue: The new blue value
        """
        if blue > self.__blue_high:
            blue = self.__blue_high

        self.__blue_low = blue

    def set_blue_high(self, blue):
        """
        Sets the blue high value of the configuration
        :param blue: The new blue value
        """
        if blue < self.__blue_low:
            blue = self.__blue_low

        self.__blue_high = blue

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

    def get_low_range(self):
        """
        Gets the value of the low range as a numpy array of uint8
        :return: The numpy array for the low values
        """
        return np.array([self.__blue_low, self.__green_low, self.__red_low], dtype=np.uint8)

    def get_high_range(self):
        """
        Gets the value of the high range as a numpy array of uint8
        :return: The numpy array for the high values
        """
        return np.array([self.__blue_high, self.__green_high, self.__red_high], dtype=np.uint8)

    def get_kernel_close(self):
        """
        Gets the value of the kernel size as a numpy matrix of 1's of the kernel size by kernel size
        :return: The numpy matrix of the kernel
        """
        return np.ones((self.__kernel_size_close, self.__kernel_size_close), np.uint8)

    def get_kernel_open(self):
        """
        Gets the value of the kernel size as a numpy matrix of 1's of the kernel size by the kernel size
        :return: The numpy matrix of the kernel
        """
        return np.ones((self.__kernel_size_open, self.__kernel_size_open), np.uint8)

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

        with open(file_location, 'wb') as config_file:
            self.__config.write(config_file)

    def validate(self):
        """
        Sets the ranges to their proper values if they aren't already
        """
        # Validate types
        if type(self.__blue_low) is not int:
            self.__blue_low = MIN_COLOR_VALUE
            logger.debug("Blue low not int, setting to 0")

        if type(self.__green_low) is not int:
            self.__green_low = MIN_COLOR_VALUE
            logger.debug("Green low not int, setting to 0")

        if type(self.__red_low) is not int:
            self.__red_low = MIN_COLOR_VALUE
            logger.debug("Red low not int, setting to 0")

        if type(self.__blue_high) is not int:
            self.__blue_high = MAX_COLOR_VALUE
            logger.debug("Blue high not int, setting to 255")

        if type(self.__green_high) is not int:
            self.__green_high = MAX_COLOR_VALUE
            logger.debug("Green high not int, setting to 255")

        if type(self.__red_high) is not int:
            self.__red_high = MAX_COLOR_VALUE
            logger.debug("Red high not int, setting to 255")

        if type(self.__kernel_size_close) is not int:
            self.__kernel_size_close = MIN_KERNEL_VALUE
            logger.debug("Kernel size close not int, setting to 0")

        if type(self.__kernel_size_open) is not int:
            self.__kernel_size_open = MIN_KERNEL_VALUE
            logger.debug("Kernel size open not int, setting to 0")

        if type(self.__should_close) is not bool:
            self.__should_close = True
            logger.debug("Kernel Should Close not bool, setting to True")

        if type(self.__kernel_size_open) is not bool:
            self.__should_open = True
            logger.debug("Kernel Should Open not bool, setting to True")

        # Clamp Values
        self.__blue_low = clamp(self.__blue_low, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Blue Low")
        self.__red_low = clamp(self.__red_low, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Red Low")
        self.__green_low = clamp(self.__green_low, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Green Low")
        self.__blue_high = clamp(self.__blue_high, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Blue High")
        self.__red_high = clamp(self.__red_high, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Red High")
        self.__green_high = clamp(self.__green_high, MIN_COLOR_VALUE, MAX_COLOR_VALUE, "Green High")
        self.__kernel_size_close = clamp(self.__kernel_size_close, MIN_KERNEL_VALUE, MAX_KERNEL_VALUE,
                                         "Kernel Size Close")
        self.__kernel_size_open = clamp(self.__kernel_size_open, MIN_KERNEL_VALUE, MAX_KERNEL_VALUE, "Kernel Size Open")

    def __add_section(self, section):
        # Try to add the section if it doesnt exit
        try:
            self.__config.add_section(section)
        except cP.DuplicateSectionError:
            pass

    def __sync(self, read_from_config=True):
        if read_from_config:
            # Get the values from the config
            self.__blue_low = self.__try_get_key(THRESHOLD_SECTION, BLUE_LOW_KEY, MIN_COLOR_VALUE)
            self.__blue_high = self.__try_get_key(THRESHOLD_SECTION, BLUE_HIGH_KEY, MAX_COLOR_VALUE)
            self.__green_low = self.__try_get_key(THRESHOLD_SECTION, GREEN_LOW_KEY, MIN_COLOR_VALUE)
            self.__green_high = self.__try_get_key(THRESHOLD_SECTION, GREEN_HIGH_KEY, MAX_COLOR_VALUE)
            self.__red_low = self.__try_get_key(THRESHOLD_SECTION, RED_LOW_KEY, MIN_COLOR_VALUE)
            self.__red_high = self.__try_get_key(THRESHOLD_SECTION, RED_HIGH_KEY, MAX_COLOR_VALUE)
            self.__kernel_size_close = self.__try_get_key(PROCESSING_SECTION, CLOSE_KERNEL_KEY, MIN_KERNEL_VALUE)
            self.__kernel_size_open = self.__try_get_key(PROCESSING_SECTION, OPEN_KERNEL_KEY, MIN_KERNEL_VALUE)
            self.__should_close = self.__try_get_key(PROCESSING_SECTION, SHOULD_CLOSE_KEY, False, True)
            self.__should_open = self.__try_get_key(PROCESSING_SECTION, SHOULD_OPEN_KEY, False, True)
        else:
            # Sets the values to the config
            self.__set_key(THRESHOLD_SECTION, BLUE_LOW_KEY, self.__blue_low)
            self.__set_key(THRESHOLD_SECTION, BLUE_HIGH_KEY, self.__blue_high)
            self.__set_key(THRESHOLD_SECTION, GREEN_LOW_KEY, self.__green_low)
            self.__set_key(THRESHOLD_SECTION, GREEN_HIGH_KEY, self.__green_high)
            self.__set_key(THRESHOLD_SECTION, RED_LOW_KEY, self.__red_low)
            self.__set_key(THRESHOLD_SECTION, RED_HIGH_KEY, self.__red_high)
            self.__set_key(PROCESSING_SECTION, CLOSE_KERNEL_KEY, self.__kernel_size_close)
            self.__set_key(PROCESSING_SECTION, OPEN_KERNEL_KEY, self.__kernel_size_open)
            self.__set_key(PROCESSING_SECTION, SHOULD_CLOSE_KEY, self.__should_close)
            self.__set_key(PROCESSING_SECTION, SHOULD_OPEN_KEY, self.__should_open)

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
