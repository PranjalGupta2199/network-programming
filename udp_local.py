import argparse, socket
from datetime import datetime
import time

MAX_BYTES = 65555
RATE = 50  # byte per minute

# data structure
ganda = {}


def check_rate(address, data_size):

    print("addr: {}, size: {}".format(address, data_size))

    ip_list = ganda.get(address)
    if (ip_list == None):
        return (True, 0)
    else:
        current_time = time.time()
        total_data_size = 0
        for (data_sz, timestamp) in ip_list:
            if (int(current_time - timestamp) <= 60):
                total_data_size += data_sz
            
        diff_size = data_size - (RATE - total_data_size)
        time_st = 0
        temp_data_size = 0
        for (data_sz, timestamp) in ip_list:
            if (int(current_time - timestamp) <= 60):
                temp_data_size += data_sz
                if (temp_data_size >= diff_size):
                    time_st = int(timestamp + 60 - time.time())


        if ((total_data_size + data_size) < RATE):
            return (True, 0)
        else:
            return (False, time_st)


def insert_rate(address, data_size):
    ip_list = ganda.get(address)
    if (ip_list == None):
        ganda[address] = [(data_size, time.time())]
    else:
        ganda[address].append((data_size, time.time()))


def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print("The client at {} says {!r}".format(address,text))
        print("received data size: {}".format(len(text)))

        response = ""
        status, timeout = check_rate(address, len(data))
        if (status):
            insert_rate(address, len(data))
            response = "data accepted"
        else:
            response = "wait for: {} seconds".format(timeout)

        data_r = response.encode('ascii')
        sock.sendto(data_r, address)
        print(ganda)

def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1',40230))
    text = 'hi' * 10
    data = text.encode('ascii')
    sock.sendto(data, ('127.0.0.1', port))
    print('The OS assigned me the address {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTES)  # client is currently in the promiscious mode (no-filtering)
    text = data.decode('ascii')
    print('The server {} replied {!r}'.format(address, text))

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description = 'Send and Receive UDP locally')
    parser.add_argument('role', choices=choices, help = 'which role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default = 1060, help = 'UDP port (default 53)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)
