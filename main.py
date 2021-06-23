"""
A simple Python flappy bird game made using the PyGame library
"""
import time

import pygame
import os
import random

pygame.init()

# Window
WIDTH, HEIGHT = 600, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
ICON = pygame.image.load(
    os.path.join("Assets", "icon.png")
)
pygame.display.set_icon(ICON)

# Game
FPS = 60
up = False

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (153, 79, 23)

# Bird
BIRD_IMG = pygame.transform.rotate(
    pygame.transform.flip(
        pygame.image.load(
            os.path.join("Assets", "bird.png")
        ),
        False,
        True,
    ),
    180,
)
BIRD_X = 50
bird_y = 100


def fall():
    global bird_y
    if not up:
        bird_y += 2


def draw():
    """
    Handles all drawings
    :return: None
    """
    WIN.fill(WHITE)

    WIN.blit(BIRD_IMG, (BIRD_X, bird_y))
    fall()

    pygame.draw.rect(
        WIN,
        BROWN,
        pygame.rect.Rect(
            (0, 50, 600, 50)
        )
    )

    pygame.display.update()


def main():
    """
    Main game loop
    :return: None
    """
    global bird_y, up
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    up = True
                    bird_y -= 30
                    time.sleep(0.05)
                up = False
        draw()
    pygame.quit()


if __name__ == "__main__":
    main()
