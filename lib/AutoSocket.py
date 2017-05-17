import ConfigParser
import socket

import PrintConfig


class AutoSocket(object):
    """docstring for AutoSocket"""

    def __init__(self, server_ip, server_port):
        super(AutoSocket, self).__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    def socket_auto_send(self, data):
        try:
            self.user_socket.send(data) 
            print "send"
        except Exception as e:
            try:
                self.user_socket.close()
                self.user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                self.user_socket.connect((self.server_ip, self.server_port))
                print "try"
            except Exception as e:
                print e



def main():
    pass


if __name__ == "__main__":
    main()




