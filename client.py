import socket

PORT = 6060
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = "fxck"
SERVER = "192.168.1.66"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

send("message 1")