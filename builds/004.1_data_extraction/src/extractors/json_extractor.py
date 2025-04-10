"""
JSON Data Extractor

This script will handle the extraction of data from JSON files.
It will provide the following functionality:

1. Data Extraction:
   - Read JSON files
   - Handle nested structures
   - Support different JSON formats
   - Process large files efficiently

2. Data Transformation:
   - Convert data types appropriately
   - Handle missing values
   - Clean and normalize data

3. Output:
   - Return data in a standardized format
   - Support different output structures
"""

import json
from typing import Dict, Any
import datetime

# Import the base class from its new location
from .base_extractor import BaseExtractor

class JSONExtractor(BaseExtractor):
    """
    Concrete implementation of BaseExtractor for JSON files.
    """
    def extract_data(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file.
            
        Returns:
            Dict[str, Any]: Extracted data (the raw JSON content).
            
        Raises:
            ValueError: If the file is not valid JSON or cannot be read.
        """
        try:
            # Open and read the JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Update metadata specific to JSON extraction
            self.metadata["file_type"] = "json"
            self.metadata["extracted_at"] = datetime.datetime.now().isoformat() # Record timestamp
            # Optionally add more metadata, e.g., size or top-level keys
            if isinstance(data, dict):
                self.metadata["top_level_keys"] = list(data.keys())
            elif isinstance(data, list):
                self.metadata["is_list"] = True
                self.metadata["list_length"] = len(data)
                
            return data
            
        except FileNotFoundError:
            # Handle file not found specifically
            raise FileNotFoundError(f"JSON file not found at: {file_path}")
        except json.JSONDecodeError as e:
            # Handle invalid JSON format
            raise ValueError(f"Invalid JSON format in file '{file_path}': {str(e)}")
        except Exception as e:
            # Catch other potential errors during file reading
            raise ValueError(f"Error extracting data from JSON file '{file_path}': {str(e)}") 