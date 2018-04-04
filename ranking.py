import pygame
from pygame.locals import *
import os


def readScores():
    f = open("Score.txt", "r")
    lines = f.readlines()
    scores = []
    for l in lines:
        scores.append(l)
        if len(scores) == 10:
            break
    for i in range(len(scores)):
        scores[i],aux = scores[i].split('\n')
    return scores


def mainRank(screen, resolution, FPS, UI_Font, clock):
    listaScores = readScores()
    textLbls = []
    textRects = []

    faustop = pygame.image.load(os.path.join('sprites', 'TrofeuFaustop.png'))
    faustop = pygame.transform.scale(faustop, (int(faustop.get_width() * 0.5), int(faustop.get_height() * 0.5)))
    faustopRect = pygame.Rect(0, 0, faustop.get_width(), faustop.get_height())
    faustopRect.center = (resolution[0] / 2, resolution[1] * 0.2)


    for i in range(len(listaScores)):
        textLbls.append(UI_Font.render(listaScores[i], True, (255, 255, 255)))
        textRects.append(pygame.Rect(0, 0, textLbls[-1].get_width(), textLbls[-1].get_height()))
        textRects[-1].center = (faustopRect.centerx, faustopRect.centery * (2+(i/4)))

    continuarLbl = UI_Font.render("Pressione algo para retornar ao menu", True, (255, 255, 255))
    continuarRect = pygame.Rect(0, 0, continuarLbl.get_width(), continuarLbl.get_height())
    continuarRect.center = (textRects[-1].centerx, textRects[-1].centery * 1.1)

    rankingSound = pygame.mixer.Sound(os.path.join('songs', 'Olha que coisa linda bicho.wav'))
    rankingSound.play()

    rankBool = True
    while rankBool:
        # Tratamento de eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                rankBool = False
            if event.type == KEYDOWN:
                rankBool = False
            if event.type == MOUSEBUTTONUP:
                rankBool = False

        screen.fill((0, 0, 0))

        for line in range(len(listaScores)):
            screen.blit(textLbls[line], textRects[line])

        screen.blit(faustop, faustopRect)
        screen.blit(continuarLbl, continuarRect)

        pygame.display.flip()
        clock.tick(FPS)
