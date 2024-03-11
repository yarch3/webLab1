import socket
import threading
import pygame


PORT = 6060
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "disc"
shot_sprite = pygame.image.load("shot.png")
shot_sprite = pygame.transform.scale(shot_sprite, (104, 93))
pygame.init()


# SERVER = "192.168.1.66"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
server.bind(ADDR)
shots = []
coordinates = []

def handle_client(conn, addr, clients):
    print(f"{addr} connected\n")
    connected = True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        for client in clients:
            client.send(msg.encode(FORMAT))
        shot = msg.split(':')
        coordinates.append(shot)
        if msg:
            print(f"{addr}: {msg}")

clients = []
def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr, clients))
        thread.start()
        print(f"{threading.active_count() - 1} active connections")




print(f"server is running on {SERVER}")
start()
WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("аэо жопа")
shots = []




# Output:
# Server is listening
# Got connection from ('127.0.0.1', 52617)
# ...
