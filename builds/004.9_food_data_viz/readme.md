## Project Overview
To address the lack of accessible information comparing the environmental footprints of animal-based and plant-based foods for consumers, particularly in NYC, a solution leveraging a vector database will be developed. The success of this solution will be measured by increased relevance and access to information, data accuracy, clear visualization, direct comparisons across key environmental metrics (greenhouse gas emissions, water usage, land use), and overall accessibility. The implementation will involve collecting data on common animal-based foods (beef, chicken, pork, dairy milk, eggs) and their plant-based alternatives from reputable sources like the World Resources Institute and the FAO, documenting specific environmental metrics per serving, and designing a database schema to store this information. A suitable database tool will be chosen, and the data will be meticulously input. Subsequently, an accessible data visualization tool will be selected and utilized to create clear and direct comparisons between food options using bar charts and infographics, with iterative refinement based on feedback to ensure clarity and impact. The effectiveness of the solution will be evaluated through subjective assessments of clarity and understandability by non-experts, time taken to comprehend the visuals, verification of data accuracy through source citation and data integrity checks, observation of initial reactions and key takeaways from viewers, ensuring relevance to consumers, and gauging the potential for encouraging consideration of plant-based options. We will start with comparing beef to plant-based alternatives. Only when we are satsified with that will we proceed further.

Do not update the project overview section of this readme. Do update the rest of the readme as we go along.

## Tech Stack
- Python 3.8+
- SQLite for data storage
- Pandas for data manipulation
- Matplotlib and Seaborn for visualization

## Project Structure
```
project_root/
├── data/                    # For database file and raw data
│   ├── raw/                # Original, unprocessed data
│   └── processed/          # Transformed data
├── src/                     # Source code
│   └── food_impact/        # Main package
│       ├── __init__.py
│       └── database/       # Database-related code
│           ├── __init__.py
│           └── models.py
├── tests/                  # Test files
│   ├── conftest.py        # Shared test fixtures
│   └── test_database.py
├── docs/                   # Documentation
│   └── README.md
├── requirements.txt        # Legacy dependencies file
├── pyproject.toml         # Modern Python packaging config
├── .gitignore             # Git ignore patterns
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guidelines
├── CHANGELOG.md           # Version history
└── readme.md              # Project documentation
```

## Installation
1. Clone the repository
2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install the package in development mode:
```bash
pip install -e ".[dev]"  # Includes development dependencies
```

## Usage
To create the database:
```python
from food_impact.database import create_database

# Create the database (will be created in data/food_environment.db by default)
create_database()
```

## Testing
To run the tests:
```bash
pytest
```

## Contributing
Please read our [contributing guidelines](CONTRIBUTING.md) before submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.