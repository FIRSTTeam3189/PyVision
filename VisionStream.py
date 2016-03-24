import socket
import time
import cv2
import struct
import sys

class VisionStream:
    def __init__(self, socket, frame_grabber):
        self.socket = socket
        self.frame_grabber = frame_grabber

    def start(self):
        """
        Starts sending over jpg images to the RoboRIO
        """
        try:
            while True:
                raw_string = self.socket.recv(1)
                if len(raw_string) == 0:
                    time.sleep(.01)
                    continue
                command = ord(raw_string)
                if command == 1:
                    # Send the image to him
                    ret, image_bytes = cv2.imencode('.jpg', self.frame_grabber.read())
                    if not ret:
                        # Failed to encode image, send empty string
                        self.socket.send(0)
                    else:
                        self.socket.send(struct.pack('i', int(len(image_bytes))))
                        self.socket.send(image_bytes)
                if command == 2:
                    # Close the socket by breaking
                    break
                else:
                    time.sleep(.1)
                    print('Got unknown command %d' % command)

        except IOError as e:
            print(e.message)
            print(e.args)
        except Exception as e:
            print(e.args)
            print(e.message)
        except:
            print('Unkown error, Closing stream')
