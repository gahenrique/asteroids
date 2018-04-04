import pygame
from pygame.locals import *
import sys
import os


def mainCred(screen, resolution, FPS, UI_Font, clock):
    creditosLbl = UI_Font.render("Créditos", True, (255, 255, 255))
    creditosRect = pygame.Rect(0, 0, creditosLbl.get_width(), creditosLbl.get_height())
    creditosRect.center = (resolution[0] / 2, resolution[1] * 0.2)

    textLbls = []
    textRects = []
    textLines = ["Gabriel Henrique", "Felipe Kaça", "Victor Falcetta"]

    for i in range(len(textLines)):
        textLbls.append(UI_Font.render(textLines[i], True, (255, 255, 255)))
        textRects.append(pygame.Rect(0, 0, textLbls[-1].get_width(), textLbls[-1].get_height()))
        textRects[-1].center = (creditosRect.centerx, creditosRect.centery * (2+(i/2)))

    continuarLbl = UI_Font.render("Pressione algo para retornar ao menu", True, (255, 255, 255))
    continuarRect = pygame.Rect(0, 0, continuarLbl.get_width(), continuarLbl.get_height())
    continuarRect.center = (textRects[-1].centerx, textRects[-1].centery * 1.5)

    creditosSong = pygame.mixer.Sound(os.path.join('songs', 'Trabalha e estuda ou so faz isso.wav'))
    creditosSong.play()

    inCreditos = True
    while inCreditos:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    sys.exit()
                else:
                    inCreditos = False
            if event.type == MOUSEBUTTONUP:
                inCreditos = False

        screen.fill((0, 0, 0))

        screen.blit(creditosLbl, creditosRect)
        for line in range(len(textLines)):
            screen.blit(textLbls[line], textRects[line])
        screen.blit(continuarLbl, continuarRect)

        pygame.display.flip()
        clock.tick(FPS)
