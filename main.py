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


def distance_rect(rect1, rect2):
    # Checa a distancia Euclideana entre dois retangulos
    return math.hypot(rect1.x - rect2.x, rect1.y - rect2.y)



pygame.init()

# Configs
resolution = [800, 600]
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Asteroids")
FPS = 30
num_asteroids = 6
clock = pygame.time.Clock()

# Importando os sprites
spaceship = pygame.image.load(os.path.join('sprites', 'spaceship1.png'))
spaceship = pygame.transform.scale(spaceship, (35, 44))

asteroid = pygame.image.load(os.path.join('sprites', 'asteroid.png'))
asteroid = pygame.transform.scale(asteroid, (52, 52))
asteroid_mini = pygame.transform.scale(asteroid, (26, 26))

missile = pygame.image.load(os.path.join('sprites', 'missile.png'))
missile = pygame.transform.scale(missile, (16, 4))

# Spaceship array indices:
# 0 == Nave_Surface / 1 == Retangulo / 2 == Velocidade / 3 == Velocidade_Rotaçao / 4 == Rotaçao_Atual / 5 == Raio
spaceship_array = [spaceship, pygame.Rect(300, 300, spaceship.get_width(), spaceship.get_height()), 0, 0, 90, 17]

# Array e variaveis para os disparos
missiles_array = []
missile_speed = 10

# Array e variavel para os asteroides
# Asteroids Array indices: 0 == Asteroid_Surface / 1 == Retangulo / 2 == Rotaçao / 3 == Raio / 4 == 0(Grande) ou 1(Pequeno)
asteroids_array = []
asteroid_speed = 3

for ast in range(num_asteroids):
    # Inicializando os asteroids em posiçoes aleatorias
    x = randint(0, resolution[0])
    y = randint(0, resolution[1])
    rot = randint(0, 360)
    asteroids_array.append([asteroid, pygame.Rect(x, y, asteroid.get_width(), asteroid.get_height()), rot, 24, 0])

inGame = True

while inGame:
    for event in pygame.event.get():
        # Tratamento de eventos
        # Sair
        if event.type == QUIT:
            inGame = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                inGame = False

            # Atirar
            if event.key == K_SPACE:
                # Indice [0] contém a surface do disparo, [1] o retangulo, [2] sua rotaçao
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
    spaceship_array[0] = pygame.transform.rotozoom(spaceship, spaceship_array[4], 1)
    spaceship_array[1] = spaceship_array[0].get_rect(center=spaceship_array[1].center)

    # Posiçao da nave /// -cos(x) para x e sen(x) para y
    spaceship_array[1] = move_by_rotation(spaceship_array[1], spaceship_array[4], spaceship_array[2])

    spaceship_array[1] = invert_position(spaceship_array[1])

    # Tiro
    for m in missiles_array:
        # Posiçao do disparo
        m[1] = move_by_rotation(m[1], m[2], -missile_speed)

    # Remove os misseis fora da tela
    missiles_array = remove_missile(missiles_array)

    # Asteroides
    for ast in asteroids_array:
        # Posiçao do asteroide
        ast[1] = move_by_rotation(ast[1], ast[2], asteroid_speed)

        # Inverte posiçao caso va sair da tela
        ast[1] = invert_position(ast[1])

        # Checa se o asteroide colidiu
        if distance_rect(ast[1], spaceship_array[1]) - (ast[4] + spaceship_array[5]) < 0:
            print("colidiu")
            #inGame = False

        # Checa se o missel colidiu com o asteroide
        for m in missiles_array:
            if m[1].colliderect(ast[1]):
                if ast[4] == 0:
                    # Cria 2 novos asteroides menores caso ele seja grande
                    for _ in range(2):
                        rot = randint(0, 360)
                        asteroids_array.append([asteroid_mini,
                                                pygame.Rect(ast[1].x, ast[1].y, asteroid_mini.get_width(), asteroid_mini.get_height()),
                                                rot, 12, 1])

                #Destroi o asteroide e o missel
                missiles_array.remove(m)
                asteroids_array.remove(ast)
    #####

    # Atualizaçao da tela
    # Limpa a tela com a cor preta
    screen.fill((0, 0, 0))

    '''
    Alcance da nave (retangulo e circulo) para teste de colisao
    # aux = pygame.Surface((spaceship_array[1].w, spaceship_array[1].h))
    # aux.fill((255,255,255))
    # screen.blit(aux, spaceship_array[1])
    # pygame.draw.circle(screen, (255, 255, 255), spaceship_array[1].center, spaceship_array[5])
    '''
    # Blit Nave
    screen.blit(spaceship_array[0], spaceship_array[1])

    # Blit Misseis
    for m in missiles_array:
        '''
        Alcance dos misseis (retangulo) para teste de colisao
        aux = pygame.Surface((m[0].get_size()))
        aux.fill((255, 255, 255))
        screen.blit(aux, m[1])
        '''
        screen.blit(m[0], m[1])

    # Blit Asteroides
    for ast in asteroids_array:
        '''
        Alcance dos asteroides (retangulo e circulo) para teste de colisao
        aux = pygame.Surface((ast[0].get_size()))
        aux.fill((255,255,255))
        screen.blit(aux, ast[1])
        pygame.draw.circle(screen,(255,255,255), ast[1].center, 24)
        '''
        screen.blit(ast[0], ast[1])

    pygame.display.flip()
    clock.tick(30)
    #####

pygame.quit()
