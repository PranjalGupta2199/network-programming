import socket
import argparse
import time

QUESTION_BANK = {
    b'Beautiful is better than?': b'Ugly.',
    b'Explicit is better than?': b'Implicit.',
    b'Simple is better than?': b'Complex.'
}

def get_answer(question, wait_time=0):
    assert isinstance(question, type(b'')), "Don't decode the question. Let it be in bytes !"
    time.sleep(wait_time)
    return QUESTION_BANK.get(question)

def parse_cmd_server(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    return (args.host, args.p)


def parse_cmd_client(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    return (args.host, args.p)


def sock_recv_until(sock, delim=b'?', byte_limit=4096):
    msg_rcvd = sock.recv(byte_limit)

    if not msg_rcvd:
        return (False, EOFError("Socket at {} closed. Raising EOFError !".format(sock.getpeername())))

    while not msg_rcvd.endswith(delim):
        packet_rcvd = sock.recv(byte_limit)
        if not packet_rcvd:
            return (False, IOError("Query did not end with the \"{}\" delimiter.\n \
                           Raising IOError !".format(delim)))

    return (True, msg_rcvd)
