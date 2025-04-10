## Project Overview
A collection of python scripts that extract data from datasets with different filetypes. Each filetype will have it's own script. There will be one script to identify the file type. And a main script to call the other scripts.

**Do not edit the project overview section of this file.**

# Data Extraction Tool

A Python-based tool for extracting data from various file formats (CSV, Excel, JSON).

## Features

- **File Type Detection**: Automatically detects file types (CSV, Excel, JSON)
- **Extensible Architecture**: Easy to add support for new file types
- **Standardized Output**: Consistent data format across all extractors
- **Metadata Tracking**: Includes extraction timestamps and file information

## Supported File Types

- CSV files (.csv)
- Excel files (.xlsx, .xls)
- JSON files (.json)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```python
from src.main import ExtractorFactory

# Create an extractor based on file type
extractor = ExtractorFactory.create_extractor("path/to/your/file.csv")

# Extract and process data
data = extractor.extract_data("path/to/your/file.csv")
transformed_data = extractor.transform_data(data)
output = extractor.format_output(transformed_data)
```

## Project Structure

```
src/
├── main.py              # Main entry point and factory
└── extractors/          # Concrete extractor implementations
    ├── csv_extractor.py
    ├── excel_extractor.py
    └── json_extractor.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here] 