from utils import parse_cmd_server, get_answer
from create_socket import server
import select
import socket

def all_events_forever(poll_object):
    while True:
        for fd, event in poll_object.poll():
            yield fd, event

def start(server):
    sockets = {server.fileno(): server}
    addresses = {}
    bytes_read = {}
    bytes_send = {}
    server_send = []
    ans_sock = {}

    poll = select.poll()
    poll.register(server, select.POLLIN)

    for fd, event in all_events_forever(poll):
        sock = sockets[fd]

        if sock is server:
            sock, addr = sock.accept()
            print ("Connection accepted from {}".format(addr))
            sock.setblocking(False)
            sockets[sock.fileno()] = sock
            addresses[sock] = addr
            if (sock.getpeername()[1] == 1070):
                poll.register(sock, select.POLLOUT)
            else:
                poll.register(sock, select.POLLIN)

        elif event & (select.POLLERR | select.POLLHUP | select.POLLNVAL):
            address = addresses.pop(sock)
            rb = bytes_read.pop(sock, b'')
            sb = bytes_send.pop(sock, b'')
            if rb:
                print('Client {} sent {} but then closed'.format(address, rb))
            elif sb:
                print('Client {} closed before we sent {}'.format(address, sb))
            else:
                print('Client {} closed socket normally'.format(address))
            poll.unregister(fd)
            del sockets[fd]

        elif event & select.POLLIN:
            more_data = sock.recv(4096)
            if not more_data:
                sock.close()
                continue

            data = bytes_read.pop(sock, b'') + more_data

            if data.endswith(b'?'):
                print (data)
                if sock.getpeername()[1] != 1070:
                    server_send.append((data, sock))
                    print ("Server Send", server_send)
                    poll.modify(sock, select.POLLOUT)
                    bytes_send[sock] = b''
                    print ("Bytes Send", bytes_send)
                else:
                    bytes_send[ans_sock] = data
                    print("data to be sent: ", data)
                    print("ans sock: ", ans_sock)
                    poll.modify(sock, select.POLLOUT)
            else:
                if sock.getpeername()[1] != 1070:
                    bytes_read[sock] = data
                else:
                    bytes_send[ans_sock] = data

        elif event & select.POLLOUT:

            if sock.getpeername()[1] == 1070:
                # print("answer server")
                if (len(server_send) == 0):
                    continue
                ques, ans_sock = server_send.pop()
                bytes_send[sock] = ques
                print("data to send to answer server")

            if not sock in bytes_send:
                continue

            if not bytes_send[sock].endswith(b'?'):
                continue

            print("sock: {}, data: {}".format(sock.getpeername(),data))

            data = bytes_send.pop(sock)
            n = sock.send(data)
            if (n < len(data)):
                bytes_send[sock] = data[n:]
            else:
                poll.modify(sock, select.POLLIN)


if __name__ == "__main__":
    address = parse_cmd_server("Example server for Assn1")
    print (address)
    print("hello")
    start(server(('127.0.0.1', 1060)))
    # print ("Hello")
