"""
A simple Python flappy bird game made using the PyGame library
"""
import time
import pygame
import os

pygame.init()

# Window
WIDTH, HEIGHT = 600, 650
WIN = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)
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
BIRD_FALL_VEL = 3
BIRD_FALL_VEL_CHANGE = 0.05
bird_cur_fall_vel = BIRD_FALL_VEL
BIRD_CLIMB_VEL = 70
BIRD_BOUNCE_VEL = BIRD_CLIMB_VEL - 20

# Obstacles
OBS_VEL = 10
OBS_GAP = BIRD_IMG.get_height() + 100
OBS_SPACING = 100

# Ground
GROUND = pygame.rect.Rect(
            (0, 600, 600, 50)
)


def fall(bird):
    global up, bird_cur_fall_vel
    bird_cur_fall_vel += BIRD_FALL_VEL_CHANGE
    if bird.colliderect(GROUND):
        jump(bird)
    elif not up:
        bird.y += bird_cur_fall_vel


def jump(bird):
    global up, bird_cur_fall_vel
    bird_cur_fall_vel = BIRD_FALL_VEL
    up = True
    bird.y -= BIRD_CLIMB_VEL
    time.sleep(0.05)
    up = False


def draw(bird):
    """
    Handles all drawings
    :return: None
    """
    WIN.fill(WHITE)

    WIN.blit(
        BIRD_IMG,
        (bird.x, bird.y)
    )
    fall(bird)
    pygame.draw.rect(
        WIN,
        BROWN,
        GROUND,
    )

    pygame.display.update()


def main():
    """
    Main game loop
    :return: None
    """
    global up, bird_cur_fall_vel
    run = True
    clock = pygame.time.Clock()
    bird = pygame.Rect(50, 100, BIRD_IMG.get_width(), BIRD_IMG.get_height())
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump(bird)
        draw(bird)
    pygame.quit()


if __name__ == "__main__":
    main()
