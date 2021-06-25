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
ICON = pygame.image.load(os.path.join("Assets", "Images", "icon.png"))
pygame.display.set_icon(ICON)

# Game
FPS = 60
INVINCIBLE = 0
up = False
score = 0

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (153, 79, 23)

# Bird
BIRD_IMG = pygame.transform.rotate(
    pygame.transform.flip(
        pygame.image.load(
            os.path.join("Assets", "Images", "bird.png")
        ),
        False,
        True,
    ),
    180,
)
SEAGULL_IMG = pygame.transform.rotate(
    pygame.transform.flip(
        pygame.image.load(
            os.path.join("Assets", "Images", "seagull.png")
        ),
        False,
        True,
    ),
    180,
)
AIRCRAFT_IMG = pygame.image.load(os.path.join("Assets", "Images", "aircraft.png"))
COPTER_IMG_1 = pygame.image.load(os.path.join("Assets", "Images", "helicopter.png"))
COPTER_IMG_2 = pygame.image.load(os.path.join("Assets", "Images", "helicopter2.png"))
cur_bird_img = BIRD_IMG
BIRD_FALL_VEL = 3
BIRD_FALL_VEL_CHANGE = 0.05
bird_cur_fall_vel = BIRD_FALL_VEL
BIRD_CLIMB_VEL = 10
BIRD_BOUNCE_VEL = 50

# Ground
GROUND = pygame.Rect(0, 600, 600, 50)

# Obstacles
OBS_VEL = 5
obs_gap = cur_bird_img.get_height() + 150
OBS_SPACING = 100
OBS_TOP = pygame.Rect(
    WIDTH - 50,
    0,
    50,
    random.randint(0, (HEIGHT - GROUND.height - obs_gap)),
)
OBS_BOTTOM = pygame.Rect(
    OBS_TOP.x,
    OBS_TOP.height + obs_gap,
    OBS_TOP.width,
    (HEIGHT - GROUND.height) - OBS_TOP.height,
)

# Fonts
MAJOR_MONO_DISPLAY = pygame.font.Font(
    os.path.join("Assets", "Fonts", "MajorMonoDisplay-Regular.ttf"),
    60
)
STAATLICHES = pygame.font.Font(
    os.path.join("Assets", "Fonts", "Staatliches-Regular.ttf"),
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
        up = True
        bird_cur_fall_vel = BIRD_FALL_VEL
        bird.y -= BIRD_BOUNCE_VEL
        up = False
    elif not up:
        bird.y += bird_cur_fall_vel
    if not INVINCIBLE:
        if bird.colliderect(OBS_TOP) or bird.colliderect(OBS_BOTTOM):
            end()


def jump(bird):
    global up, bird_cur_fall_vel
    bird_cur_fall_vel = BIRD_FALL_VEL
    up = True
    bird.y -= BIRD_CLIMB_VEL
    up = False


def move_bird(bird):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_SPACE] and bird.y - BIRD_CLIMB_VEL > 0:
        jump(bird)


def obs_move():
    global obs_gap, score
    obs_gap = cur_bird_img.get_height() + 150
    if OBS_TOP.x + OBS_TOP.width < 0:
        OBS_TOP.x = WIDTH - OBS_TOP.width
        OBS_TOP.height = random.randint(0, (HEIGHT - GROUND.height - obs_gap))
        score += 1
    OBS_TOP.x -= OBS_VEL
    OBS_BOTTOM.x = OBS_TOP.x
    OBS_BOTTOM.y = OBS_TOP.height + obs_gap
    OBS_BOTTOM.height = (HEIGHT - GROUND.height) - OBS_TOP.height


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
        OBS_TOP,
    )
    pygame.draw.rect(
        WIN,
        GREEN,
        OBS_BOTTOM,
    )
    obs_move()

    # Bird
    move_bird(bird)
    WIN.blit(
        cur_bird_img,
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
    global cur_bird_img, up, bird_cur_fall_vel
    run = True
    clock = pygame.time.Clock()
    bird = pygame.Rect(50, 100, cur_bird_img.get_width(), cur_bird_img.get_height())
    obstacles = []
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    cur_bird_img = BIRD_IMG
                elif event.key == pygame.K_2:
                    cur_bird_img = SEAGULL_IMG
                elif event.key == pygame.K_3:
                    cur_bird_img = AIRCRAFT_IMG
                elif event.key == pygame.K_4:
                    cur_bird_img = COPTER_IMG_1
                elif event.key == pygame.K_5:
                    cur_bird_img = COPTER_IMG_2
        draw(bird)
    pygame.quit()


if __name__ == "__main__":
    main()
