import socket

import pygame
import sys
import random

import select
from _socket import IPPROTO_TCP

pygame.init()
PORT = 6060
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "disc"
SERVER = "192.168.1.66"
ADDR = (SERVER, PORT)
WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite пистолета")

gun_sprite = pygame.image.load("gun_sprite.png")
gun_sprite = pygame.transform.scale(gun_sprite, (600, 600))
computer_sprite = pygame.image.load("computer.png")
computer_sprite = pygame.transform.scale(computer_sprite, (626, 385))
fire_sprite = pygame.image.load("fire.png")
fire_sprite = pygame.transform.scale(fire_sprite, (200, 140))
shot_sprite = pygame.image.load("shot.png")
shot_sprite = pygame.transform.scale(shot_sprite, (104, 93))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
client.connect(ADDR)

is_shooting = False
fire_timer = 0
array_shot = []
array_shot_client = []

userid = 0

def shooter(fire_timer):
    running = True
    while running:
        screen.fill((150, 100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fire_timer = pygame.time.get_ticks()
                    # Создание нового попадания
                    x_cords = random.randint(315, 705)
                    y_cords = random.randint(185, 390)
                    new_shot = (x_cords, y_cords)
                    new_shot_client = ((x_cords - 340) * 2.5, (y_cords - 210) * 2.85)
                    send_text = str(new_shot_client[0]) + ';' + str(new_shot_client[1])
                    client.send(send_text.encode(FORMAT))
                    print(new_shot)
                    array_shot.append(new_shot)

                # Попадание клиенту

                # Попадание
        for i in array_shot:
            screen.blit(shot_sprite, i)
        # Компутер
        screen.blit(computer_sprite, (250, 180))
        # Огонь
        current_time = pygame.time.get_ticks()
        if current_time - fire_timer < 100:
            screen.blit(fire_sprite, (600, 380))
        # Ружьё
        screen.blit(gun_sprite, (400, 100))

        pygame.display.flip()
        pygame.time.delay(30)


def notshooter():
    client.setblocking(False)  # Устанавливаем неблокирующий режим для сокета клиента
    while True:
        screen.fill((150, 100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.close()
                pygame.quit()
                sys.exit()
        ready = select.select([client], [], [], 1)
        if ready[0]:
            received = client.recv(1024).decode(FORMAT)
            received = tuple(float(y) for y in received.split(";"))
            print(f"received {received}")
            array_shot_client.append(received)
            for i in array_shot_client:
                screen.blit(shot_sprite, i)
            pygame.display.flip()
            if not received:
                break


shooter(fire_timer)



