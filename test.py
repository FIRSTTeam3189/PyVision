import cv2
import VisionConfiguration
import VisionProcessor
from VisionFrameGrabber import VisionFrameGrabber


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


def normalize_points(points, width, height):
    '''
    Normalizes a set of points
    :param points: The points
    :param width: Width
    :param height: Height
    :return: The normalized points
    '''
    norm = []

    for point in points:
        norm.append([point[0] / float(width), point[1] / float(height)])

    return tuple(norm)


def test():
    print('Version: ' + cv2.__version__)

    # Get video capture
    cap = VisionFrameGrabber(0, 10).start()

    # Set properties of kinect
    cap.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    cap.stream.set(cv2.CAP_PROP_EXPOSURE, 0.0)

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
        frame = cap.read()

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
        # config.validate()

        processed = vp.process_frame(frame, config)
        hull, biggest_hull = vp.hull_frame(processed, config)
        drawn_image, points = vp.get_polygon_from_hull(biggest_hull, frame)
        cv2.imshow(window_key, drawn_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.stop()
    cv2.destroyAllWindows()
    print("Closing")
    config.save("settings.conf")


def test2():
    vfg = VisionFrameGrabber(0, 10).start()

    while True:
        frame = vfg.read()
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vfg.stop()
