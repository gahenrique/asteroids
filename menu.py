import pygame
import os
from pygame.locals import *


pygame.init()

# Configs
resolution = [800, 600]
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Asteroids")
FPS = 30
num_asteroids = 6
clock = pygame.time.Clock()
UI_Font = pygame.font.SysFont("Times New Roman", 24)

# Logo
logo = pygame.image.load(os.path.join('sprites', 'logo.png'))
logo = pygame.transform.scale(logo, (int(logo.get_width() * 0.5), int(logo.get_height() * 0.5)))
logo_Rect = pygame.Rect(0, 0, logo.get_width(), logo.get_height())
logo_Rect.center = (resolution[0] / 2, resolution[1] / 2.5)

# Menu opçoes
start = UI_Font.render("Jogar", True, (255, 255, 255))
start_Rect = pygame.Rect(0, 0, start.get_width(), start.get_height())
start_Rect.center = (logo_Rect.centerx, logo_Rect.centery * 1.6)

ranking = UI_Font.render("Ranking", True, (255, 255, 255))
ranking_Rect = pygame.Rect(0, 0, ranking.get_width(), ranking.get_height())
ranking_Rect.center = (start_Rect.centerx, start_Rect.centery * 1.1)

creditos = UI_Font.render("Créditos", True, (255, 255, 255))
creditos_Rect = pygame.Rect(0, 0, creditos.get_width(), creditos.get_height())
creditos_Rect.center = (ranking_Rect.centerx, ranking_Rect.centery * 1.1)

sair = UI_Font.render("Sair", True, (255, 255, 255))
sair_Rect = pygame.Rect(0, 0, sair.get_width(), sair.get_height())
sair_Rect.center = (creditos_Rect.centerx, creditos_Rect.centery * 1.1)

menu = True
while menu:
    # Tratamento de eventos
    for event in pygame.event.get():
        # Sair
        if event.type == QUIT:
            menu = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                menu = False

        # Muda as cores de fundo de cada opçao quando o mouse estiver em cima
        if event.type == MOUSEMOTION:
            if start_Rect.collidepoint(event.pos):
                start = UI_Font.render("Jogar", True, (0, 0, 0), (255, 255, 255))
            else:
                start = UI_Font.render("Jogar", True, (255, 255, 255))

            if ranking_Rect.collidepoint(event.pos):
                ranking = UI_Font.render("Ranking", True, (0, 0, 0), (255, 255, 255))
            else:
                ranking = UI_Font.render("Ranking", True, (255, 255, 255))

            if creditos_Rect.collidepoint(event.pos):
                creditos = UI_Font.render("Créditos", True, (0, 0, 0), (255, 255, 255))
            else:
                creditos = UI_Font.render("Créditos", True, (255, 255, 255))

            if sair_Rect.collidepoint(event.pos):
                sair = UI_Font.render("Sair", True, (0, 0, 0), (255, 255, 255))
            else:
                sair = UI_Font.render("Sair", True, (255, 255, 255))

        if event.type == MOUSEBUTTONUP:
            if start_Rect.collidepoint(event.pos[0], event.pos[1]):
                # Start_Game()
                pass

    # -------------------------------------------------------------------------

    # Atualizaçao da tela
    # Limpa a tela com a cor preta
    screen.fill((0, 0, 0))

    # Blit logo
    screen.blit(logo, logo_Rect)

    #Blit Opçoes
    screen.blit(start, start_Rect)
    screen.blit(ranking, ranking_Rect)
    screen.blit(creditos, creditos_Rect)
    screen.blit(sair, sair_Rect)

    clock.tick(30)
    pygame.display.flip()

pygame.quit()
