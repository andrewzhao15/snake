import unittest
import os
import sys
import pygame
import tempfile
from unittest.mock import patch, MagicMock, ANY

# Add the parent directory to the path so we can import snake_game
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from snake_game import Snake, spawn_food, load_high_score, save_high_score, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE

# Mock Pygame modules
pygame.display = MagicMock()
pygame.draw = MagicMock()
pygame.font = MagicMock()
pygame.time = MagicMock()
pygame.event = MagicMock()

class TestSnake(unittest.TestCase):
    def setUp(self):
        self.snake = Snake()
        
    def test_initial_state(self):
        """Test that the snake initializes with the correct state"""
        self.assertEqual(len(self.snake.body), 1)
        self.assertEqual(self.snake.direction, (1, 0))  # Initially moving right
        self.assertEqual(self.snake.grow, 0)
        
    def test_change_direction(self):
        """Test changing the snake's direction"""
        # Test valid direction changes
        self.snake.change_direction((0, -1))  # Up
        self.assertEqual(self.snake.direction, (0, -1))
        
        # Test invalid direction change (180-degree turn)
        self.snake.change_direction((0, 1))  # Down (invalid, opposite of current)
        self.assertEqual(self.snake.direction, (0, -1))  # Should not change
        
    def test_move(self):
        """Test snake movement"""
        initial_head = self.snake.body[0]
        self.snake.move()
        self.assertEqual(self.snake.body[0], (initial_head[0] + 1, initial_head[1]))
        
    def test_move_wrap_around(self):
        """Test snake wraps around screen edges"""
        # Move snake to right edge
        self.snake.body[0] = (WINDOW_WIDTH // GRID_SIZE - 1, 0)
        self.snake.direction = (1, 0)
        self.snake.move()
        self.assertEqual(self.snake.body[0], (0, 0))
        
        # Move snake to left edge
        self.snake.body[0] = (0, 0)
        self.snake.direction = (-1, 0)
        self.snake.move()
        self.assertEqual(self.snake.body[0][0], (WINDOW_WIDTH // GRID_SIZE) - 1)
        
    def test_collision_detection(self):
        """Test snake collision with itself"""
        # Create a snake with 3 segments
        self.snake.body = [(5, 5), (5, 6), (5, 7)]
        # Move to collide with body
        self.snake.direction = (0, -1)
        self.snake.move()
        self.assertTrue(self.snake.check_collision())
        
    @patch('pygame.draw.rect')
    def test_draw(self, mock_draw):
        """Test snake drawing"""
        self.snake.body = [(1, 1), (1, 2)]
        mock_screen = MagicMock()
        self.snake.draw(mock_screen)
        self.assertEqual(mock_draw.call_count, 2)  # Should draw head and body segments
        
    def test_grow(self):
        """Test that the snake grows when it should"""
        initial_length = len(self.snake.body)
        self.snake.grow = 3
        self.snake.move()
        self.assertEqual(len(self.snake.body), initial_length + 3)
        self.assertEqual(self.snake.grow, 0)

class TestGameFunctions(unittest.TestCase):
    def test_spawn_food(self):
        """Test that food spawns in a valid position"""
        # Test with empty snake
        food = spawn_food([])
        self.assertIsInstance(food, tuple)
        self.assertEqual(len(food), 2)
        
        # Test with snake occupying some positions
        snake_body = [(1, 1), (1, 2), (1, 3)]
        food = spawn_food(snake_body)
        self.assertNotIn(food, snake_body)
        
        # Test with nearly full board
        full_board = [(x, y) for x in range(10) for y in range(10)]
        with self.assertRaises(ValueError):
            spawn_food(full_board)
        
    def test_high_score_io(self):
        """Test saving and loading high score"""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            
        # Patch the high score file path
        with patch('snake_game.HIGH_SCORE_FILE', temp_path):
            try:
                test_score = 42
                save_high_score(test_score)
                loaded_score = load_high_score()
                self.assertEqual(loaded_score, test_score)
                
                # Test with non-existent file
                os.unlink(temp_path)
                self.assertEqual(load_high_score(), 0)
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

if __name__ == '__main__':
    unittest.main()
