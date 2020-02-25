import threading
from utils import sock_recv_until, get_answer

def start_server(server, num_worker=-1):
    if num_worker > 0:
        print ("Starting Server with {} threads..".format(num_worker))
        for i in range(num_worker):
            threading.Thread(target=accept_connection, args=[server]).start()
    else:
        print ("Starting Server at main thread...")
        accept_connection(server)


def accept_connection(server):
    while True:
        connection, addr = server.accept()
        print ("Connection accepted from {}".format(connection.getpeername()))
        srv_reply(connection)


def srv_reply(conn_socket, delim=b'?'):
    addr = conn_socket.getpeername()
    try:
        while True:
            data = sock_recv_until(conn_socket, delim=delim)
            reply = get_answer(data)
            conn_socket.sendall(reply)
    except Exception as e:
        print ("Exception at srv_reply() by {}: \"{}\"\n".format(addr, e))
    finally:
        conn_socket.close()
