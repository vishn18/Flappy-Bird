"""
A simple Python flappy bird game made using the PyGame library
"""
import pygame
import os
import random

pygame.init()

# Window
WIDTH, HEIGHT = 600, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
ICON = pygame.image.load(os.path.join("Assets", "icon.png"))
pygame.display.set_icon(ICON)

# Game
FPS = 60

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def draw():
    """
    Handles all drawings
    :return:
    """
    WIN.fill(WHITE)

    pygame.display.update()


def main():
    """
    Main game loop
    :return:
    """
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw()
    pygame.quit()


if __name__ == "__main__":
    main()
