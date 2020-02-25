import socket
import threading
import time

def server(address, backlog=64):
    srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_socket.bind(('127.0.0.1', 1060))
    srv_socket.listen(backlog)

    print("Server Started at {}".format(address))
    return srv_socket
