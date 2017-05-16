import sys
sys.path.insert(0, 'lib')

import schedule # see https://github.com/dbader/schedule
import serial
import autosocket


device_id = 0x01

radar_serial = serial.Serial('/dev/serial0',921600)

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
        print rx_msg
        print distance
        #print value
        


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

    
    autosocket.socket_auto_send(frame_buff)




if __name__ == "__main__":
    main()



