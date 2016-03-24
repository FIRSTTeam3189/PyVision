from networktables import NetworkTable

ip = "roboRIO-3189-FRC.local"

network_log_file = 'net.log'

NetworkTable.setClientMode()
NetworkTable.setIPAddress(ip)
NetworkTable.initialize()

POINT_ONE_X = 'onex'
POINT_ONE_Y = 'oney'
POINT_TWO_X = 'twox'
POINT_TWO_Y = 'twoy'
POINT_THREE_X = 'threex'
POINT_THREE_Y = 'threey'
POINT_FOUR_X = 'fourx'
POINT_FOUR_Y = 'foury'

SHOULD_SHUTDOWN = 'shutdown'
EXCEPTION_THROWN = 'exception'
IS_ONLINE = 'online'
TAKE_SNAPSHOT = 'snapshot'
LOOP_AMOUNT = 'loops'


class ConnectionListener:
    def connected(self, table):
        with file(network_log_file, 'a') as f:
            f.write('Connected to network table.\n')

    def disconnected(self, table):
        with file(network_log_file, 'a') as f:
            f.write('Disconnected from network table.\n')


class VisionTable:
    def __init__(self, table_name):
        self.table = NetworkTable.getTable(table_name)
        self.table.addConnectionListener(ConnectionListener())

    def send_points(self, points):
        for i in xrange(0, 4):
            self.send_point(i, points[i])

    def send_point(self, index, point):
        """
        Sends the points to the Vision Table
        """
        if index == 0:
            self.table.putNumber(POINT_ONE_X, point[0])
            self.table.putNumber(POINT_ONE_Y, point[1])
        elif index == 1:
            self.table.putNumber(POINT_TWO_X, point[0])
            self.table.putNumber(POINT_TWO_Y, point[1])
        elif index == 2:
            self.table.putNumber(POINT_THREE_X, point[0])
            self.table.putNumber(POINT_THREE_Y, point[1])
        elif index == 3:
            self.table.putNumber(POINT_FOUR_X, point[0])
            self.table.putNumber(POINT_FOUR_Y, point[1])

    def send_exception_status(self, exception_status):
        """
        Sends true/false if the server is crashing
        """
        self.table.putBoolean(EXCEPTION_THROWN, exception_status)

    def send_is_online(self, is_online):
        """
        Sets if the server is online
        :param is_online: If the server is online
        """
        self.table.putBoolean(IS_ONLINE, is_online)

    def get_should_shutdown(self):
        """
        Gets if the server should shutdown
        :return: If the Server should shutdown
        """
        return self.table.getBoolean(SHOULD_SHUTDOWN, False)

    def get_should_snapshot(self):
        """
        Gets if the server should take pictures
        :return: If the Server should take pictures
        """
        return self.table.getBoolean(TAKE_SNAPSHOT, False)

    def send_should_snapshot(self, should_snapshot):
        """
        Sets if the vision should snapshot
        """
        self.table.putBoolean(TAKE_SNAPSHOT, should_snapshot)

    def send_loops(self, loops):
        """
        Puts to the table how many loops we've done
        """
        self.table.putNumber(LOOP_AMOUNT, loops)
