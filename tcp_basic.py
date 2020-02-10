import socket
import time
import threading

client_counter = 0
CLIENT_COUNT = 2

def recvall(sock):
    data = b''
    while True:
        more = sock.recv(1)
        if more.decode('ascii') == '$':
            return data
        if not more:
            raise EOFError("error")
        data += more


def client_handler(sc, socketname):
    global client_counter
    while True:
        message = recvall(sc)

        if (message.decode('ascii') == 'exit'):
            client_counter -= 1
            sc.sendall(b'bye bro$')
            sc.close()
            return

        print('message: {!r}'.format(message))
        sc.sendall(b'Farewell, client$')
        # sc.close()
        # print('socket closed')


def server(interface, port):
    global client_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(2)
    print("server listening at: {}".format(sock.getsockname()))
    while True:
        sc, socketname = sock.accept()
        if (client_counter >= CLIENT_COUNT):
            sc.sendall(b'ma chuda madarchod$')
            sc.close()
        else:
            client_counter += 1
            sc.sendall(b'accepted$')
            print('connection from {}'.format(socketname))
            print("socket name: {!r}, socket peer: {!r}".format(sc.getsockname(), sc.getpeername()))
            t = threading.Thread(target=client_handler, args=(sc, socketname))
            t.start()
        # message = recvall(sc)
        # print('message: {!r}'.format(message))
        # sc.sendall(b'Farewell, client$')
        # sc.close()
        # print('socket closed')


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    reply = recvall(sock)
    print('server: {}'.format(reply))
    if (reply.decode('ascii') == 'ma chuda madarchod'):
        sock.close()
        exit()


    while True:
        print('client socket name: {}'.format(sock.getsockname()))
        message = input("message: ")
        message += '$'
        message = message.encode('ascii')
        print("message sent: {}".format(message))
        sock.sendall(message)  # size change
        reply = recvall(sock)
        print('server: {}'.format(reply))
        if (reply.decode('ascii') == 'ma chuda madarchod'):
            sock.close()
            exit()


if __name__ == '__main__':
    choice = input("role: ")
    if (choice == 'server'):
        interface = input("interface: ")
        server(interface, 1060)
    
    else:
        host = input('host: ')
        client(host, 1060)

