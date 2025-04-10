# Contributing to Food Impact Visualization

Thank you for your interest in contributing to the Food Impact Visualization project! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/food-impact.git
cd food-impact
```

3. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Code Style

- We use [Black](https://black.readthedocs.io/) for code formatting
- We use [Flake8](https://flake8.pycqa.org/) for style guide enforcement
- Run `black .` and `flake8` before committing

## Testing

- Write tests for new features using pytest
- Ensure all tests pass before submitting a pull request:
```bash
pytest
```

## Pull Request Process

1. Create a new branch for your feature
2. Make your changes
3. Update documentation as needed
4. Run tests and ensure they pass
5. Submit a pull request with a clear description of changes

## Adding New Data

When adding new food items to the database:
1. Use reputable sources (WRI, FAO, etc.)
2. Document the source in the `data_source` field
3. Include any relevant notes about the data
4. Verify units match our schema (kg CO2e, liters, square meters)

## Questions?

Feel free to open an issue for any questions about contributing! 