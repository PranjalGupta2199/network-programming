from utils import parse_cmd_server
from create_socket import server
# from thread_start import start_server
from async_start import start_server

if __name__ == "__main__":
    address = parse_cmd_server("Example Server")
    socket = server(address)
    start_server(socket)
