from networktables import NetworkTable

ip = "roboRIO-3189-FRC.local"

NetworkTable.setClientMode()
NetworkTable.setIPAddress(ip)
NetworkTable.initialize()


class VisionTable:
    def __init__(self, table_name):
        self.table = NetworkTable.getTable(table_name)

    def send_points(self, points):
        for i in xrange(0, 4):
            self.send_point(i, points[i])

    def send_point(self, index, point):
        if index == 0:
            self.table.putNumber('onex', point[0])
            self.table.putNumber('oney', point[1])
        elif index == 1:
            self.table.putNumber('twox', point[0])
            self.table.putNumber('twoy', point[1])
        elif index == 2:
            self.table.putNumber('threex', point[0])
            self.table.putNumber('threey', point[1])
        elif index == 3:
            self.table.putNumber('fourx', point[0])
            self.table.putNumber('foury', point[1])
