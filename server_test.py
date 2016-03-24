import SingleFrameGrabber
import VisionServer
import socket
import threading
import struct
import cv2
import numpy as np

def main():
    address = ('localhost', 4269)
    frame_grabber = SingleFrameGrabber.SingleFrameGrabber('pupp.jpg').start()
    VisionServer.frame_grabber = frame_grabber
    server = VisionServer.VisionServer(address, VisionServer.VisionHandler)

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()
    print('Server is running')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)

    # Send control byte
    s.send(chr(1).encode())

    # Get first four bytes and decode length
    stuffs = s.recv(4)
    length = int(struct.unpack('i', str(stuffs))[0])
    print(length)

    # Get the Image
    image_bytes = s.recv(1024)
    length -= 1024
    while length > 0:
        if length < 1024:
            image_bytes = image_bytes + s.recv(length)
            length = 0
        else:
            image_bytes = image_bytes + s.recv(1024)
            length -= 1024

    numpy_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    image = cv2.imdecode(numpy_bytes, 0)

    cv2.imshow('Image', image)
    cv2.waitKey(0)

    s.close()
    server.socket.close()


if __name__ == '__main__':
    main()