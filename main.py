import os
import pygame
import math
from pygame.locals import *


def move_by_rotation(rect, rot, speed):
    # Entra com um retangulo, uma rotaçao e uma velocidade para mover em determinado angulo
    rect = rect.move(-math.cos(math.radians(rot)) * speed, math.sin(math.radians(rot)) * speed)
    return rect

def remove_missile(list):
    for rect in list:
        if rect[1].x > resolution[0] or rect[1].x < 0 or rect[1].y > resolution[1] or rect[1].y < 0:
            list.remove(rect)
    return list


def invert_position(rect):
    # Inverte a posiçao na tela se ultrapassar do limite da resoluçao
    if rect.x > resolution[0]:
        rect = rect.move(0, rect.y)
    if rect.x < 0:
        rect = rect.move(resolution[0], rect.y)
    if rect.y > resolution[1]:
        rect = rect.move(rect.x, 0)
    if rect.y < 0:
        rect = rect.move(rect.x, resolution[1])
    return rect

pygame.init()

# Configs
resolution = [800, 600]
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Asteroids")
FPS = 30
clock = pygame.time.Clock()

# Importando os sprites
spaceship = pygame.image.load(os.path.join('sprites', 'spaceship1.png')).convert()
spaceship = pygame.transform.scale(spaceship, (35, 44))
spaceship_copy = spaceship.copy()

# array indices 0 e 1 = x e y respectivamente
spaceship_rect = pygame.Rect(spaceship.get_width(), spaceship.get_height(), 300, 300)
spaceship_speedy = 0
spaceship_rotationspeed = 0
spaceship_rotation = 90

# Array e variaveis para os disparos
missile = pygame.image.load(os.path.join('sprites', 'missile.png')).convert()
missile = pygame.transform.scale(missile, (16, 4))
missiles_array = []
missile_speed = 10

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
                missiles_array.append([missile, pygame.Rect(spaceship_rect.centerx, spaceship_rect.centery,
                                                            missile.get_width(), missile.get_height()),
                                       spaceship_rotation])

                # Rotaçao do disparo
                missiles_array[-1][0] = pygame.transform.rotozoom(missile, missiles_array[-1][2], 1)

        # Movimento
            if event.key == K_w:
                spaceship_speedy = -5
            if event.key == K_a:
                spaceship_rotationspeed = 5
            if event.key == K_d:
                spaceship_rotationspeed = -5

        if event.type == KEYUP:
            if event.key == K_w:
                spaceship_speedy = 0
            if event.key == K_a:
                spaceship_rotationspeed = 0
            if event.key == K_d:
                spaceship_rotationspeed = 0
        ######

    # Atualizaçao do jogo
    # Rotaçao da nave
    spaceship_rotation += spaceship_rotationspeed
    spaceship = pygame.transform.rotozoom(spaceship_copy, spaceship_rotation, 1)
    spaceship_rect = spaceship.get_rect(center=spaceship_rect.center)

    # Posiçao da nave /// -cos(x) para x e sen(x) para y
    spaceship_rect = move_by_rotation(spaceship_rect, spaceship_rotation, spaceship_speedy)

    #spaceship_rect = invert_position(spaceship_rect)

    # Tiro
    for m in range(len(missiles_array)):
        # Posiçao do disparo
        missiles_array[m][1] = move_by_rotation(missiles_array[m][1], missiles_array[m][2], -missile_speed)

    # Remove os misseis fora da tela
    missiles_array = remove_missile(missiles_array)
    #####

    # Atualizaçao da tela
    screen.fill((0, 0, 0))

    for i in range(len(missiles_array)):
        screen.blit(missiles_array[i][0], missiles_array[i][1])

    screen.blit(spaceship, spaceship_rect)
    pygame.display.flip()
    clock.tick(30)
    #####

pygame.quit()
