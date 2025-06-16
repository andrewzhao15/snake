import pygame
import sys
import random
from collections import deque

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Difficulty settings (frames per second)
DIFFICULTIES = {
    'Easy': 8,
    'Medium': 12,
    'Hard': 16
}

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def spawn_food(snake_body):
    while True:
        food = (random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1))
        if food not in snake_body:
            return food

# Set up the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = deque([(GRID_WIDTH // 2, GRID_HEIGHT // 2)])
        self.direction = (1, 0)  # Start moving right
        self.length = 1
        self.next_direction = self.direction
        self.growing = False
        self.alive = True
        self.difficulty = 'Medium'  # Default difficulty

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (self.direction[0] + new_direction[0], self.direction[1] + new_direction[1]) != (0, 0):
            self.next_direction = new_direction

    def move(self):
        if not self.alive:
            return

        # Update direction
        self.direction = self.next_direction
        
        # Get current head position
        head_x, head_y = self.body[0]
        
        # Calculate new head position
        new_head = (
            (head_x + self.direction[0]) % GRID_WIDTH,
            (head_y + self.direction[1]) % GRID_HEIGHT
        )
        
        # Check for collision with self
        if new_head in list(self.body)[1:]:
            self.alive = False
            return

        # Add new head
        self.body.appendleft(new_head)
        
        # Remove tail if not growing
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False
            self.length += 1

    def draw(self, screen):
        for segment in self.body:
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GREEN, rect)

def load_high_score():
    try:
        with open('highscore.txt', 'r') as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open('highscore.txt', 'w') as f:
        f.write(str(score))

def main():
    snake = Snake()
    food_position = spawn_food(snake.body)
    font = pygame.font.SysFont('arial', 24)
    high_score = load_high_score()
    show_difficulty_menu = True

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if show_difficulty_menu:
                    if event.key == pygame.K_1:
                        snake.difficulty = 'Easy'
                        show_difficulty_menu = False
                    elif event.key == pygame.K_2:
                        snake.difficulty = 'Medium'
                        show_difficulty_menu = False
                    elif event.key == pygame.K_3:
                        snake.difficulty = 'Hard'
                        show_difficulty_menu = False
                elif not snake.alive and event.key == pygame.K_SPACE:
                    snake.reset()
                    food_position = spawn_food(snake.body)
                    show_difficulty_menu = True

        # Handle keyboard input
        if snake.alive and not show_difficulty_menu:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                snake.change_direction((0, -1))
            elif keys[pygame.K_DOWN]:
                snake.change_direction((0, 1))
            elif keys[pygame.K_LEFT]:
                snake.change_direction((-1, 0))
            elif keys[pygame.K_RIGHT]:
                snake.change_direction((1, 0))
        
        # Move the snake
        snake.move()
        
        # Check if snake ate food
        if snake.alive and snake.body[0] == food_position:
            snake.growing = True
            food_position = spawn_food(snake.body)
        
        # Clear the screen
        screen.fill(BLACK)
        
        # Draw the food
        food_rect = pygame.Rect(
            food_position[0] * GRID_SIZE,
            food_position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, RED, food_rect)
        
        # Draw the snake
        snake.draw(screen)
        
        # Calculate current score
        current_score = snake.length - 1
        
        # Update high score if needed
        if current_score > high_score:
            high_score = current_score
            save_high_score(high_score)
        
        if show_difficulty_menu:
            # Draw difficulty selection menu
            title_text = font.render('Select Difficulty:', True, WHITE)
            easy_text = font.render('1 - Easy', True, WHITE)
            medium_text = font.render('2 - Medium', True, WHITE)
            hard_text = font.render('3 - Hard', True, WHITE)
            
            screen.blit(title_text, (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 - 60))
            screen.blit(easy_text, (WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2 - 20))
            screen.blit(medium_text, (WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2 + 10))
            screen.blit(hard_text, (WINDOW_WIDTH/2 - 50, WINDOW_HEIGHT/2 + 40))
        else:
            # Draw scores and difficulty
            score_text = font.render(f'Score: {current_score}', True, WHITE)
            high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
            difficulty_text = font.render(f'Difficulty: {snake.difficulty}', True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (10, 40))
            screen.blit(difficulty_text, (10, 70))
        
        # Draw game over message
        if not snake.alive:
            game_over_text = font.render('Game Over!', True, WHITE)
            final_score_text = font.render(f'Final Score: {current_score}', True, WHITE)
            restart_text = font.render('Press SPACE to restart', True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 40))
            final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 40))
            
            screen.blit(game_over_text, game_over_rect)
            screen.blit(final_score_text, final_score_rect)
            screen.blit(restart_text, restart_rect)
        
        # Update the display
        pygame.display.flip()
        
        # Control game speed based on difficulty
        clock.tick(DIFFICULTIES[snake.difficulty])

if __name__ == '__main__':
    main()
