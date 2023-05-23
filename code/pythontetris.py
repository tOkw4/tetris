import pygame
import random


pygame.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")


clock = pygame.time.Clock()

# Define the shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Define the colors for each Tetromino shape
COLORS = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE]

# Set up the grid
GRID_WIDTH = 10
GRID_HEIGHT = 20
grid = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Set up the current Tetromino
current_shape = random.choice(SHAPES)
current_color = random.choice(COLORS)
floor = GRID_WIDTH // 2 - len(current_shape[0]) // 2
top = 0

# Set up the next Tetromino
next_block = random.choice(SHAPES)

# Set up the hold block
hold_block = None

# Function to check if a position is valid
def is_valid_position(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] and (
                x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col] != BLACK
            ):
                return False
    return True

# Function to check if the current position is a collision
def is_collision(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] and (
                x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col] != BLACK
            ):
                return True
    return False

# Function to merge the current Tetromino with the grid
def merge_tetromino_with_grid():
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col]:
                grid[top + row][floor + col] = current_color

# Function to remove completed rows from the grid
def remove_completed_rows():
    global completed_rows
    completed_rows = []
    for row in range(GRID_HEIGHT):
        if all(cell != BLACK for cell in grid[row]):
            completed_rows.append(row)
    for row in completed_rows:
        del grid[row]
        grid.insert(0, [BLACK] * GRID_WIDTH)

# Function to update the score
def update_score(rows_cleared):
    global score
    score += rows_cleared * rows_cleared

# Function to store the score in a file
def store_score(score):
    with open("scores.txt", "a") as file:
        file.write(str(score) + "\n")

# Function to display the highest score
def display_highest_score():
    highest_score = 0
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
            for score in scores:
                score = int(score.strip())
                if score > highest_score:
                    highest_score = score
    except FileNotFoundError:
        pass

    font = pygame.font.Font(None, 30)
    text = font.render("Highest Score: " + str(highest_score), True, WHITE)
    window.blit(text, (20, 20))

# Function to display the game over screen
def display_game_over():
    font = pygame.font.Font(None, 80)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    window.blit(text, text_rect)

# Function to display the Tetromino grid
def display_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            pygame.draw.rect(
                window,
                grid[row][col],
                (grid_x + col * CELL_SIZE, grid_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
            pygame.draw.rect(
                window,
                GRAY,
                (grid_x + col * CELL_SIZE, grid_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1,
            )

# Function to display the current Tetromino
def display_current_tetromino():
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col]:
                pygame.draw.rect(window,current_color,(grid_x + (floor + col) * CELL_SIZE, grid_y + (top + row) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(window,GRAY,(grid_x + (floor + col) * CELL_SIZE, grid_y + (top + row) * CELL_SIZE, CELL_SIZE, CELL_SIZE),1)

# Function to display the shadow block
def display_shadow_block():
    shadow_y = top
    while not is_collision(current_shape, floor, shadow_y + 1):
        shadow_y += 1
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col]:
                pygame.draw.rect(window,GRAY,(grid_x + (floor + col) * CELL_SIZE, grid_y + (shadow_y + row) * CELL_SIZE, CELL_SIZE, CELL_SIZE),3)

# Function to display the next block
def display_next_block():
    font = pygame.font.Font(None, 30)
    text = font.render("Next Block:", True, WHITE)
    window.blit(text, (grid_x + GRID_WIDTH * CELL_SIZE + 20, 100))
    for row in range(len(next_block)):
        for col in range(len(next_block[row])):
            if next_block[row][col]:
                pygame.draw.rect(window,COLORS[random.randint(0, len(COLORS) - 1)],(grid_x + GRID_WIDTH * CELL_SIZE + 20 + col * CELL_SIZE,150 + row * CELL_SIZE,CELL_SIZE,CELL_SIZE))
                pygame.draw.rect(window,GRAY,(grid_x + GRID_WIDTH * CELL_SIZE + 20 + col * CELL_SIZE,150 + row * CELL_SIZE,CELL_SIZE,CELL_SIZE),1)

# Function to display the hold block
def display_hold_block():
    font = pygame.font.Font(None, 30)
    text = font.render("Hold Block:", True, WHITE)
    window.blit(text, (grid_x - 120, 100))
    if hold_block:
        for row in range(len(hold_block)):
            for col in range(len(hold_block[row])): 
                if hold_block[row][col]:
                    pygame.draw.rect(window,COLORS[random.randint(0, len(COLORS) - 1)],(grid_x - 120 + col * CELL_SIZE,150 + row * CELL_SIZE,CELL_SIZE,CELL_SIZE))
                    pygame.draw.rect(window,GRAY,(grid_x - 120 + col * CELL_SIZE, 150 + row * CELL_SIZE, CELL_SIZE, CELL_SIZE),1)

# Game loop
game_over = False
score = 0
completed_rows = []

while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if is_valid_position(current_shape, floor - 1, top):
                    floor -= 1
            elif event.key == pygame.K_RIGHT:
                if is_valid_position(current_shape, floor + 1, top):
                    floor += 1
            elif event.key == pygame.K_DOWN:
                if is_valid_position(current_shape, floor, top + 1):
                    top += 1
            elif event.key == pygame.K_UP:
                rotated_shape = [[current_shape[col][row] for col in range(len(current_shape))] for row in range(len(current_shape[0]) - 1, -1, -1)]
                if is_valid_position(rotated_shape, floor, top):
                    current_shape = rotated_shape
            elif event.key == pygame.K_SPACE:
                while is_valid_position(current_shape, floor, top + 1):
                    top += 1
                merge_tetromino_with_grid()
                remove_completed_rows()
                update_score(len(completed_rows))
                current_shape = next_block
                current_color = random.choice(COLORS)
                floor = GRID_WIDTH // 2 - len(current_shape[0]) // 2
                top = 0
                next_block = random.choice(SHAPES)
            elif event.key == pygame.K_c:
                if not hold_block:
                    hold_block = current_shape
                    current_shape = next_block
                    current_color = random.choice(COLORS)
                    floor = GRID_WIDTH // 2 - len(current_shape[0]) // 2
                    top = 0
                    next_block = random.choice(SHAPES)
                else:
                    hold_block, current_shape = current_shape, hold_block
                    floor = GRID_WIDTH // 2 - len(current_shape[0]) // 2
                    top = 0

    # Update game state

    if is_valid_position(current_shape, floor, top + 1):
        top += 1
    else:
        if top <= 0:
            game_over = True
        merge_tetromino_with_grid()
        remove_completed_rows()
        update_score(len(completed_rows))
        if not game_over:
            current_shape = next_block
            current_color = random.choice(COLORS)
            floor = GRID_WIDTH // 2 - len(current_shape[0]) // 2
            top = 0
            next_block = random.choice(SHAPES)


    # Clear the window
    window.fill(BLACK)

    # Display the grid
    CELL_SIZE = 30
    grid_x = (WINDOW_WIDTH - GRID_WIDTH * CELL_SIZE) // 2
    grid_y = WINDOW_HEIGHT - GRID_HEIGHT * CELL_SIZE - 20
    display_grid()

    # Display the current Tetromino
    display_current_tetromino()

    # Display the shadow block
    display_shadow_block()

    # Display the next block
    display_next_block()

    # Display the hold block
    display_hold_block()

    # Display the score
    font = pygame.font.Font(None, 30)
    text = font.render("Score: " + str(score), True, WHITE)
    window.blit(text, (grid_x + GRID_WIDTH * CELL_SIZE + 20, 20))

    # Display the highest score
    display_highest_score()

    # Check if game over
    if game_over:
        display_game_over()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(10)

# Store the score
store_score(score)

# Quit the game
pygame.quit()
