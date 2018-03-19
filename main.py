import os
import pygame
import math
from pygame.locals import *

pygame.init()

# Configs
resolution = (800, 600)
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

inGame = True

while inGame:
    for event in pygame.event.get():
        # Tratamento de eventos
        if event.type == QUIT:
            inGame = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                inGame = False

        ##### Movimento
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

    ##### Atualizaçao do jogo
    # Rotaçao
    spaceship_rotation += spaceship_rotationspeed
    spaceship = pygame.transform.rotozoom(spaceship_copy, spaceship_rotation, 1)
    spaceship_rect = spaceship.get_rect(center=spaceship_rect.center)

    # Posiçao /// -cos(x) para x e sen(x) para y
    spaceship_rect = spaceship_rect.move(-math.cos(math.radians(spaceship_rotation)) * spaceship_speedy,
                                         math.sin(math.radians(spaceship_rotation)) * spaceship_speedy)
    #####


    # Atualizaçao da tela
    screen.fill((0, 0, 0))
    screen.blit(spaceship, spaceship_rect)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
