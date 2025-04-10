"""
Main Data Extraction Script

This script serves as the entry point for the data extraction process.
It implements a class-based structure for handling different file types.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Type, List
from datetime import datetime
import os
from pathlib import Path
import time
import json

# Import the base class and specific extractors
from extractors.base_extractor import BaseExtractor
from extractors.csv_extractor import CSVExtractor
from extractors.json_extractor import JSONExtractor
from extractors.excel_extractor import ExcelExtractor

# Define supported file types and their corresponding extractor classes
SUPPORTED_EXTRACTORS = {
    "csv": CSVExtractor,
    "json": JSONExtractor,
    "xlsx": ExcelExtractor,
    "xls": ExcelExtractor
}

def get_default_directories() -> tuple[Path, Path]:
    """
    Gets the default input and output directories.
    Looks for input/output directories in the same folder as main.py.
    """
    current_file_path = Path(__file__).resolve()
    src_dir = current_file_path.parent
    
    # Default directories are in the same folder as main.py
    default_input_dir = src_dir / "input"
    default_output_dir = src_dir / "output"
    
    return default_input_dir, default_output_dir

def extract_data_from_file(file_path: Path) -> Dict[str, Any]:
    """
    Extracts data from a single file using the appropriate extractor.
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"Input file not found: {str(file_path)}")
        
    file_extension = file_path.suffix.lower().lstrip('.')
    extractor_class = SUPPORTED_EXTRACTORS.get(file_extension)
    
    if not extractor_class:
        raise ValueError(f"Unsupported file type: '.{file_extension}' for file '{file_path.name}'. Supported extensions: {list(SUPPORTED_EXTRACTORS.keys())}")
        
    extractor = extractor_class()
    
    try:
        print(f"\nProcessing file: '{file_path.name}'")
        print(f"Using extractor: {extractor.__class__.__name__}")
        start_time = time.time()
        extracted_data = extractor.extract_data(str(file_path))
        end_time = time.time()
        
        result = {
            "data": extracted_data,
            "metadata": extractor.get_metadata()
        }
        
        result["metadata"]["extraction_time_seconds"] = round(end_time - start_time, 4)
        result["metadata"]["original_filename"] = file_path.name
        
        print(f"Extraction successful for '{file_path.name}' in {result['metadata']['extraction_time_seconds']:.4f} seconds.")
        return result
        
    except Exception as e:
        print(f"Error during extraction from '{file_path.name}': {str(e)}")
        raise ValueError(f"Failed to extract data from '{file_path.name}': {str(e)}") from e

def main():
    """
    Main function to process files and save results.
    Uses default input and output directories.
    """
    # Get default directories
    input_dir, output_dir = get_default_directories()

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Using input directory: {input_dir}")
    print(f"Using output directory: {output_dir}")

    # Process files
    processed_files = 0
    failed_files = 0
    total_start_time = time.time()

    print("\nStarting directory scan...")
    for item_path in input_dir.iterdir():
        if item_path.is_file():
            file_extension = item_path.suffix.lower().lstrip('.')
            if file_extension in SUPPORTED_EXTRACTORS:
                try:
                    result = extract_data_from_file(item_path)
                    output_filename = item_path.stem + ".json"
                    output_file_path = output_dir / output_filename
                    
                    with open(output_file_path, 'w') as f:
                        json.dump(result, f, indent=4, default=str)
                    print(f"  -> Output saved to: {output_file_path.name}")
                    processed_files += 1
                    
                except Exception as e:
                    print(f"Failed to process file '{item_path.name}': {str(e)}")
                    failed_files += 1

    # Print summary
    total_end_time = time.time()
    print("\n--- Extraction Summary ---")
    print(f"Total time taken: {total_end_time - total_start_time:.2f} seconds")
    print(f"Successfully processed files: {processed_files}")
    print(f"Failed files: {failed_files}")
    print(f"Results saved in: {output_dir}")

if __name__ == "__main__":
    main() 