# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-04-06

### Added
- Initial project setup
- Basic SQLite database structure
- Food model for environmental impact data
- Basic test suite
- Project documentation

## [Unreleased]

### Added
- Created `scripts/convert_word_to_csv.py` to process the Poore & Nemecek (2018) Word document
  - Extracts food impact data from Word tables
  - Cleans and standardizes data
  - Saves to CSV format in processed data directory
- Added `python-docx` package to requirements.txt for Word document processing

### Fixed
- Removed `sqlite3` from requirements.txt as it's part of Python's standard library 