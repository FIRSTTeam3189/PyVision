import numpy as np
import cv2
import VisionConfiguration
import VisionProcessor


def nothing(x):
    pass


def clamp(x, low, high):
    """
    Clamps a value x between low and high

    :param x: The Value to clamp
    :param low: Low value
    :param high: High Value
    :return:
    """

    if x < low:
        x = low
    elif x > high:
        x = high

    return x


def test():
    print('Version: ' + cv2.__version__)

    # Get video capture
    cap = cv2.VideoCapture(0)

    # Keys for the window
    window_key = 'Image'
    r_low_key = 'H Low'
    r_high_key = 'H High'
    g_low_key = 'S Low'
    g_high_key = 'S High'
    b_low_key = 'V Low'
    b_high_key = 'V High'

    # Setup Window
    cv2.namedWindow(window_key)
    cv2.createTrackbar(r_low_key, window_key, 0, 255, nothing)
    cv2.createTrackbar(g_low_key, window_key, 0, 255, nothing)
    cv2.createTrackbar(b_low_key, window_key, 0, 255, nothing)
    cv2.createTrackbar(r_high_key, window_key, 0, 255, nothing)
    cv2.createTrackbar(g_high_key, window_key, 0, 255, nothing)
    cv2.createTrackbar(b_high_key, window_key, 0, 255, nothing)

    config = VisionConfiguration.VisionConfiguration("settings.conf")
    vp = VisionProcessor.VisionProcessor(config)

    cv2.setTrackbarPos(r_low_key, window_key, config.get_low_range()[0])
    cv2.setTrackbarPos(g_low_key, window_key, config.get_low_range()[1])
    cv2.setTrackbarPos(b_low_key, window_key, config.get_low_range()[2])
    cv2.setTrackbarPos(r_high_key, window_key, config.get_high_range()[0])
    cv2.setTrackbarPos(g_high_key, window_key, config.get_high_range()[1])
    cv2.setTrackbarPos(b_high_key, window_key, config.get_high_range()[2])

    while True:
        ret, frame = cap.read()

        # Get RGB Values
        r_low = cv2.getTrackbarPos(r_low_key, window_key)
        g_low = cv2.getTrackbarPos(g_low_key, window_key)
        b_low = cv2.getTrackbarPos(b_low_key, window_key)
        r_high = cv2.getTrackbarPos(r_high_key, window_key)
        g_high = cv2.getTrackbarPos(g_high_key, window_key)
        b_high = cv2.getTrackbarPos(b_high_key, window_key)

        # Set the values of the config file
        config.set_one_low(r_low)
        config.set_two_low(g_low)
        config.set_three_low(b_low)
        config.set_one_high(r_high)
        config.set_two_high(g_high)
        config.set_three_high(b_high)

        # Validate Configs
        config.validate()

        processed = vp.process_frame(frame, config)
        hull, biggest_hull = vp.hull_frame(processed, config)
        cv2.imshow(window_key, hull)
        # cv2.imshow('Hull', hull)
        # cv2.imshow('Orig Image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Closing")
    config.save("settings.conf")


def main():
    pass


if __name__ == '__main__':
    test()
