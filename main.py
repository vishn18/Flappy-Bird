"""
A simple Python Flappy Bird game made using the Pygame library
"""
try:
    from colorama import Fore
except ModuleNotFoundError:
    print("Couldn't import colorama!")
try:
    import pygame
except ModuleNotFoundError:
    try:
        print(f"{Fore.RED}Couldn't import pygame: Module 'pygame' is not installed!")
        print(f"{Fore.YELLOW}Flappy Bird requires pygame to run.")
    except NameError:
        print("Couldn't import pygame: Module 'pygame' is not installed!")
        print("Flappy Bird requires pygame to run.")
    finally:
        exit()
import random
from Data import data
import os

with open(os.path.join("Data", "data.csv"), "r") as file:
    if file.read() == "":
        try:
            print(f"{Fore.RED}Data file is empty!")
            print(f"{Fore.YELLOW}Resetting data...")
            data.reset()
            print(f"{Fore.GREEN}Done!")
        except NameError:
            print("Data file is empty!")
            print("Resetting data...")
            data.reset()
            print("Done!")

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
up = False
score = 0

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (233, 63, 74)
TEAL = (36, 156, 131)
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
birds = {
    1: BIRD_IMG,
    2: SEAGULL_IMG,
    3: AIRCRAFT_IMG,
    4: COPTER_IMG_1,
    5: COPTER_IMG_2,
}
cur_bird_img = birds[int(data.get()["bird"])]
BIRD_FALL_VEL = 3
BIRD_FALL_VEL_CHANGE = 0.05
bird_cur_fall_vel = BIRD_FALL_VEL
BIRD_CLIMB_VEL = 10

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
    """
    Game ending / 'outro'
    :return: None
    """
    hs = data.get()["highscore"]
    if score > int(hs):
        hs_broken = 1
    else:
        hs_broken = 0
    WIN.fill(WHITE)
    message = MAJOR_MONO_DISPLAY.render("GAME OVER", True, BROWN)
    WIN.blit(message, (WIDTH / 2 - message.get_width() / 2, WIDTH / 2 - message.get_height()))
    score_text = STAATLICHES.render(f"SCORE: {score}", True, BLACK)
    WIN.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, WIDTH / 2 + 100))
    if hs_broken:
        hs_text = STAATLICHES.render(f"NEW HIGH SCORE!", True, BLACK)
        hs_prev = STAATLICHES.render(f"PREVIOUS HIGH SCORE: {hs}", True, BLACK)
        WIN.blit(hs_prev, (WIDTH / 2 - hs_prev.get_width() / 2, WIDTH / 2 + 300))
        data.edit(score, list(birds.keys())[list(birds.values()).index(cur_bird_img)])
    else:
        hs_text = STAATLICHES.render(f"HIGH SCORE: {hs}", True, BLACK)
        data.edit(hs, list(birds.keys())[list(birds.values()).index(cur_bird_img)])
    WIN.blit(hs_text, (WIDTH / 2 - hs_text.get_width() / 2, WIDTH / 2 + 200))
    pygame.display.update()
    pygame.time.wait(5000)
    exit()


def fall(bird):
    """
    Handles falling and collision of the bird
    :param Rect object 'bird'
    :return: None
    """
    global up, bird_cur_fall_vel
    bird_cur_fall_vel += BIRD_FALL_VEL_CHANGE
    if not up:
        bird.y += bird_cur_fall_vel
    if bird.colliderect(OBS_TOP) or bird.colliderect(OBS_BOTTOM) or bird.colliderect(GROUND):
        end()


def jump(bird):
    """
    Handles jumping of the bird
    :param bird: Rect object 'bird'
    :return: None
    """
    global up, bird_cur_fall_vel
    bird_cur_fall_vel = BIRD_FALL_VEL
    up = True
    bird.y -= BIRD_CLIMB_VEL
    up = False


def move_bird(bird):
    """
    Handles movement of the bird
    :param bird: Rect object 'bird'
    :return: None
    """
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_SPACE] and bird.y - BIRD_CLIMB_VEL > 0:
        jump(bird)


def obs_move():
    """
    Handles movement of obstacles
    :return: None
    """
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
    WIN.fill(BLACK)

    # Obstacles
    pygame.draw.rect(
        WIN,
        RED,
        OBS_TOP,
    )
    pygame.draw.rect(
        WIN,
        RED,
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
        TEAL,
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
