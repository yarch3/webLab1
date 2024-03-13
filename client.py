import socket
import pygame
import sys
import random
import select
import subprocess

pygame.init()
pygame.mixer.init()
global SERVER
PORT = 6060
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "disc"
WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2PCshooting")

gun_sprite = pygame.image.load("img/gun_sprite.png")
gun_sprite = pygame.transform.scale(gun_sprite, (600, 600))
computer_sprite = pygame.image.load("img/computer.png")
computer_sprite = pygame.transform.scale(computer_sprite, (626, 385))
fire_sprite = pygame.image.load("img/fire.png")
fire_sprite = pygame.transform.scale(fire_sprite, (200, 140))
shot_sprite = pygame.image.load("img/shot.png")
shot_sprite = pygame.transform.scale(shot_sprite, (104, 93))

fire_sound = pygame.mixer.Sound("music/fire.mp3")
button_sound = pygame.mixer.Sound("music/button.mp3")
beginShooter_sound = pygame.mixer.Sound("music/beginShooter.mp3")
bulletFlight_sound = pygame.mixer.Sound("music/bulletFlight.mp3")
afterFire_sound = pygame.mixer.Sound("music/afterFire.mp3")
glass_sound = pygame.mixer.Sound("music/glass.mp3")
screen.fill((150, 100, 100))
fire_timer = 0
array_shot = []
array_shot_client = []
score = 0


font = pygame.font.Font(None, 36)
button_left = pygame.Rect(300, 375, 200, 50)
button_right = pygame.Rect(600, 375, 200, 50)
button_menu = pygame.Rect(25, 25, 100, 50)
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def get_connection(ADDR):
    server_started = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while not server_started:
        screen.fill((150, 100, 100))
        draw_text('Загрузка...', font, (255, 255, 255), 300, 200)
        pygame.display.flip()
        try:
            s.connect(ADDR)
            server_started = True
        except ConnectionRefusedError:
            pass
    return s

def connectionSelection():
    while True:
        draw_text('Выбери тип подключения:', font, (255, 255, 255), 300, 200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (button_left.collidepoint(event.pos)):
                    button_sound.play(0)
                    server_process = subprocess.Popen("python main.py", shell=True)
                    SERVER = socket.gethostbyname(socket.gethostname())
                    client = get_connection((SERVER, PORT))
                    menu(client)
                if button_right.collidepoint(event.pos):
                    button_sound.play(0)
                    check_ip()
        pygame.draw.rect(screen, (100, 150, 150), button_left)
        draw_text('Создать сервер', font, (255, 255, 255), 315, 385)
        pygame.draw.rect(screen, (150, 100, 150), button_right)
        draw_text('Присоединиться', font, (255, 255, 255), 615, 385)
        pygame.display.flip()
def check_ip():
    SERVER = ""
    while True:
        screen.fill((150, 100, 100))
        draw_text('Введите IP сервера:', font, (255, 255, 255), 300, 200)
        draw_text(SERVER, font, (255, 255, 255), 300, 250)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    client = get_connection((SERVER, PORT))
                    menu(client)
                elif event.key == pygame.K_BACKSPACE:
                    SERVER = SERVER[:-1]
                else:
                    SERVER += event.unicode


        pygame.display.flip()
def menu(client,server_process):
    screen.fill((150, 100, 100))
    while True:
        draw_text('Выбери кто ты по жизни', font, (255, 255, 255), 300, 200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (button_left.collidepoint(event.pos)):
                    button_sound.play(0)
                    shooter(fire_timer, shot_sprite, client)
                elif button_right.collidepoint(event.pos):
                    button_sound.play(0)
                    notshooter(client)
        pygame.draw.rect(screen, (100, 150, 150), button_left)
        draw_text('Актив', font, (255, 255, 255), 315, 385)
        pygame.draw.rect(screen, (150, 100, 150), button_right)
        draw_text('Пассив', font, (255, 255, 255), 615, 385)
        pygame.display.flip()

def shooter(fire_timer, shot_sprite, client):
    beginShooter_sound.play(0)
    shot_sprite = pygame.transform.scale(shot_sprite, (34, 30))
    while True:
        screen.fill((150, 100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fire_sound.play(0)
                    afterFire_sound.play(0)
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
def notshooter(client):
    client.setblocking(False)  # Устанавливаем неблокирующий режим для сокета клиента
    screen.fill((150, 100, 100))
    s = 0
    array_shot_client = []
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.close()
                pygame.quit()
                sys.exit()
        ready = select.select([client], [], [], 1)
        if ready[0]:
            received = client.recv(1024).decode(FORMAT)
            received = tuple(float(y) for y in received.split(";"))
            glass_sound.play(0)
            s = s + 1
            print(s)
            print(f"received {received}")
            array_shot_client.append(received)
            for i in array_shot_client:
                screen.blit(shot_sprite, i)
            pygame.display.flip()
            if not received:
                break
            elif s > 10:
                #выключить компутер гейм овер
                break
connectionSelection()