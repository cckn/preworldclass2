
"""official lib"""
import sys
sys.path.insert(0, 'lib')
import schedule # see https://github.com/dbader/schedule
import serial
import ConfigParser


"""my lib"""
import AutoSocket
import PrintConfig


CONFIG_PATH = "config.conf"

printconfig = PrintConfig.PrintConfig(CONFIG_PATH)
printconfig.show()

config = ConfigParser.ConfigParser()
config.read(CONFIG_PATH)

device_id = config.getint("DEVICE_INFO", "id")
server_ip = config.get("NETWORK_CONF", "server_ip")
server_port = config.getint("NETWORK_CONF", "server_port")


radar_serial = serial.Serial('/dev/serial0',921600)
socket = AutoSocket.AutoSocket(server_ip, server_port)

distance = 0
seqnum = 0 




def main():
    radar_serial.close()
    radar_serial.open()
    
    schedule.every(1).seconds.do(send_distance)
     
    while True:
        schedule.run_pending()
        radar_parser()



def radar_parser():
    global distance      

    rx_msg = radar_serial.readline()
    try:            
        value = int(float(rx_msg[13:21]))
        distance = (distance * 0.95) + (value * 0.05)
    except Exception as e:
        pass
    finally:
        # print rx_msg
        # print distance
        #print value
        pass
        


def send_distance():
    global seqnum

    if seqnum >= 0xffff : 
        seqnum = 0
    else : 
        seqnum += 1

    frame_buff = bytearray()

    """ HEADER """ 
    frame_buff.append(0x02) # stx 
    frame_buff.append(0x06) # Len
    frame_buff.append(0x01) # CMD TYPE
    frame_buff.append(device_id) # DEVICE ID

    """ BODY """ 
    frame_buff.append((seqnum >> 8) & 0xff) # seqNum
    frame_buff.append((seqnum) & 0xff) # seqNum
    frame_buff.append((int(distance) >> 8) & 0xff) # DISTANCE HI
    frame_buff.append(int(distance) & 0xff) # DISTANCE LOW

    """FOOTER"""
    frame_buff.append(0x03) # ETX

    
    socket.socket_auto_send(frame_buff)




if __name__ == "__main__":
    main()



