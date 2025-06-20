# Snake Game

A classic Snake game implementation in Python using Pygame.

## Features

- Classic snake gameplay with score tracking
- Multiple difficulty levels
- High score persistence
- Comprehensive test suite
- CI/CD pipeline with GitHub Actions

## Prerequisites

- Python 3.8+
- Pygame
- pytest (for running tests)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/andrewzhao15/windsurf-test.git
   cd windsurf-test/snake_game
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python snake_game.py
```

### Controls
- Arrow keys to change direction
- ESC to quit
- P to pause
- R to restart
- 1, 2, 3 to change difficulty

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
cd snake_game
python -m pytest
```

For test coverage report:
```bash
python -m pytest --cov=snake_game --cov-report=html
open htmlcov/index.html  # View coverage report
```

## CI/CD

This project uses GitHub Actions for continuous integration. The workflow:

1. Runs on all pushes to `main` and `demo-branch`
2. Runs on all pull requests to `main`
3. Executes the test suite
4. Uploads coverage reports to Codecov

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
