import numpy as np
import cv2
import time
import VisionConfiguration
import VisionProcessor
from VisionFrameGrabber import VisionFrameGrabber
import VisionTable
import sys

log_file = 'run.log'

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
    with open(log_file, 'a') as f:
        f.write('Server Started\n')

    vfg = VisionFrameGrabber(0, 5).start()
    config = VisionConfiguration.VisionConfiguration("settings.conf")
    vp = VisionProcessor.VisionProcessor(config)
    table = VisionTable.VisionTable('Vision')

    # Set properties of kinect
    vfg.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.0)
    vfg.stream.set(cv2.CAP_PROP_EXPOSURE, 0.0)

    if not vfg.stopped:
        with open(log_file, 'a') as f:
            f.write('Starting Vision Processing\n')

    while not vfg.stopped:
        try:
            table.send_exception_status(False)
            table.send_is_online(True)
            frame = vfg.read()

            height, width, c = frame.shape

            processed = vp.process_frame(frame, config)
            hull, biggest_hull = vp.hull_frame(processed, config, False)
            drawn_image, points = vp.get_polygon_from_hull(biggest_hull)

            if points is not None:
                normalized = normalize_points(points, width, height)
                table.send_points(normalized)

            # Get if we should shut down
            if table.get_should_shutdown():
                vfg.stop()

            # Get if we should save frames
            if table.get_should_snapshot():
                vfg.should_save_frames(True)
                table.send_should_snapshot(False)

        except KeyboardInterrupt:
            vfg.stop()
            time.sleep(5)
            return 0
        except Exception as e:
            print(e.args)
            print(e.message)
            table.send_exception_status(True)
            vfg.stop()
            with open(log_file, 'a') as f:
                f.write('Exception Processing vision\n')
                f.write(e.args)
                f.write(e.message)
        except:
            print(sys.exc_info())
            print(sys.exc_traceback)
            table.send_exception_status(True)
            vfg.stop()
            with open(log_file, 'a') as f:
                f.write('Exception Processing vision\n')
                f.write(sys.exc_info())
                f.write(sys.exc_traceback)

    with open(log_file, 'a') as f:
        f.write('Server shutting down\n')

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
