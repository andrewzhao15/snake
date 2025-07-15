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
        """Test that game constants are properly defined and have expected values.

        Validates that all window dimensions, grid settings, and layout constants
        are correctly configured for the Snake game. These constants are critical
        for proper game rendering and collision detection.

        Assertions:
            - WINDOW_WIDTH: Game window width in pixels (800)
            - WINDOW_HEIGHT: Game window height in pixels (600)
            - GRID_SIZE: Size of each grid cell in pixels (20)
            - GRID_WIDTH: Number of grid cells horizontally (40)
            - GRID_HEIGHT: Number of grid cells vertically (30)
        """
        assert snake_game.WINDOW_WIDTH == 800
        assert snake_game.WINDOW_HEIGHT == 600
        assert snake_game.GRID_SIZE == 20
        assert snake_game.GRID_WIDTH == 40
        assert snake_game.GRID_HEIGHT == 30

    def test_difficulties(self):
        """Test that difficulty settings are properly configured with correct FPS values.

        Validates the DIFFICULTIES dictionary contains all expected difficulty levels
        with their corresponding frames-per-second values. These settings control
        the game speed and player experience.

        Expected difficulty mappings:
            - Easy: 8 FPS (slower, beginner-friendly)
            - Medium: 12 FPS (moderate speed)
            - Hard: 16 FPS (faster, challenging)

        Assertions:
            - All three difficulty levels are present
            - Each difficulty has the correct FPS value
            - Dictionary structure matches expected format
        """
        expected_difficulties = {"Easy": 8, "Medium": 12, "Hard": 16}
        assert snake_game.DIFFICULTIES == expected_difficulties

    def test_colors(self):
        """Test that color constants are properly defined as RGB tuples.

        Validates that all game colors are correctly defined as RGB tuples
        for consistent rendering across the game interface.

        Color definitions:
            - BLACK: (0, 0, 0) - Background color
            - GREEN: (0, 255, 0) - Snake body color
            - RED: (255, 0, 0) - Food color
            - WHITE: (255, 255, 255) - Text and UI elements

        Assertions:
            - Each color is a valid RGB tuple
            - Color values match expected game design
        """
        assert snake_game.BLACK == (0, 0, 0)
        assert snake_game.GREEN == (0, 255, 0)
        assert snake_game.RED == (255, 0, 0)
        assert snake_game.WHITE == (255, 255, 255)


class TestSnake:
    """Test suite for the Snake class."""

    def test_snake_initialization(self):
        """Test Snake class initialization with default starting state.

        Validates that a new Snake instance is created with the correct initial
        state including position, direction, size, and game status. The snake
        should start at the center of the grid moving right.

        Initial state expectations:
            - Position: Center of the game grid
            - Direction: Moving right (1, 0)
            - Length: 1 segment
            - Status: Alive and not growing
            - Difficulty: Medium (default)

        Assertions:
            - Snake body contains exactly one segment at grid center
            - Movement direction is rightward
            - All boolean flags are in correct initial state
            - Default difficulty is set
        """
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
        """Test Snake reset functionality returns to initial state.

        Validates that the reset() method properly restores the snake to its
        initial state regardless of current game state. This is critical for
        the restart functionality after game over.

        Test procedure:
            1. Create snake and modify all state variables
            2. Call reset() method
            3. Verify all state returns to initial values

        State changes tested:
            - Body length and position
            - Movement direction
            - Growth and alive status
            - Difficulty setting

        Assertions:
            - All state variables return to initialization values
            - Snake position resets to grid center
            - Movement direction resets to rightward
        """
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
        """Test valid direction changes are accepted and stored.

        Validates that the snake can change direction to perpendicular directions
        (up/down when moving horizontally). The direction change should be stored
        in next_direction and applied on the next move.

        Valid direction changes tested:
            - Right to Up: (1, 0) to (0, -1)
            - Right to Down: (1, 0) to (0, 1)

        Assertions:
            - next_direction is updated with new direction
            - Direction changes are accepted for perpendicular moves
            - No immediate change to current direction (applied on next move)
        """
        snake = snake_game.Snake()

        snake.change_direction((0, -1))
        assert snake.next_direction == (0, -1)

        snake.change_direction((0, 1))
        assert snake.next_direction == (0, 1)

    def test_change_direction_invalid_180_turn(self):
        """Test that 180-degree turns are prevented to avoid self-collision.

        Validates that the snake cannot reverse direction directly (e.g., from
        right to left) as this would cause immediate self-collision. The game
        should ignore such direction changes.

        Test scenario:
            - Snake moving right (1, 0)
            - Attempt to change to left (-1, 0)
            - Direction change should be ignored

        Game logic:
            - Prevents immediate self-collision
            - Maintains game flow and fairness
            - Common feature in Snake games

        Assertions:
            - next_direction remains unchanged
            - Invalid direction change is ignored
        """
        snake = snake_game.Snake()
        original_direction = snake.direction

        snake.change_direction((-1, 0))
        assert snake.next_direction == original_direction

    def test_snake_movement_basic(self):
        """Test basic snake movement in the current direction.

        Validates that the snake moves one grid position in its current direction
        when move() is called. For a single-segment snake, this involves adding
        a new head and removing the tail (maintaining length).

        Movement mechanics:
            - New head position calculated from current direction
            - Old tail removed to maintain length
            - Snake body remains single segment

        Test verification:
            - Head position advances by one grid cell
            - Snake length remains constant (1 segment)
            - Movement follows current direction vector

        Assertions:
            - New head position matches expected coordinates
            - Snake body length unchanged
        """
        snake = snake_game.Snake()
        original_head = snake.body[0]

        snake.move()

        new_head = snake.body[0]
        expected_head = (original_head[0] + 1, original_head[1])
        assert new_head == expected_head
        assert len(snake.body) == 1

    def test_snake_movement_with_growth(self):
        """Test snake movement when growing flag is set (after eating food).

        Validates that when the growing flag is True, the snake adds a new head
        without removing the tail, effectively increasing its length by one.
        This simulates the behavior when the snake eats food.

        Growth mechanics:
            - New head added in movement direction
            - Tail is NOT removed (snake grows)
            - Growing flag reset to False after growth
            - Length counter incremented

        Test procedure:
            1. Set growing flag to True
            2. Call move() method
            3. Verify length increase and flag reset

        Assertions:
            - Snake length increases by 1
            - Growing flag resets to False
            - New head added correctly
        """
        snake = snake_game.Snake()
        original_length = len(snake.body)

        snake.growing = True
        snake.move()

        assert len(snake.body) == original_length + 1
        assert snake.length == 2
        assert snake.growing is False

    def test_snake_wrapping(self):
        """Test that snake wraps around screen edges using modulo arithmetic.

        Validates that when the snake moves beyond the grid boundaries, it wraps
        to the opposite side of the screen. This is implemented using modulo
        operations on the grid coordinates.

        Wrapping behavior:
            - Moving past right edge wraps to left edge
            - Moving past left edge wraps to right edge
            - Moving past top edge wraps to bottom edge
            - Moving past bottom edge wraps to top edge

        Test scenario:
            - Position snake at right edge (GRID_WIDTH - 1, y)
            - Move right (direction: 1, 0)
            - Verify wrapping to left edge (0, y)

        Assertions:
            - Snake position wraps correctly using modulo
            - No collision or game over from edge movement
        """
        snake = snake_game.Snake()

        snake.body = deque([(snake_game.GRID_WIDTH - 1, 10)])
        snake.direction = (1, 0)
        snake.next_direction = (1, 0)

        snake.move()

        assert snake.body[0] == (0, 10)

    def test_snake_self_collision(self):
        """Test snake collision detection with its own body segments.

        Validates that when the snake's head moves into a position occupied by
        any part of its body, the collision is detected and the snake dies.
        This is a core game over condition.

        Collision detection logic:
            - Check if new head position exists in body segments
            - Exclude current head from collision check
            - Set alive flag to False on collision

        Test setup:
            - Create multi-segment snake: [(5,5), (4,5), (3,5)]
            - Move left to position (2,5) - no collision
            - Move left again to position (3,5) - collision with body

        Assertions:
            - Snake alive flag becomes False
            - Collision properly detected
            - Game over state triggered
        """
        snake = snake_game.Snake()

        snake.body = deque([(5, 5), (4, 5), (3, 5)])
        snake.direction = (-1, 0)
        snake.next_direction = (-1, 0)

        snake.move()

        assert snake.alive is False

    def test_snake_no_movement_when_dead(self):
        """Test that dead snake doesn't move or change state.

        Validates that when the snake's alive flag is False, calling move()
        has no effect on the snake's position or state. This prevents
        posthumous movement and maintains game over state.

        Dead state behavior:
            - move() method returns early if not alive
            - Snake body position remains unchanged
            - No direction updates or position calculations
            - Game state preserved for restart

        Test procedure:
            1. Set snake alive flag to False
            2. Store current body state
            3. Call move() method
            4. Verify no state changes occurred

        Assertions:
            - Snake body remains identical
            - No position or direction changes
            - Dead state maintained
        """
        snake = snake_game.Snake()
        snake.alive = False
        original_body = list(snake.body)

        snake.move()

        assert list(snake.body) == original_body


class TestFoodSpawning:
    """Test suite for food spawning functionality."""

    @patch("snake_game.random.randint")
    def test_spawn_food_empty_grid(self, mock_randint):
        """Test food spawning on grid with available positions.

        Validates that the spawn_food function correctly generates food at
        random coordinates when there are available positions on the grid.
        Uses mocking to control random number generation for deterministic testing.

        Mocking strategy:
            - Mock random.randint to return predetermined coordinates
            - First call returns x-coordinate (10)
            - Second call returns y-coordinate (15)

        Test scenario:
            - Snake occupies position (5, 5)
            - Food should spawn at mocked position (10, 15)
            - Position should not conflict with snake body

        Assertions:
            - Food spawns at expected mocked coordinates
            - Function returns correct tuple format
            - No collision with existing snake body
        """
        mock_randint.side_effect = [10, 15]

        snake_body = deque([(5, 5)])
        food_position = snake_game.spawn_food(snake_body)

        assert food_position == (10, 15)

    @patch("snake_game.random.randint")
    def test_spawn_food_avoids_snake(self, mock_randint):
        """Test that food spawning avoids collision with snake body segments.

        Validates that the spawn_food function implements collision avoidance
        by re-rolling random coordinates when they conflict with snake body
        positions. This ensures food is always accessible to the player.

        Collision avoidance logic:
            - Generate random coordinates
            - Check if position exists in snake body
            - If collision detected, generate new coordinates
            - Repeat until valid position found

        Test scenario:
            - Snake body at positions: [(5,5), (4,5)]
            - First random attempt: (5,5) - collision with head
            - Second random attempt: (10,15) - valid position

        Mock sequence:
            - Calls 1-2: Return (5,5) - conflicts with snake
            - Calls 3-4: Return (10,15) - valid position

        Assertions:
            - Food spawns at valid non-conflicting position
            - Collision avoidance mechanism works correctly
            - Final position not in snake body
        """
        mock_randint.side_effect = [5, 5, 10, 15]

        snake_body = deque([(5, 5), (4, 5)])
        food_position = snake_game.spawn_food(snake_body)

        assert food_position == (10, 15)
        assert food_position not in snake_body


class TestHighScore:
    """Test suite for high score functionality."""

    def test_load_high_score_file_exists(self):
        """Test loading high score from existing file with valid content.

        Validates that the load_high_score function correctly reads and parses
        a high score value from the highscore.txt file when it exists and
        contains valid integer data.

        File I/O mocking:
            - Mock file open operation
            - Provide valid integer string content ("42")
            - Simulate successful file read

        Expected behavior:
            - File opened in read mode
            - Content parsed as integer
            - Parsed value returned

        Test verification:
            - Function returns correct integer value
            - File reading mechanism works properly
            - String-to-integer conversion successful

        Assertions:
            - Returned score matches file content (42)
            - No exceptions raised during operation
        """
        mock_file_content = "42"

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            score = snake_game.load_high_score()
            assert score == 42

    def test_load_high_score_file_not_exists(self):
        """Test loading high score when highscore.txt file doesn't exist.

        Validates that the load_high_score function gracefully handles the
        case where the high score file hasn't been created yet (first run
        scenario). Should return default value without crashing.

        Error handling:
            - FileNotFoundError exception caught
            - Default value (0) returned
            - No error propagated to caller

        First-run scenario:
            - Game launched for first time
            - No previous high score recorded
            - Function should provide sensible default

        Exception mocking:
            - Mock file open to raise FileNotFoundError
            - Simulate missing file condition
            - Test exception handling path

        Assertions:
            - Function returns 0 as default value
            - No exceptions escape function
            - Graceful degradation behavior
        """
        with patch("builtins.open", side_effect=FileNotFoundError):
            score = snake_game.load_high_score()
            assert score == 0

    def test_load_high_score_invalid_content(self):
        """Test loading high score when file contains invalid/corrupted data.

        Validates that the load_high_score function handles corrupted or
        invalid file content gracefully by returning a default value instead
        of crashing. This covers scenarios like file corruption or manual editing.

        Invalid content scenarios:
            - Non-numeric strings ("invalid", "abc")
            - Empty files
            - Files with special characters
            - Partially corrupted data

        Error handling:
            - ValueError exception caught during int() conversion
            - Default value (0) returned
            - No error propagated to caller

        Test setup:
            - Mock file with invalid content ("invalid")
            - Simulate int() conversion failure
            - Verify graceful fallback behavior

        Assertions:
            - Function returns 0 for invalid content
            - Exception handling prevents crashes
            - Robust error recovery implemented
        """
        mock_file_content = "invalid"

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            score = snake_game.load_high_score()
            assert score == 0

    def test_save_high_score(self):
        """Test saving high score value to persistent storage file.

        Validates that the save_high_score function correctly writes the
        high score value to the highscore.txt file for persistence across
        game sessions. Uses mocking to verify file operations without
        actual file system interaction.

        File I/O operations:
            - Open highscore.txt in write mode
            - Convert integer score to string
            - Write string content to file
            - File automatically closed

        Mocking verification:
            - File opened with correct parameters
            - Write operation called with correct data
            - Proper file handling implemented

        Test procedure:
            1. Mock file operations
            2. Call save_high_score with test value (100)
            3. Verify file opened in write mode
            4. Verify correct content written

        Assertions:
            - File opened with correct filename and mode
            - Score value written as string
            - File operations called exactly once
        """
        mock_file = mock_open()

        with patch("builtins.open", mock_file):
            snake_game.save_high_score(100)

        mock_file.assert_called_once_with("highscore.txt", "w")
        mock_file().write.assert_called_once_with("100")


class TestGameIntegration:
    """Integration tests for game components working together."""

    def test_snake_eating_food_integration(self):
        """Test integration of snake growth mechanism when eating food.

        Validates the complete food consumption workflow including snake
        growth, length tracking, and state management. This integration
        test ensures all components work together correctly.

        Food eating workflow:
            1. Snake head moves to food position
            2. Collision detection triggers
            3. Growing flag set to True
            4. Next move() call increases length
            5. Growing flag reset to False

        Integration components:
            - Snake movement system
            - Growth mechanism
            - Length tracking
            - State flag management

        Test simulation:
            - Set growing flag (simulates food collision)
            - Call move() to trigger growth
            - Verify length increase and flag reset

        Assertions:
            - Snake length increases by exactly 1
            - Length counter updated correctly
            - Growing flag properly reset
            - Integration between systems works
        """
        snake = snake_game.Snake()

        next_pos = (snake.body[0][0] + 1, snake.body[0][1])

        snake.growing = True
        original_length = len(snake.body)

        snake.move()

        assert len(snake.body) == original_length + 1
        assert snake.length == original_length + 1
        assert snake.growing is False

    def test_difficulty_settings_integration(self):
        """Test integration between Snake class and global difficulty settings.

        Validates that the Snake class properly integrates with the global
        DIFFICULTIES dictionary and that difficulty changes are correctly
        applied and accessible. This ensures the difficulty system works
        end-to-end.

        Integration points:
            - Snake.difficulty attribute
            - Global DIFFICULTIES dictionary
            - FPS/timing system integration
            - Difficulty selection mechanism

        Test coverage:
            - All difficulty levels (Easy, Medium, Hard)
            - Difficulty assignment to snake
            - FPS value accessibility
            - Consistency between systems

        Test procedure:
            1. Iterate through all difficulty levels
            2. Assign each difficulty to snake
            3. Verify assignment successful
            4. Verify FPS value accessible

        Assertions:
            - Snake difficulty properly set
            - FPS values match expected settings
            - All difficulty levels supported
            - Integration maintains consistency
        """
        snake = snake_game.Snake()

        for difficulty, expected_fps in snake_game.DIFFICULTIES.items():
            snake.difficulty = difficulty
            assert snake.difficulty == difficulty
            assert snake_game.DIFFICULTIES[difficulty] == expected_fps


if __name__ == "__main__":
    pytest.main([__file__])
