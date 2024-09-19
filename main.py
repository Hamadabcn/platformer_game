import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Platformer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game variables
player_size = 50
player_color = BLUE
player_x, player_y = WIDTH // 2, HEIGHT - player_size
player_vel = 300
player_jump = False
jump_count = 10
fall_speed = 0  # Start with no fall speed
gravity = 15  # Adjust gravity for smoother jumping
level = 0
platforms = []
bounce_factor = 0.7  # Bounce factor for the ball
best_score = 0
delay_start = False
delay_timer = 0
rotation_angle = 0
rotation_speed = 2  # Speed of rolling effect

# Constants
FINISH_LINE_HEIGHT = 100  # Space reserved for the finish line at the top
PLATFORM_SPACING = 150  # Minimum vertical distance between platforms


def draw_background():
    """Draws a gradient background for the main game screen."""
    top_color = pygame.Color(135, 206, 250)  # Sky blue
    bottom_color = pygame.Color(0, 191, 255)  # Deep sky blue

    gradient_surface = pygame.Surface((WIDTH, HEIGHT))

    for y in range(HEIGHT):
        color = pygame.Color(
            int(top_color.r + (bottom_color.r - top_color.r) * (y / HEIGHT)),
            int(top_color.g + (bottom_color.g - top_color.g) * (y / HEIGHT)),
            int(top_color.b + (bottom_color.b - top_color.b) * (y / HEIGHT))
        )
        pygame.draw.line(gradient_surface, color, (0, y), (WIDTH, y))

    screen.blit(gradient_surface, (0, 0))


def draw_instructions_background():
    """Draws a gradient background for the instructions screen."""
    top_color = pygame.Color(255, 223, 186)  # Light peach
    bottom_color = pygame.Color(255, 182, 193)  # Light pink

    gradient_surface = pygame.Surface((WIDTH, HEIGHT))

    for y in range(HEIGHT):
        color = pygame.Color(
            int(top_color.r + (bottom_color.r - top_color.r) * (y / HEIGHT)),
            int(top_color.g + (bottom_color.g - top_color.g) * (y / HEIGHT)),
            int(top_color.b + (bottom_color.b - top_color.b) * (y / HEIGHT))
        )
        pygame.draw.line(gradient_surface, color, (0, y), (WIDTH, y))

    screen.blit(gradient_surface, (0, 0))


def generate_platforms(level):
    """Generates platforms based on the current level."""
    global platforms
    platforms = []
    num_platforms = level + 15  # Increase the number of platforms per level
    platform_width = 200
    platform_height = 20
    base_y = HEIGHT - platform_height - 100  # Starting y position for the first platform

    while base_y > FINISH_LINE_HEIGHT + PLATFORM_SPACING:
        x = random.randint(0, WIDTH - platform_width)
        platforms.append(pygame.Rect(x, base_y, platform_width, platform_height))
        base_y -= random.randint(PLATFORM_SPACING - 30, PLATFORM_SPACING)

    platforms.append(pygame.Rect(WIDTH // 2 - platform_width // 2, FINISH_LINE_HEIGHT + 70, platform_width,
                                 platform_height))


def draw_text(text, font, color, surface, x, y):
    """Draws text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def draw_window():
    """Draws the main game window."""
    draw_background()  # Draw gradient background
    draw_ball()  # Draw the ball with rolling effect
    for plat in platforms:
        pygame.draw.rect(screen, BLACK, plat)

    pygame.draw.rect(screen, RED, pygame.Rect(WIDTH // 2 - 25, 50, 50, 20))  # Finish line

    pygame.draw.rect(screen, GREEN, (50, 10, 100, 40))  # Play Again button
    pygame.draw.rect(screen, RED, (650, 10, 100, 40))  # Quit button

    draw_text("Play Again", pygame.font.SysFont('Comic Sans MS', 21), BLACK, screen, 100, 30)
    draw_text("Quit", pygame.font.SysFont('Comic Sans MS', 21), BLACK, screen, 700, 30)
    draw_text(f"Level {level + 1}", pygame.font.SysFont('Comic Sans MS', 28), BLACK, screen, WIDTH // 2, 30)
    draw_text(f"Best Score: {best_score}", pygame.font.SysFont('Comic Sans MS', 28), BLACK, screen, WIDTH // 2,
              HEIGHT - 30)

    pygame.display.update()


def draw_ball():
    """Draws the ball with a rolling effect."""
    global rotation_angle
    ball_surface = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
    pygame.draw.circle(ball_surface, player_color, (player_size // 2, player_size // 2), player_size // 2)
    rotated_surface = pygame.transform.rotate(ball_surface, rotation_angle)
    screen.blit(rotated_surface, (player_x - player_size // 2, player_y - player_size // 2))
    rotation_angle = (rotation_angle + rotation_speed) % 360


def show_instructions():
    """Displays the instructions page."""
    font = pygame.font.SysFont(None, 36)
    draw_instructions_background()  # Draw gradient background for instructions

    draw_text("Welcome to the Interactive Platformer Game!", font, BLACK, screen, WIDTH // 2, HEIGHT // 4)
    draw_text("Controls:", font, BLACK, screen, WIDTH // 2, HEIGHT // 3)
    draw_text("Arrow Keys - Move Left/Right", font, BLACK, screen, WIDTH // 2, HEIGHT // 3 + 40)
    draw_text("Spacebar - Jump", font, BLACK, screen, WIDTH // 2, HEIGHT // 3 + 100)
    draw_text("Click anywhere to start...", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)
    draw_text("Good Luck!!!", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 120)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def handle_buttons():
    """Handles button clicks for Play Again and Quit."""
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if (50 < mouse_pos[0] < 150) and (10 < mouse_pos[1] < 50):
        if mouse_click[0]:
            reset_game()

    if (650 < mouse_pos[0] < 750) and (10 < mouse_pos[1] < 50):
        if mouse_click[0]:
            pygame.quit()
            sys.exit()


def reset_game():
    """Resets the game to the initial state."""
    global player_x, player_y, player_jump, jump_count, fall_speed, level, delay_start, delay_timer

    player_x, player_y = WIDTH // 2, HEIGHT - player_size
    player_jump = False
    jump_count = 10
    fall_speed = 0
    level = 0
    delay_start = False
    delay_timer = 0
    generate_platforms(level)  # Regenerate platforms for the starting level


def handle_movement(keys, dt):
    """Handles player movement and jumping."""
    global player_x, player_y, player_jump, jump_count, fall_speed, delay_start, delay_timer, rotation_angle

    if keys[pygame.K_LEFT]:
        player_x -= player_vel * dt
    if keys[pygame.K_RIGHT]:
        player_x += player_vel * dt

    if not player_jump:
        if keys[pygame.K_SPACE]:
            player_jump = True
            jump_count = 10  # Reset jump count
            fall_speed = -8  # Decrease initial jump speed for shorter jump
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.3 * neg  # Further reduce jump height
            jump_count -= 1
        else:
            player_jump = False
            jump_count = 10
            fall_speed = 0

    player_y += fall_speed * dt
    fall_speed += gravity * dt  # Gravity remains the same

    if delay_start:
        if time.time() - delay_timer > 1:
            delay_start = False
        return

    # Check for bounce effect
    if player_y > HEIGHT - player_size // 2:
        player_y = HEIGHT - player_size // 2
        fall_speed = -fall_speed * bounce_factor

    if player_x < player_size // 2:
        player_x = player_size // 2
    if player_x > WIDTH - player_size // 2:
        player_x = WIDTH - player_size // 2
    if player_y < player_size // 2:
        player_y = player_size // 2
        fall_speed = 0

    handle_collision()


def handle_collision():
    """Handles collisions between the player and platforms."""
    global player_y, fall_speed, delay_start, delay_timer
    on_ground = False
    player_rect = pygame.Rect(player_x - player_size // 2, player_y - player_size // 2, player_size, player_size)
    for plat in platforms:
        if player_rect.colliderect(plat):
            if player_y + player_size // 2 > plat.top and fall_speed > 0:
                player_y = plat.top - player_size // 2
                fall_speed = 0
                on_ground = True

    if player_y < 50 and not on_ground:
        if pygame.Rect(WIDTH // 2 - 25, 50, 50, 20).colliderect(player_rect):
            level_up()

    if not on_ground:
        fall_speed += gravity


def level_up():
    """Advances to the next level."""
    global level, player_x, player_y, player_jump, jump_count, fall_speed, delay_start, delay_timer

    level += 1
    generate_platforms(level)
    player_x, player_y = WIDTH // 2, HEIGHT - player_size
    player_jump = False
    jump_count = 10
    fall_speed = 0
    delay_start = True
    delay_timer = time.time()

    # Update best score
    global best_score
    best_score = max(best_score, level + 1)


def game_loop():
    """Main game loop."""
    global player_x, player_y

    clock = pygame.time.Clock()
    generate_platforms(level)
    show_instructions()

    while True:
        dt = clock.tick(30) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        handle_movement(keys, dt)
        handle_buttons()

        draw_window()


if __name__ == "__main__":
    game_loop()
