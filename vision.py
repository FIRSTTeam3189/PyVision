import numpy as np
import cv2
import threading
import time
import VisionConfiguration
import VisionProcessor
from VisionFrameGrabber import VisionFrameGrabber
import VisionTable
import VisionServer
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
        f.write('Server Started')

    vfg = VisionFrameGrabber(0, 5).start()
    config = VisionConfiguration.VisionConfiguration("settings.conf")
    vp = VisionProcessor.VisionProcessor(config)
    table = VisionTable.VisionTable('Vision')

    # Setup streaming server
    address = ('0.0.0.0', 4269)
    try:
        VisionServer.frame_grabber = vfg
        server = VisionServer.VisionServer(address, VisionServer.VisionHandler)
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True)
        t.start()
    except Exception as e:
        print(e.args)
        print(e.message)

        # Stop all the things
        vfg.stop()
        table.send_exception_status(True)
        with open(log_file, 'a') as f:
            f.write('Failed to open stream server')
    except:
        # Stop all the things
        vfg.stop()
        table.send_exception_status(True)

    with open(log_file, 'a') as f:
        f.write('Initialized Server')
        with open(log_file, 'a') as f:
            f.write('Failed to open stream server')

    # Set properties of kinect
    vfg.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.0)
    vfg.stream.set(cv2.CAP_PROP_EXPOSURE, 0.0)

    if not vfg.stopped:
        with open(log_file, 'a') as f:
            f.write('Failed to Start server')

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
            with open(log_file, 'a') as f:
                f.write('Exception Processing vision')
                f.write(e.args)
                f.write(e.message)
        except:
            print(sys.exc_info())
            print(sys.exc_traceback)
            table.send_exception_status(True)
            vfg.stop()
            with open(log_file, 'a') as f:
                f.write('Exception Processing vision')
                f.write(sys.exc_info())
                f.write(sys.exc_traceback)

    with open(log_file, 'a') as f:
        f.write('Server shutting down')
    if table.get_should_shutdown():
        # Let table send any data
        table.send_is_online(False)
        time.sleep(3)
        server.socket.close()
        return 69

    # Let network table send any data
    table.send_is_online(False)
    time.sleep(3)
    server.socket.close()
    return 0

if __name__ == '__main__':
    code = main()
    sys.exit(code)
