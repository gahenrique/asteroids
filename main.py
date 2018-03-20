import os
import pygame
import math
from pygame.locals import *
from random import randint


def move_by_rotation(rect, rot, speed):
    # Entra com um retangulo, uma rotaçao e uma velocidade para mover em determinado angulo
    rect = rect.move(-math.cos(math.radians(rot)) * speed, math.sin(math.radians(rot)) * speed)
    return rect


def remove_missile(list):
    # Entra com uma lista e se o retangulo contido estiver fora da tela ele e removido do array
    for rect in list:
        if rect[1].x > resolution[0] or rect[1].x < 0 or rect[1].y > resolution[1] or rect[1].y < 0:
            list.remove(rect)
    return list


def invert_position(rect):
    # Inverte a posiçao na tela se ultrapassar do limite da resoluçao
    if rect.x > resolution[0]:
        rect.x = 0
    if rect.x < 0:
        rect.x = resolution[0]
    if rect.y > resolution[1]:
        rect.y = 0
    if rect.y < 0:
        rect.y = resolution[1]
    return rect

pygame.init()

# Configs
resolution = [800, 600]
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Asteroids")
FPS = 30
num_asteroids = 6
clock = pygame.time.Clock()

# Importando os sprites
spaceship = pygame.image.load(os.path.join('sprites', 'spaceship1.png')).convert()
spaceship = pygame.transform.scale(spaceship, (35, 44))
spaceship_copy = spaceship.copy()

asteroid = pygame.image.load(os.path.join('sprites', 'asteroid.png'))
asteroid = pygame.transform.scale(asteroid, (52, 52))

missile = pygame.image.load(os.path.join('sprites', 'missile.png')).convert()
missile = pygame.transform.scale(missile, (16, 4))

# Spaceship array indices:
# 0 == Nave_Surface / 1 == Retangulo / 2 == Speed / 3 == Rotation_speed / 4 == Current_rotation
spaceship_array = [spaceship, pygame.Rect(300, 300, spaceship.get_width(), spaceship.get_height()), 0, 0, 90]

# Array e variaveis para os disparos
missiles_array = []
missile_speed = 10

# Array e variavel para os asteroides
# Asteroids Array indices: 0 == Asteroid_Surface / 1 == Retangulo / 2 == Rotaçao
asteroids_array = []
asteroid_speed = 3

for ast in range(num_asteroids):
    #Inicializando os asteroids em posiçoes aleatorias
    x = randint(0,resolution[0])
    y = randint(0,resolution[1])
    rot = randint(0,360)
    asteroids_array.append([asteroid, pygame.Rect(x,y, asteroid.get_width(), asteroid.get_height()), rot])

inGame = True

while inGame:
    for event in pygame.event.get():
        # Tratamento de eventos
        if event.type == QUIT:
            inGame = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                inGame = False

            # Atirar
            if event.key == K_SPACE:
                # Indice [0] contém a surface do disparo, [1] o retangulo e [2] sua rotaçao
                missiles_array.append([missile, pygame.Rect(spaceship_array[1].centerx, spaceship_array[1].centery,
                                                            missile.get_width(), missile.get_height()),
                                       spaceship_array[4]])

                # Rotaçao do disparo
                missiles_array[-1][0] = pygame.transform.rotozoom(missile, missiles_array[-1][2], 1)

        # Movimento
            if event.key == K_w:
                spaceship_array[2] = -5
            if event.key == K_a:
                spaceship_array[3] = 5
            if event.key == K_d:
                spaceship_array[3] = -5

        if event.type == KEYUP:
            if event.key == K_w:
                spaceship_array[2] = 0
            if event.key == K_a:
                spaceship_array[3] = 0
            if event.key == K_d:
                spaceship_array[3] = 0
        ######

    # Atualizaçao do jogo
    # Rotaçao da nave
    spaceship_array[4] += spaceship_array[3]
    spaceship_array[0] = pygame.transform.rotozoom(spaceship_copy, spaceship_array[4], 1)
    spaceship_array[1] = spaceship_array[0].get_rect(center=spaceship_array[1].center)

    # Posiçao da nave /// -cos(x) para x e sen(x) para y
    spaceship_array[1] = move_by_rotation(spaceship_array[1], spaceship_array[4], spaceship_array[2])

    spaceship_array[1] = invert_position(spaceship_array[1])

    # Tiro
    for m in range(len(missiles_array)):
        # Posiçao do disparo
        missiles_array[m][1] = move_by_rotation(missiles_array[m][1], missiles_array[m][2], -missile_speed)

    # Remove os misseis fora da tela
    missiles_array = remove_missile(missiles_array)

    #Asteroides
    for ast in asteroids_array:
        # Posiçao do asteroide
        ast[1] = move_by_rotation(ast[1], ast[2], asteroid_speed)

        # Inverte posiçao caso va sair da tela
        ast[1] = invert_position(ast[1])

        # Checa se o asteroide colidiu
        if ast[1].collidelist([spaceship_array[1]]) != -1:
            print("colidiu")

        for m in missiles_array:
            if m[1].colliderect(ast[1]):
                print("missel")

    #####

    # Atualizaçao da tela
    screen.fill((0, 0, 0))
    screen.blit(spaceship_array[0], spaceship_array[1])

    for i in range(len(missiles_array)):
        screen.blit(missiles_array[i][0], missiles_array[i][1])

    for ast in asteroids_array:
        screen.blit(ast[0], ast[1])

    pygame.display.flip()
    clock.tick(30)
    #####

pygame.quit()
