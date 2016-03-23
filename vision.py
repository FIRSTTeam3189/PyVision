import numpy as np
import cv2
import timeit
import time
import VisionConfiguration
import VisionProcessor
from VisionFrameGrabber import VisionFrameGrabber
import VisionTable
import sys


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
        norm.append([float(point[0]) / float(width), float(point[1]) / float(height)])

    return tuple(norm)


def main():
    vfg = VisionFrameGrabber(0, 5).start()
    config = VisionConfiguration.VisionConfiguration("settings.conf")
    vp = VisionProcessor.VisionProcessor(config)
    table = VisionTable.VisionTable('Vision')

    # Set properties of kinect
    vfg.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.0)
    vfg.stream.set(cv2.CAP_PROP_EXPOSURE, 0.0)

    table.send_exception_status(False)

    while not vfg.stopped:
        try:
            table.send_is_online(True)
            frame = vfg.read()

            height, width, c = frame.shape

            processed = vp.process_frame(frame, config)
            hull, biggest_hull = vp.hull_frame(processed, config, False)
            drawn_image, points = vp.get_polygon_from_hull(biggest_hull)

            if points is not None:
                normalized = normalize_points(points, width, height)
                table.send_points(normalized)

            if table.get_should_shutdown():
                vfg.stop()

        except KeyboardInterrupt:
            vfg.stop()
            return 69
        except Exception as e:
            print(e.args)
            print(e.message)
            table.send_exception_status(True)
            vfg.stop()
        except:
            print(sys.exc_info())
            print(sys.exc_traceback)
            table.send_exception_status(True)
            vfg.stop()

    print('Shutting Down')
    if table.get_should_shutdown():
        # Let table send any data
        table.send_is_online(False)
        time.sleep(3)
        return 69

    # Let network table send any data
    table.send_is_online(False)
    time.sleep(3)
    return 0

if __name__ == '__main__':
    code = main()
    sys.exit(code)
