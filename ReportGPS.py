#-*- coding: utf-8 -*-

import schedule  # see https://github.com/dbader/schedule
import serial
import ConfigParser
import random
from collections import namedtuple

from import_manager import AutoSocket
from import_manager import PrintConfig
from import_manager import protocol


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

        """GPS_DUMMY_CONF"""
        self.tagid = config.getint("GPS_DUMMY_CONF", "tagid")
        self.default_latitute = config.getfloat(
            "GPS_DUMMY_CONF", "default_latitute")
        self.default_longitute = config.getfloat(
            "GPS_DUMMY_CONF", "default_longitute")
        self.rand_value = config.getint("GPS_DUMMY_CONF", "rand_value")

        self.seqnum = 0

        self.gps_serial = serial.Serial(serial_path, serial_baudrate)
        self.socket = AutoSocket.AutoSocket(server_ip, server_port)

        self.gps_serial.close()
        self.gps_serial.open()

        schedule.every(report_interval).seconds.do(self.report)

        self.gps = namedtuple(
            "gps", "tagid, seqnum, NS, latitude, EW, longitude")
        self.gps_data = 0

    # def init()

    def update(self):
        if self.seqnum >= 0xffff:
            self.seqnum = 0
        else:
            self.seqnum += 1

        latitude = self.default_latitute + \
            (float(random.randrange(0, self.rand_value)) / pow(10, 6))
        longitude = self.default_longitute + \
            (float(random.randrange(0, self.rand_value)) / pow(10, 6))

        self.gps_data = self.gps(self.tagid, self.seqnum,
                                 "N", latitude, "E", longitude)

        random.randrange(0, 85)
        self

    def report(self):

        self.update()

        self.frame_buff = bytearray()

        """ HEADER """
        self.frame_buff.append(protocol.STX)  # stx
        self.frame_buff.append(0x00)  # Len
        self.frame_buff.append(protocol.REPORT_RADAR_DATA)  # CMD TYPE
        self.frame_buff.append(self.device_id)  # DEVICE ID

        """ BODY """
        self.frame_buff.append(((self.gps_data.tagid) >> 8) & 0xff)  # Tag id
        self.frame_buff.append((self.gps_data.tagid) & 0xff)  # Tag id
        self.frame_buff.append((self.gps_data.seqnum >> 8) & 0xff)  # seqNum
        self.frame_buff.append((self.gps_data.seqnum) & 0xff)  # seqNum

        """BODY - GPS DATA"""
        self.frame_buff = self.frame_buff + bytearray(self.gps_data.NS)
        self.frame_buff = self.frame_buff + \
            bytearray("%.6f" % self.gps_data.latitude)
        self.frame_buff = self.frame_buff + bytearray(self.gps_data.EW)
        self.frame_buff = self.frame_buff + \
            bytearray("%.6f" % self.gps_data.longitude)

        """FOOTER"""
        self.frame_buff.append(protocol.ETX)  # ETX

        """Update Length Field"""
        self.frame_buff[1] = self.frame_buff.__len__() - 3
        self.socket.send(self.frame_buff)

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

    def run(self):

        while True:
            schedule.run_pending()


def main():

    ex = ReportGPS("config.conf")
    ex.run()

if __name__ == "__main__":
    main()
