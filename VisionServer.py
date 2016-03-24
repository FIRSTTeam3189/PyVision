import SocketServer
import VisionStream
import threading

frame_grabber = None


class VisionServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class VisionHandler(SocketServer.BaseRequestHandler):
    """
    This is a simple socket server to serve jpg images to a client on request
    """
    def handle(self):
        # Dispatches a new thread to stream images to the client
        handler = VisionStream.VisionStream(self.request, frame_grabber)
        handler.start()
