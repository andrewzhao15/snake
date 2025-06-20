import unittest
import os
import sys
import pygame
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import snake_game
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from snake_game import Snake, spawn_food, load_high_score, save_high_score

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
        snake_body = [(1, 1), (1, 2), (1, 3)]
        food = spawn_food(snake_body)
        self.assertNotIn(food, snake_body)
        
    def test_high_score_io(self):
        """Test saving and loading high score"""
        test_score = 42
        save_high_score(test_score)
        loaded_score = load_high_score()
        self.assertEqual(loaded_score, test_score)

if __name__ == '__main__':
    unittest.main()
