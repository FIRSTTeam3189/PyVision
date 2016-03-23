import numpy as np
import cv2
import timeit
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
        norm.append([point[0] / float(width), point[1] / float(height)])

    return tuple(norm)


def main():
    vfg = VisionFrameGrabber(0, 5).start()
    config = VisionConfiguration.VisionConfiguration("settings.conf")
    vp = VisionProcessor.VisionProcessor(config)
    table = VisionTable.VisionTable('Vision')

    # Set properties of kinect
    vfg.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.0)
    vfg.stream.set(cv2.CAP_PROP_EXPOSURE, 0.0)

    while not vfg.stopped:
        try:
            frame = vfg.read()

            height, width, c = frame.shape

            processed = vp.process_frame(frame, config)
            hull, biggest_hull = vp.hull_frame(processed, config, False)
            drawn_image, points = vp.get_polygon_from_hull(biggest_hull)

            if points is not None:
                normalized = normalize_points(points, width, height)
                table.send_points(normalized)
        except:
            print(sys.exc_info())
            print(sys.exc_traceback)
            vfg.stop()

    vfg.stop()
    print('Shutting Down')

if __name__ == '__main__':
    main()
