"""
Excel Data Extractor

This script will handle the extraction of data from Excel files.
It will provide the following functionality:

1. Data Extraction:
   - Read Excel files (.xlsx, .xls)
   - Handle multiple sheets
   - Support different Excel versions
   - Process large files efficiently

2. Data Transformation:
   - Convert data types appropriately
   - Handle missing values
   - Clean and normalize data

3. Output:
   - Return data in a standardized format
   - Support different output structures
"""

import pandas as pd
from typing import Dict, Any
import datetime

# Import the base class from its new location
from .base_extractor import BaseExtractor

class ExcelExtractor(BaseExtractor):
    """
    Concrete implementation of BaseExtractor for Excel files.
    This extracts data from the first sheet of the Excel file.
    """
    def extract_data(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from the first sheet of an Excel file.
        
        Args:
            file_path (str): Path to the Excel file (.xls or .xlsx).
            
        Returns:
            Dict[str, Any]: Extracted data including headers, rows, and row count.
            
        Raises:
            ValueError: If the file cannot be read or processed as Excel.
            FileNotFoundError: If the Excel file does not exist.
        """
        try:
            # Read the first sheet of the Excel file using pandas
            # Requires openpyxl for .xlsx or xlrd for .xls
            df = pd.read_excel(file_path, sheet_name=0) # sheet_name=0 reads the first sheet
            
            # Convert DataFrame to a dictionary format
            data = {
                "headers": df.columns.tolist(), # List of column names
                "rows": df.values.tolist(),    # List of lists (rows)
                "row_count": len(df)           # Number of data rows
            }
            
            # Update metadata specific to Excel extraction
            self.metadata["file_type"] = "excel"
            self.metadata["extracted_at"] = datetime.datetime.now().isoformat() # Record timestamp
            self.metadata["sheet_name"] = df.attrs.get('sheet_name', 0) # Store sheet name/index if available
            self.metadata["columns"] = df.columns.tolist() # Add column names
            self.metadata["shape"] = df.shape # Add DataFrame shape (rows, cols)
            
            return data

        except FileNotFoundError:
            # Handle file not found specifically
            raise FileNotFoundError(f"Excel file not found at: {file_path}")
        except Exception as e:
            # Catch other potential errors (e.g., invalid format, password-protected)
            # Consider adding more specific error handling for libraries like openpyxl or xlrd if needed
            raise ValueError(f"Error extracting data from Excel file '{file_path}': {str(e)}") 