import sys
sys.path.insert(0, 'lib')

from collections import namedtuple
import schedule # see https://github.com/dbader/schedule
import serial
import autosocket
import random


device_id = 0x01


seqnum = 0 
# gps_serial = serial.Serial('/dev/serial0',921600)

TEST_GPS_STRING_1 = "$GPRMC,114455.532,A,3735.0079,N,12701.6446,E,0.000000,121.61,110706,,*0A"
TEST_GPS_STRING_2 = "$GPRMC,011346.002,V,,,,,0.00,0.00,060180,,,N*41"


gps = namedtuple("gps", "tagid, seqnum, rssi, NS, latitude, EW, longitude")
gps_data = 0 


def main():
    # gps_serial.close()
    # gps_serial.open()
    
    schedule.every(1).seconds.do(gps_sender)
    gps_data_parser()
    while True:
        schedule.run_pending()

        # print sys.argv[1]
    #     rx_msg = gps_serial.readline()
    #     try:            
    #         value = int(float(rx_msg[13:21]))
    #         distance = (distance * 0.95) + (value * 0.05)
    #     except Exception as e:
    #         pass
    #     finally:
    #         print rx_msg
    #         print distance
    #         #print value


        
def gps_convert_to_only_degree(string_data):
    float_data = float(string_data)

    degree = int(float_data / 100) 
    minute = float(float_data % 100)

    result = degree + minute / 60
    return result


def gps_convert_to_degree_and_minute(float_data):
    degree = int(float_data) * 100
    minute = (float_data % 1) * 60

    result = "%.4f" % (degree + minute) 
    return result



def gps_sender():
    gps_data_parser()
    send_gps_data()
    

def gps_data_parser():
    global seqnum
    global gps_data

    if seqnum > 0xffff : 
        seqnum = 0
    else : 
        seqnum += 1

    gps_data = gps(1, seqnum, random.randrange(50,85), "N", "3735.0079", "E", "12701.6446")


def send_gps_data():
    global gps_data        
    

    frame_buff = bytearray()

    """ HEADER """ 
    frame_buff.append(0x02) # STX 
    frame_buff.append(0x1B) # Length
    frame_buff.append(0x02) # CMD TYPE
    frame_buff.append(device_id) # DEVICE ID

    """ BODY """ 
    frame_buff.append((gps_data.tagid >> 8) & 0xff) # Tag id
    frame_buff.append((gps_data.tagid) & 0xff) # Tag id
    frame_buff.append((gps_data.seqnum >> 8) & 0xff) # seqNum
    frame_buff.append((gps_data.seqnum) & 0xff) # seqNum

    """BODY - GPS DATA"""
    frame_buff = frame_buff + bytearray(gps_data.NS)
    frame_buff = frame_buff + bytearray("%.6f" % gps_convert_to_only_degree(gps_data.latitude))
    frame_buff = frame_buff + bytearray(gps_data.EW)
    frame_buff = frame_buff + bytearray("%.6f" % gps_convert_to_only_degree(gps_data.longitude))

    """FOOTER"""
    frame_buff.append(0x03) # ETX
    
    autosocket.send(frame_buff)


if __name__ == "__main__":
    main()





