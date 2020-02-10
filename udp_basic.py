import argparse, socket
from datetime import datetime

MAX_BYTE = 65535
def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    print("Listening at {}".format(sock.getsockname()))
    while True:
        data_recv, address = sock.recvfrom(MAX_BYTE)
        text = data_recv.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        text = "your data was {} bytes long.".format(len(data_recv))
        data_sent = text.encode('ascii')
        sock.sendto(data_sent, address)


def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = "this time is {}".format(datetime.now())
    data_sent = text.encode('ascii')
    sock.sendto(data_sent, ('127.0.0.1', port))
    print('address assigned: {}'.format(sock.getsockname()))
    data_recv, address = sock.recvfrom(MAX_BYTE)
    text = data_recv.decode('ascii')
    print("the server {} sent {}".format(address, text))


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description="send and recv UDP locally")
    parser.add_argument('role', choices=choices, help='role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP Port')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)
