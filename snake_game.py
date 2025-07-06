import pygame
import sys
import random

# Game settings
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        if new_head in self.positions:
            return False  # Collision with self
        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, new_dir):
        # Prevent reversing
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def eat(self):
        self.grow = True

    def head(self):
        return self.positions[0]

class Food:
    def __init__(self, snake_positions):
        self.position = self.random_position(snake_positions)

    def random_position(self, snake_positions):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_positions:
                return pos

def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, BLACK, (0, y), (SCREEN_WIDTH, y))

def draw_snake(surface, snake):
    for i, pos in enumerate(snake.positions):
        x, y = pos[0]*CELL_SIZE, pos[1]*CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        # Gradient effect for 3D look
        color1 = (0, 200, 0)
        color2 = (0, 100, 0)
        for j in range(CELL_SIZE):
            blend = j / CELL_SIZE
            r = int(color1[0] * (1-blend) + color2[0] * blend)
            g = int(color1[1] * (1-blend) + color2[1] * blend)
            b = int(color1[2] * (1-blend) + color2[2] * blend)
            pygame.draw.line(surface, (r, g, b), (x, y+j), (x+CELL_SIZE-1, y+j))
        # Outline
        pygame.draw.rect(surface, (0, 80, 0), rect, 2)
        # Head highlight
        if i == 0:
            pygame.draw.ellipse(surface, (180, 255, 180), rect.inflate(-CELL_SIZE//3, -CELL_SIZE//3))

def draw_food(surface, food):
    x, y = food.position[0]*CELL_SIZE, food.position[1]*CELL_SIZE
    center = (x + CELL_SIZE//2, y + CELL_SIZE//2)
    radius = CELL_SIZE//2 - 2
    # Draw main food body
    pygame.draw.circle(surface, (220, 30, 30), center, radius)
    # Draw highlight for 3D effect
    highlight_center = (center[0] - radius//3, center[1] - radius//3)
    pygame.draw.circle(surface, (255, 180, 180), highlight_center, radius//3)
def draw_food(surface, food):
    rect = pygame.Rect(food.position[0]*CELL_SIZE, food.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, RED, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food(snake.positions)
    score = 0

    # Start with a slow speed
    fps = 6  # Start slower than default

    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        if not snake.move():
            print(f"Game Over! Your score: {score}")
            running = False
            continue

        if snake.head() == food.position:
            snake.eat()
            score += 1
            food = Food(snake.positions)
            # Increase speed as score increases, up to a max
            fps = min(25, 6 + score // 2)

        screen.fill(WHITE)
        draw_grid(screen)
        draw_snake(screen, snake)
        draw_food(screen, food)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def new_func():
    running = True

if __name__ == "__main__":
    main()