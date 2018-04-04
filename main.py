import pygame
import menu
pygame.init()

# Configs
resolution = [800, 600]
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Fausteroids")
FPS = 30
UI_Font = pygame.font.SysFont("Times New Roman", 24)
clock = pygame.time.Clock()

menu.main(screen, resolution, FPS, UI_Font, clock)

pygame.quit()
