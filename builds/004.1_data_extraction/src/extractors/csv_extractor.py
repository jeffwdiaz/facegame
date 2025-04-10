"""
CSV Data Extractor

This script will handle the extraction of data from CSV (Comma-Separated Values) files.
It will provide the following functionality:

1. Data Extraction:
   - Read CSV files with different delimiters
   - Handle quoted fields
   - Support different encodings
   - Process large files efficiently

2. Data Analysis:
   - Preview of data
   - Column statistics
   - Data type information
   - Missing value analysis
   - Column selection

3. Output:
   - Return data in a standardized format
   - Support different output structures
   - Include metadata about the extraction

The extractor will use Python's built-in csv module and pandas for efficient processing.
"""

import csv
import pandas as pd
from typing import Dict, Any, List, Optional
import numpy as np

# Import the base class from its new location
from .base_extractor import BaseExtractor

class CSVExtractor(BaseExtractor):
    """
    Concrete implementation of BaseExtractor for CSV files.
    """
    def __init__(self, preview_lines: int = 5):
        """
        Initialize the CSV extractor with configuration options.
        
        Args:
            preview_lines (int): Number of lines to include in preview (default: 5)
        """
        super().__init__()
        self.preview_lines = preview_lines
        self.selected_columns = None
        
    def _get_column_stats(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Calculate basic statistics for each column.
        
        Args:
            df (pd.DataFrame): The DataFrame to analyze
            
        Returns:
            Dict[str, Dict[str, Any]]: Statistics for each column
        """
        stats = {}
        for col in df.columns:
            col_stats = {
                "dtype": str(df[col].dtype),
                "non_null_count": df[col].count(),
                "null_count": df[col].isnull().sum(),
                "unique_values": df[col].nunique()
            }
            
            # Add numeric-specific stats
            if pd.api.types.is_numeric_dtype(df[col]):
                col_stats.update({
                    "mean": df[col].mean(),
                    "std": df[col].std(),
                    "min": df[col].min(),
                    "max": df[col].max(),
                    "median": df[col].median()
                })
            
            # Add categorical-specific stats
            elif pd.api.types.is_string_dtype(df[col]):
                col_stats.update({
                    "most_common": df[col].mode().iloc[0] if not df[col].mode().empty else None,
                    "most_common_count": df[col].value_counts().iloc[0] if not df[col].value_counts().empty else 0
                })
            
            stats[col] = col_stats
        return stats

    def _interactive_column_selection(self, df: pd.DataFrame) -> List[str]:
        """
        Interactively select columns from the DataFrame.
        
        Args:
            df (pd.DataFrame): The DataFrame to select columns from
            
        Returns:
            List[str]: List of selected column names
        """
        print("\nAvailable columns with sample data:")
        for idx, col in enumerate(df.columns, 1):
            # Get the first non-null value in the column
            sample_value = df[col].iloc[0] if not pd.isna(df[col].iloc[0]) else "NULL"
            print(f"{idx}. {col} (Sample: {sample_value})")
        
        while True:
            try:
                choices = input("\nEnter column numbers (comma-separated) or 'all' for all columns: ").strip()
                if choices.lower() == 'all':
                    return list(df.columns)
                
                selected_indices = [int(x.strip()) - 1 for x in choices.split(',')]
                selected_columns = [df.columns[i] for i in selected_indices if 0 <= i < len(df.columns)]
                
                if selected_columns:
                    return selected_columns
                print("Invalid selection. Please try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter numbers separated by commas.")
        
    def extract_data(self, file_path: str) -> Dict[str, Any]:
        """
        Extract data from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file.
            
        Returns:
            Dict[str, Any]: Extracted data including headers, rows, and analysis.
            
        Raises:
            ValueError: If the file cannot be read or processed as CSV.
            FileNotFoundError: If the CSV file does not exist.
        """
        try:
            # First read just a preview to show the user
            preview_df = pd.read_csv(file_path, nrows=self.preview_lines)
            
            # Show file information
            print(f"\nFile: {file_path}")
            print(f"Shape: {preview_df.shape[0]} rows, {preview_df.shape[1]} columns")
            
            # Show preview of data
            print("\nPreview of data:")
            print(preview_df)
            
            # Get column selection from user
            self.selected_columns = self._interactive_column_selection(preview_df)
            
            # Now read the entire file with only the selected columns
            print("\nReading entire file with selected columns...")
            df = pd.read_csv(file_path, usecols=self.selected_columns)
            
            # Get column statistics
            column_stats = self._get_column_stats(df)
            
            # Convert DataFrame to a dictionary format
            data = {
                "headers": df.columns.tolist(),  # List of column names
                "data": df.to_dict('records'),  # All data, not just preview
                "row_count": len(df),  # Number of data rows
                "column_stats": column_stats,  # Statistics for each column
                "shape": df.shape,  # (rows, columns)
                "memory_usage": df.memory_usage(deep=True).sum(),  # Total memory usage
                "dtypes": df.dtypes.astype(str).to_dict()  # Data types of each column
            }
            
            # Update metadata specific to CSV extraction
            self.metadata.update({
                "file_type": "csv",
                "extracted_at": pd.Timestamp.now().isoformat(),
                "columns": df.columns.tolist(),
                "shape": df.shape,
                "total_memory_usage": f"{data['memory_usage'] / 1024:.2f} KB",
                "preview_lines": self.preview_lines,
                "selected_columns": self.selected_columns
            })
            
            return data
            
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at: {file_path}")
        except pd.errors.EmptyDataError:
            raise ValueError(f"CSV file is empty: {file_path}")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV file '{file_path}': {str(e)}")
        except Exception as e:
            raise ValueError(f"Error extracting data from CSV file '{file_path}': {str(e)}")
            
    @staticmethod
    def get_headers(file_path: str) -> List[str]:
        """
        Get the headers from a CSV file without loading the entire file.
        
        Args:
            file_path (str): Path to the CSV file.
            
        Returns:
            List[str]: List of column headers.
        """
        try:
            # Read just the first row to get headers
            df = pd.read_csv(file_path, nrows=0)
            return df.columns.tolist()
        except Exception as e:
            raise ValueError(f"Error reading headers from CSV file '{file_path}': {str(e)}") 