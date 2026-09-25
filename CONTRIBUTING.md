# Contributing to Blackjax

First off, thanks for taking the time to contribute!

## Development Setup

1. Clone the repo and navigate to the directory:
   ```bash
   git clone <repo-url>
   cd blackjax
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Pull Request Process

1. Ensure all tests pass by running `pytest`.
2. Ensure code is formatted and passes linting and type checks (`pre-commit run --all-files`).
3. Submit your PR with a clear description of the changes.
