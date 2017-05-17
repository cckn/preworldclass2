import sys
from collections import namedtuple
import schedule  # see https://github.com/dbader/schedule
import serial
import autosocket
import random

sys.path.insert(0, 'lib')


TEST_GPS_STRING_1 = "$GPRMC,114455.532,A,3735.0079,N,12701.6446,E,0.000000,121.61,110706,,*0A"
TEST_GPS_STRING_2 = "$GPRMC,011346.002,V,,,,,0.00,0.00,060180,,,N*41"


class ReportGPS(object):
    """docstring for ReportGPS"""

    def __init__(self, config_path):
        super(ReportGPS, self).__init__()

        PrintConfig.PrintConfig(config_path).show()

        config = ConfigParser.ConfigParser()
        config.read(config_path)

        """DEVICE_INFO"""
        self.device_id = config.getint("DEVICE_INFO", "id")

        """NETWORK_CONF"""
        server_ip = config.get("NETWORK_CONF", "server_ip")
        server_port = config.getint("NETWORK_CONF", "server_port")

        """GPS_CONF"""
        serial_path = config.get("GPS_CONF", "serial_path")
        serial_baudrate = config.getint("GPS_CONF", "serial_baudrate")
        report_interval = config.getint("GPS_CONF", "report_interval")

        self.seqnum = 0
        self.distance = 0

        self.gps_serial = serial.Serial(serial_path, serial_baudrate)
        self.socket = AutoSocket.AutoSocket(server_ip, server_port)

        self.radar_serial.close()
        self.radar_serial.open()

        schedule.every(report_interval).seconds.do(self.report)

        self.gps = namedtuple(
            "gps", "tagid, seqnum, rssi, NS, latitude, EW, longitude")
        self.gps_data = 0

    # def init()

    def report(self):
        global gps_data

        self.frame_buff = bytearray()

        """ HEADER """
        self.frame_buff.append(protocol.STX)  # STX
        self.frame_buff.append(0x00)  # Length
        self.frame_buff.append(protocol.RAPORT_GPS_DATA)  # CMD TYPE
        self.frame_buff.append(device_id)  # DEVICE ID

        """ BODY """
        self.frame_buff.append((gps_data.tagid >> 8) & 0xff)  # Tag id
        self.frame_buff.append((gps_data.tagid) & 0xff)  # Tag id
        self.frame_buff.append((gps_data.seqnum >> 8) & 0xff)  # seqNum
        self.frame_buff.append((gps_data.seqnum) & 0xff)  # seqNum

        """BODY - GPS DATA"""
        self.frame_buff = self.frame_buff + bytearray(gps_data.NS)
        self.frame_buff = self.frame_buff + \
            bytearray("%.6f" % convert_to_only_degree(gps_data.latitude))
        self.frame_buff = self.frame_buff + bytearray(gps_data.EW)
        self.frame_buff = self.frame_buff + \
            bytearray("%.6f" % convert_to_only_degree(gps_data.longitude))

        """FOOTER"""
        self.frame_buff.append(protocol.ETX)  # ETX

        self.frame_buff[1] = self.frame_buff.__len__() - 3

        autosocket.send(self.frame_buff)

    def convert_to_only_degree(self, string_data):
        float_data = float(string_data)

        degree = int(float_data / 100)
        minute = float(float_data % 100)

        result = degree + minute / 60
        return result

    def convert_to_degree_and_minute(self, float_data):
        degree = int(float_data) * 100
        minute = (float_data % 1) * 60

        result = "%.4f" % (degree + minute)
        return result

    def gps_sender(self):
        gps_data_parser()
        send_gps_data()

    def gps_data_parser():
        global seqnum
        global gps_data

        if seqnum > 0xffff:
            seqnum = 0
        else:
            seqnum += 1

        gps_data = gps(1, seqnum, random.randrange(50, 85),
                       "N", "3735.0079", "E", "12701.6446")

    def run(self):
        schedule.every(1).seconds.do(gps_sender)

        gps_data_parser()
        while True:
            schedule.run_pending()


def send_gps_data():

if __name__ == "__main__":
    main()
