
#-*- coding: utf-8 -*-
import schedule  # see https://github.com/dbader/schedule
import datetime


def teee():
    dt = datetime.datetime.now() + datetime.timedelta(seconds=10)

    if(dt.microsecond < 1000):
        print(dt)
        print(dt.microsecond)


# schedule.every(1).seconds.do(teee)


while True:
    dt = datetime.datetime.now() + datetime.timedelta(seconds=10)

    if(dt.microsecond < 100):
        print(dt)
        print(dt.microsecond)

    # schedule.run_pending()

# #-*- coding: utf-8 -*-

# import socket
# from datetime import datetime


# user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# user_socket.connect(("192.168.0.11", 6000))


# while True:
#     dt = datetime.now()
#     user_socket.send(str(dt) + "\n")
