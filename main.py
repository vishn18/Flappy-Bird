"""
A simple Python flappy bird game made using the PyGame library
"""
import random
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
score = 0

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

# Ground
GROUND = pygame.Rect(0, 600, 600, 50)

# Obstacles
OBS = pygame.Rect(WIDTH - 50, 0, 50, HEIGHT)
OBS_VEL = 5
OBS_GAP = BIRD_IMG.get_height() + 100
OBS_SPACING = 100
OBS_PATH = pygame.Rect(
    OBS.x,
    random.randint(
        0,
        (HEIGHT - GROUND.height - OBS_GAP)
    ),
    OBS.width,
    OBS_GAP,
)

# Fonts
MAJOR_MONO_DISPLAY = pygame.font.Font(
    os.path.join("Assets", "MajorMonoDisplay-Regular.ttf"),
    60
)
STAATLICHES = pygame.font.Font(
    os.path.join("Assets", "Staatliches-Regular.ttf"),
    40
)


def end():
    WIN.fill(WHITE)
    message = MAJOR_MONO_DISPLAY.render("GAME OVER", True, BROWN)
    WIN.blit(message, (WIDTH / 2 - message.get_width() / 2, WIDTH / 2 - message.get_height()))
    score_text = STAATLICHES.render(f"SCORE: {score}", True, BLACK)
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, WIDTH / 2 + 100))
    pygame.display.update()
    time.sleep(3)
    quit()


def fall(bird):
    global up, bird_cur_fall_vel
    bird_cur_fall_vel += BIRD_FALL_VEL_CHANGE
    if bird.colliderect(GROUND):
        jump(bird)
    elif not up:
        bird.y += bird_cur_fall_vel
    if (bird.colliderect(OBS) and not bird.colliderect(OBS_PATH)) and (not(bird.colliderect(OBS) and bird.colliderect(OBS_PATH))):
        end()


def jump(bird):
    global up, bird_cur_fall_vel
    bird_cur_fall_vel = BIRD_FALL_VEL
    up = True
    bird.y -= BIRD_CLIMB_VEL
    time.sleep(0.05)
    up = False


def obs_move():
    global score
    if OBS.x + OBS.width < 0:
        OBS.x = WIDTH - OBS.width
        OBS_PATH.y = random.randint(0, (HEIGHT - GROUND.height - OBS_GAP))
        score += 1
    OBS.x -= OBS_VEL
    OBS_PATH.x = OBS.x


def draw(bird):
    """
    Handles all drawings
    :return: None
    """
    # Background
    WIN.fill(WHITE)

    # Obstacles
    pygame.draw.rect(
        WIN,
        GREEN,
        OBS
    )
    pygame.draw.rect(
        WIN,
        WHITE,
        OBS_PATH
    )
    obs_move()

    # Bird
    WIN.blit(
        BIRD_IMG,
        (bird.x, bird.y)
    )
    fall(bird)

    # Ground
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
    obstacles = []
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
