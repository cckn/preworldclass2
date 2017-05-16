import socket

# HOST='192.168.0.36' #localhost
# PORT=6005
HOST='192.168.0.11' #localhost
PORT=6000


user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

def socket_auto_send(data):
    try:
        user_socket.send(data) 
    except Exception as e:
        try:
            user_socket.close()
            global user_socket
            user_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            user_socket.connect((HOST,PORT))
            print "try"
        except Exception as e:
            print e

