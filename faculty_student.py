import socket

BUFSIZE = 65535
def server(ip_addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip_addr, port))
    print("Listening for datagrams at {}".format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(BUFSIZE)
        text = data.decode('ascii')
        print('the client at {} says: {!r}'.format(address, text))


def client(ip_addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    text = input("text: ")
    sock.sendto(text.encode('ascii'), (ip_addr, port))

if __name__ == '__main__':
    choice = input("role: ")
    if (choice == "client"):
        client('<broadcast>', 1060)
    else:
        host = input()
        server(host, 1060)

