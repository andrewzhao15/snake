# Snake Game Tests

This directory contains unit tests for the Snake game.

## Running Tests

1. Install the test dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

2. Run the tests with coverage:
   ```bash
   cd ..  # Navigate to the snake_game directory
   python -m pytest
   ```

## Test Structure

- `test_snake.py`: Contains tests for the Snake class and game functions
  - `TestSnake`: Tests for the Snake class
  - `TestGameFunctions`: Tests for utility functions like food spawning and high score handling

## Writing New Tests

1. Create a new test file named `test_*.py`
2. Write test classes that inherit from `unittest.TestCase`
3. Name test methods with `test_` prefix
4. Use assertions to verify expected behavior

## Coverage

Test coverage is automatically generated when running tests. To view the coverage report:

```bash
python -m pytest --cov=snake_game --cov-report=html
```

Then open `htmlcov/index.html` in a web browser.
