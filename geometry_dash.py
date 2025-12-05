import pygame
import sys

pygame.init()

# --- Window ---
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Geometry Dash")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (70, 130, 255)
RED   = (255, 80, 80)
GREEN = (80, 255, 120)

# --- Player setup ---
player_size = 30
player_x = 100
ground_level = HEIGHT - 20  # Ground height
player_rect = pygame.Rect(player_x, ground_level - player_size, player_size, player_size)

gravity = 0.7
jump_force = -12
velocity_y = 0

# --- Levels ---
LEVELS = {
    1: {
        "speed": 6,
        "color": BLUE,
        "obstacles": [500, 700, 900, 1150, 1500]
    },
    2: {
        "speed": 8,
        "color": RED,
        "obstacles": [400, 600, 800, 1000, 1300, 1600]
    },
    3: {
        "speed": 10,
        "color": GREEN,
        "obstacles": [450, 650, 900, 1200, 1500, 1800, 2100]
    }
}

current_level = 1
running_game = False

def reset_player():
    global velocity_y
    player_rect.y = ground_level - player_size
    velocity_y = 0

def create_obstacles(offsets):
    return [pygame.Rect(x, ground_level - 50, 30, 50) for x in offsets]

def draw(level_data, obstacles):
    WIN.fill(level_data["color"])

    # ground
    pygame.draw.rect(WIN, BLACK, (0, ground_level, WIDTH, 20))

    # player
    pygame.draw.rect(WIN, WHITE, player_rect)

    # obstacles
    for o in obstacles:
        pygame.draw.rect(WIN, BLACK, o)

    pygame.display.update()

def show_menu():
    WIN.fill(BLACK)
    font = pygame.font.SysFont(None, 48)
    text1 = font.render("Press 1, 2, or 3 to choose a level", True, WHITE)
    WIN.blit(text1, (80, 150))
    pygame.display.update()

clock = pygame.time.Clock()

# --- Main Loop ---
while True:
    if not running_game:
        show_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not running_game and event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                current_level = int(event.unicode)
                level_data = LEVELS[current_level]
                obstacles = create_obstacles(level_data["obstacles"])
                reset_player()
                running_game = True

        if running_game and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= ground_level:
                velocity_y = jump_force

    if running_game:
        # gravity
        velocity_y += gravity
        player_rect.y += velocity_y

        # ground collision
        if player_rect.bottom > ground_level:
            player_rect.bottom = ground_level
            velocity_y = 0

        # move obstacles
        for o in obstacles:
            o.x -= level_data["speed"]

        # respawn obstacles after they exit screen
        for i, o in enumerate(obstacles):
            if o.right < 0:
                prev = obstacles[i - 1]
                o.x = prev.x + 300  # consistent spacing

        # detect collision → return to menu
        for o in obstacles:
            if player_rect.colliderect(o):
                running_game = False

        draw(level_data, obstacles)

    clock.tick(60)
