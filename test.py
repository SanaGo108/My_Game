import pygame
import random
import math

pygame.init()

# Constants
CELL_SIZE = 20
NUM_CELLS = 20
SCREEN_SIZE = NUM_CELLS * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60  # Increased FPS for smoother movement

# Display setup
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("ЗМЕЙКА")

# Font setup for game over message
font = pygame.font.Font(None, 36)

# Load snake head image
snake_head_img = pygame.image.load('snake_head.png').convert_alpha()
snake_head_img = pygame.transform.scale(snake_head_img, (CELL_SIZE, CELL_SIZE))

# Timer
clock = pygame.time.Clock()

def draw_circle(color, row, col):
    center_position = (int(col * CELL_SIZE + CELL_SIZE // 2), int(row * CELL_SIZE + CELL_SIZE // 2))
    pygame.draw.circle(screen, color, center_position, CELL_SIZE // 2)

def mouse_to_direction(mouse_pos, snake_head):
    mx, my = mouse_pos
    head_x, head_y = snake_head
    head_screen_x = head_y * CELL_SIZE + CELL_SIZE // 2
    head_screen_y = head_x * CELL_SIZE + CELL_SIZE // 2
    return (mx - head_screen_x, my - head_screen_y)

def display_game_over(screen, font):
    """Displays the game over message."""
    screen.fill(BLACK)
    text = font.render('ИГРА ОКОНЧЕНА', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)  # Display the message for 2 seconds

def game_loop():
    snake = [(NUM_CELLS // 2, NUM_CELLS // 2)]
    food = (random.randint(0, NUM_CELLS - 1), random.randint(0, NUM_CELLS - 1))
    direction = (0, 1)  # Start moving to the right
    grow_snake = False  # Toggle to control snake growth

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        mouse_pos = pygame.mouse.get_pos()
        move = mouse_to_direction(mouse_pos, snake[0])

        if math.hypot(move[0], move[1]) > CELL_SIZE:
            if abs(move[0]) > abs(move[1]):
                direction = (0, 1 if move[0] > 0 else -1)
            else:
                direction = (1 if move[1] > 0 else -1, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if new_head[0] < 0 or new_head[0] >= NUM_CELLS or new_head[1] < 0 or new_head[1] >= NUM_CELLS:
            game_over = True
            continue

        snake.insert(0, new_head)

        if new_head == food:
            grow_snake = not grow_snake
            food = (random.randint(0, NUM_CELLS - 1), random.randint(0, NUM_CELLS - 1))
            while food in snake:
                food = (random.randint(0, NUM_CELLS - 1), random.randint(0, NUM_CELLS - 1))
            if not grow_snake:
                snake.pop()
        else:
            snake.pop()

        screen.fill(BLACK)
        for i, segment in enumerate(snake):
            if i == 0:
                head_position = (int(segment[1] * CELL_SIZE + CELL_SIZE // 2 - snake_head_img.get_width() / 2),
                                 int(segment[0] * CELL_SIZE + CELL_SIZE // 2 - snake_head_img.get_height() / 2))
                screen.blit(snake_head_img, head_position)
            else:
                draw_circle(GREEN, segment[0], segment[1])

        draw_circle(RED, food[0], food[1])
        pygame.display.update()
        clock.tick(FPS)

    display_game_over(screen, font)

# Start the game
game_loop()
pygame.quit()
