import argparse, random, socket, zen_utils

def client(address, cause_error=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.bind(('127.0.0.1', 1070))
    sock.connect(address)
    # sock.settimeout(2) ## connection refused after timeout
    print ("Connected at {}".format(sock.getsockname()))
    aphorisms = list(zen_utils.aphorisms)
    if cause_error:
        sock.sendall(aphorisms[0][:-1])
        return
    while True:
        for ques in aphorisms:
            sock.sendall(ques)
            print ("question {}".format(ques))
            print("Answer:", zen_utils.recv_until(sock, b'?'))
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-e', action='store_true', help='cause an error')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, 1060)
    client(address, args.e)
