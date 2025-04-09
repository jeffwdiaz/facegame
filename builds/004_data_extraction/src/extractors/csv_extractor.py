"""
CSV Data Extractor

This script will handle the extraction of data from CSV (Comma-Separated Values) files.
It will provide the following functionality:

1. Data Extraction:
   - Read CSV files with different delimiters
   - Handle quoted fields
   - Support different encodings
   - Process large files efficiently

2. Data Transformation:
   - Convert data types appropriately
   - Handle missing values
   - Clean and normalize data

3. Output:
   - Return data in a standardized format
   - Support different output structures
   - Include metadata about the extraction

The extractor will use Python's built-in csv module and pandas for efficient processing.
"""

import csv
import pandas as pd
from typing import Dict, Any

# Import the base class from its new location
from .base_extractor import BaseExtractor

class CSVExtractor(BaseExtractor):
    """
    Concrete implementation of BaseExtractor for CSV files.
    """
    def extract_data(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file.
            
        Returns:
            Dict[str, Any]: Extracted data including headers, rows, and row count.
            
        Raises:
            ValueError: If the file cannot be read or processed as CSV.
            FileNotFoundError: If the CSV file does not exist.
        """
        try:
            # Read the CSV file using pandas
            df = pd.read_csv(file_path)
            
            # Convert DataFrame to a dictionary format
            data = {
                "headers": df.columns.tolist(),  # List of column names
                "rows": df.values.tolist(),     # List of lists (rows)
                "row_count": len(df)            # Number of data rows
            }
            
            # Update metadata specific to CSV extraction
            self.metadata["file_type"] = "csv"
            self.metadata["extracted_at"] = pd.Timestamp.now().isoformat() # Record timestamp
            self.metadata["columns"] = df.columns.tolist() # Add column names to metadata
            self.metadata["shape"] = df.shape # Add DataFrame shape (rows, cols) to metadata
            
            return data
            
        except FileNotFoundError:
            # Handle file not found specifically
            raise FileNotFoundError(f"CSV file not found at: {file_path}")
        except pd.errors.EmptyDataError:
            # Handle empty CSV file
            raise ValueError(f"CSV file is empty: {file_path}")
        except pd.errors.ParserError as e:
            # Handle CSV parsing errors
            raise ValueError(f"Error parsing CSV file '{file_path}': {str(e)}")
        except Exception as e:
            # Catch other potential errors during file reading or processing
            raise ValueError(f"Error extracting data from CSV file '{file_path}': {str(e)}") 