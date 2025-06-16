---
description: Python Code Formatting with Black
---

## Setup Instructions

1. Install Black:
   ```bash
   pip3 install black
   ```

2. Create a `pyproject.toml` file in your project root:
   ```toml
   [tool.black]
   line-length = 88
   target-version = ['py39']
   include = '\.pyi?$'
   ```

## Usage

- Format all Python files:
  ```bash
  black .
  ```

- Check formatting without making changes:
  ```bash
  black --check .
  ```
