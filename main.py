import socket
import threading

PORT = 6060
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = "fxck"
#SERVER = "192.168.1.66"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
shots = []


def handle_client(conn, addr): 
    print(f"{addr} connected\n")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False

            print(f"{addr}: {msg}")

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"{threading.active_count() - 1} active connections")

print(f"server is running on {SERVER}")
start()


# Output:
# Server is listening
# Got connection from ('127.0.0.1', 52617)
# ...
