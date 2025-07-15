import pytest
import sys
import os
from unittest.mock import patch, mock_open, MagicMock
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "snake_game"))

with patch.dict(
    "sys.modules",
    {
        "pygame": MagicMock(),
        "pygame.display": MagicMock(),
        "pygame.font": MagicMock(),
        "pygame.time": MagicMock(),
        "pygame.draw": MagicMock(),
    },
):
    import snake_game


class TestSnakeGame:
    """Test suite for the Snake game functionality."""

    def test_constants(self):
        """Test that game constants are properly defined."""
        assert snake_game.WINDOW_WIDTH == 800
        assert snake_game.WINDOW_HEIGHT == 600
        assert snake_game.GRID_SIZE == 20
        assert snake_game.GRID_WIDTH == 40
        assert snake_game.GRID_HEIGHT == 30

    def test_difficulties(self):
        """Test that difficulty settings are properly configured."""
        expected_difficulties = {"Easy": 8, "Medium": 12, "Hard": 16}
        assert snake_game.DIFFICULTIES == expected_difficulties

    def test_colors(self):
        """Test that color constants are properly defined."""
        assert snake_game.BLACK == (0, 0, 0)
        assert snake_game.GREEN == (0, 255, 0)
        assert snake_game.RED == (255, 0, 0)
        assert snake_game.WHITE == (255, 255, 255)


class TestSnake:
    """Test suite for the Snake class."""

    def test_snake_initialization(self):
        """Test Snake class initialization."""
        snake = snake_game.Snake()

        expected_center = (snake_game.GRID_WIDTH // 2, snake_game.GRID_HEIGHT // 2)
        assert snake.body[0] == expected_center
        assert len(snake.body) == 1

        assert snake.direction == (1, 0)
        assert snake.length == 1
        assert snake.next_direction == snake.direction
        assert snake.growing is False
        assert snake.alive is True
        assert snake.difficulty == "Medium"

    def test_snake_reset(self):
        """Test Snake reset functionality."""
        snake = snake_game.Snake()

        snake.body.append((10, 10))
        snake.direction = (0, 1)
        snake.length = 5
        snake.growing = True
        snake.alive = False
        snake.difficulty = "Hard"

        snake.reset()
        expected_center = (snake_game.GRID_WIDTH // 2, snake_game.GRID_HEIGHT // 2)
        assert snake.body[0] == expected_center
        assert len(snake.body) == 1
        assert snake.direction == (1, 0)
        assert snake.length == 1
        assert snake.next_direction == snake.direction
        assert snake.growing is False
        assert snake.alive is True
        assert snake.difficulty == "Medium"

    def test_change_direction_valid(self):
        """Test valid direction changes."""
        snake = snake_game.Snake()

        snake.change_direction((0, -1))
        assert snake.next_direction == (0, -1)

        snake.change_direction((0, 1))
        assert snake.next_direction == (0, 1)

    def test_change_direction_invalid_180_turn(self):
        """Test that 180-degree turns are prevented."""
        snake = snake_game.Snake()
        original_direction = snake.direction

        snake.change_direction((-1, 0))
        assert snake.next_direction == original_direction

    def test_snake_movement_basic(self):
        """Test basic snake movement."""
        snake = snake_game.Snake()
        original_head = snake.body[0]

        snake.move()

        new_head = snake.body[0]
        expected_head = (original_head[0] + 1, original_head[1])
        assert new_head == expected_head
        assert len(snake.body) == 1

    def test_snake_movement_with_growth(self):
        """Test snake movement when growing."""
        snake = snake_game.Snake()
        original_length = len(snake.body)

        snake.growing = True
        snake.move()

        assert len(snake.body) == original_length + 1
        assert snake.length == 2
        assert snake.growing is False

    def test_snake_wrapping(self):
        """Test that snake wraps around screen edges."""
        snake = snake_game.Snake()

        snake.body = deque([(snake_game.GRID_WIDTH - 1, 10)])
        snake.direction = (1, 0)
        snake.next_direction = (1, 0)

        snake.move()

        assert snake.body[0] == (0, 10)

    def test_snake_self_collision(self):
        """Test snake collision with itself."""
        snake = snake_game.Snake()

        snake.body = deque([(5, 5), (4, 5), (3, 5)])
        snake.direction = (-1, 0)
        snake.next_direction = (-1, 0)

        snake.move()

        assert snake.alive is False

    def test_snake_no_movement_when_dead(self):
        """Test that dead snake doesn't move."""
        snake = snake_game.Snake()
        snake.alive = False
        original_body = list(snake.body)

        snake.move()

        assert list(snake.body) == original_body


class TestFoodSpawning:
    """Test suite for food spawning functionality."""

    @patch("snake_game.random.randint")
    def test_spawn_food_empty_grid(self, mock_randint):
        """Test food spawning on empty grid."""
        mock_randint.side_effect = [10, 15]

        snake_body = deque([(5, 5)])
        food_position = snake_game.spawn_food(snake_body)

        assert food_position == (10, 15)

    @patch("snake_game.random.randint")
    def test_spawn_food_avoids_snake(self, mock_randint):
        """Test that food doesn't spawn on snake body."""
        mock_randint.side_effect = [5, 5, 10, 15]

        snake_body = deque([(5, 5), (4, 5)])
        food_position = snake_game.spawn_food(snake_body)

        assert food_position == (10, 15)
        assert food_position not in snake_body


class TestHighScore:
    """Test suite for high score functionality."""

    def test_load_high_score_file_exists(self):
        """Test loading high score when file exists."""
        mock_file_content = "42"

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            score = snake_game.load_high_score()
            assert score == 42

    def test_load_high_score_file_not_exists(self):
        """Test loading high score when file doesn't exist."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            score = snake_game.load_high_score()
            assert score == 0

    def test_load_high_score_invalid_content(self):
        """Test loading high score with invalid file content."""
        mock_file_content = "invalid"

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            score = snake_game.load_high_score()
            assert score == 0

    def test_save_high_score(self):
        """Test saving high score to file."""
        mock_file = mock_open()

        with patch("builtins.open", mock_file):
            snake_game.save_high_score(100)

        mock_file.assert_called_once_with("highscore.txt", "w")
        mock_file().write.assert_called_once_with("100")


class TestGameIntegration:
    """Integration tests for game components working together."""

    def test_snake_eating_food_integration(self):
        """Test the integration of snake eating food."""
        snake = snake_game.Snake()

        next_pos = (snake.body[0][0] + 1, snake.body[0][1])

        snake.growing = True
        original_length = len(snake.body)

        snake.move()

        assert len(snake.body) == original_length + 1
        assert snake.length == original_length + 1
        assert snake.growing is False

    def test_difficulty_settings_integration(self):
        """Test that difficulty settings are properly integrated."""
        snake = snake_game.Snake()

        for difficulty, expected_fps in snake_game.DIFFICULTIES.items():
            snake.difficulty = difficulty
            assert snake.difficulty == difficulty
            assert snake_game.DIFFICULTIES[difficulty] == expected_fps


if __name__ == "__main__":
    pytest.main([__file__])
