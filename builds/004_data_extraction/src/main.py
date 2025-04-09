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
import argparse # Added for command-line arguments
import time     # Added for timing execution
import json # Added for JSON output

# Import the base class and specific extractors
# Note: BaseExtractor is no longer defined here
from .extractors.base_extractor import BaseExtractor # Import BaseExtractor from its new location
from .extractors.csv_extractor import CSVExtractor
from .extractors.json_extractor import JSONExtractor
from .extractors.excel_extractor import ExcelExtractor # Assuming you have this

# Define supported file types and their corresponding extractor classes
SUPPORTED_EXTRACTORS = {
    "csv": CSVExtractor,
    "json": JSONExtractor,
    "xlsx": ExcelExtractor, # Map .xlsx to ExcelExtractor
    "xls": ExcelExtractor   # Map .xls to ExcelExtractor
}

# --- Helper function to determine project root --- 
def get_project_root() -> Path:
    """Determines the project root directory (assuming src is one level down)."""
    # Path to the current file (main.py)
    current_file_path = Path(__file__).resolve()
    # Path to the src directory
    src_dir = current_file_path.parent
    # Project root is the parent of src
    return src_dir.parent

def get_default_directories() -> tuple[Path, Path]:
    """
    Gets the default input and output directories.
    Looks for input/output directories in the same folder as main.py.
    """
    # Path to the current file (main.py)
    current_file_path = Path(__file__).resolve()
    # Path to the src directory
    src_dir = current_file_path.parent
    
    # Default directories are in the same folder as main.py
    default_input_dir = src_dir / "input"
    default_output_dir = src_dir / "output"
    
    return default_input_dir, default_output_dir

def extract_data_from_file(file_path: Path) -> Dict[str, Any]: # Changed type hint to Path
    """
    Extracts data from a single file using the appropriate extractor.
    
    Args:
        file_path (Path): The path to the input file.
        
    Returns:
        Dict[str, Any]: A dictionary containing the extracted data and metadata.
        
    Raises:
        ValueError: If the file type is unsupported or if extraction fails.
        FileNotFoundError: If the input file does not exist.
    """
    # Check if the file exists (Path object checks this implicitly often, but explicit is good)
    if not file_path.is_file():
        raise FileNotFoundError(f"Input file not found: {str(file_path)}")
        
    # Determine the file extension (lowercase, without dot)
    file_extension = file_path.suffix.lower().lstrip('.')
    
    # Find the appropriate extractor class
    extractor_class = SUPPORTED_EXTRACTORS.get(file_extension)
    
    # Check if the file type is supported
    if not extractor_class:
        raise ValueError(f"Unsupported file type: '.{file_extension}' for file '{file_path.name}'. Supported extensions: {list(SUPPORTED_EXTRACTORS.keys())}")
        
    # Instantiate the extractor
    extractor = extractor_class()
    
    # Perform data extraction
    try:
        print(f"Extracting data from '{file_path.name}' using {extractor.__class__.__name__}...")
        start_time = time.time()
        # Pass the string representation of the path to the extractor if needed
        extracted_data = extractor.extract_data(str(file_path)) 
        end_time = time.time()
        
        # Combine extracted data and metadata
        result = {
            "data": extracted_data,
            "metadata": extractor.get_metadata()
        }
        
        # Add extraction time and original filename to metadata
        result["metadata"]["extraction_time_seconds"] = round(end_time - start_time, 4)
        result["metadata"]["original_filename"] = file_path.name
        
        print(f"Extraction successful for '{file_path.name}' in {result['metadata']['extraction_time_seconds']:.4f} seconds.")
        return result
        
    except Exception as e:
        # Propagate specific exceptions or catch general ones
        print(f"Error during extraction from '{file_path.name}': {str(e)}")
        # Re-raise to be caught in the main loop
        raise ValueError(f"Failed to extract data from '{file_path.name}': {str(e)}") from e

def main():
    """
    Main function to parse arguments, find files, run extraction, and save results.
    Processes all supported files in an input directory and saves results to an output directory.
    """
    # Get default directories from the same folder as main.py
    default_input_dir, default_output_dir = get_default_directories()

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Extract data from supported files in an input directory to an output directory."
    )
    parser.add_argument(
        "-i", "--input_dir", 
        type=Path, # Use Path type for easier handling
        default=default_input_dir,
        help=f"Path to the input directory (default: {default_input_dir})"
    )
    parser.add_argument(
        "-o", "--output_dir", 
        type=Path, 
        default=default_output_dir,
        help=f"Path to the output directory (default: {default_output_dir})"
    )
    
    # Parse command-line arguments
    args = parser.parse_args()

    input_dir = args.input_dir.resolve() # Get absolute path
    output_dir = args.output_dir.resolve()

    # --- Input Directory Validation ---
    if not input_dir.is_dir():
        print(f"Error: Input directory not found or is not a directory: {input_dir}")
        exit(1)

    # --- Output Directory Creation ---
    try:
        output_dir.mkdir(parents=True, exist_ok=True) # Create output dir if it doesn't exist
        print(f"Using input directory: {input_dir}")
        print(f"Using output directory: {output_dir}")
    except OSError as e:
        print(f"Error: Could not create output directory '{output_dir}': {str(e)}")
        exit(1)

    # --- File Processing Loop ---
    processed_files = 0
    failed_files = 0
    total_start_time = time.time()

    print("\nStarting directory scan...")
    # Iterate through all items in the input directory
    for item_path in input_dir.iterdir():
        # Process only files
        if item_path.is_file():
            # Check if the file extension is supported
            file_extension = item_path.suffix.lower().lstrip('.')
            if file_extension in SUPPORTED_EXTRACTORS:
                try:
                    # Extract data from the file
                    result = extract_data_from_file(item_path)
                    
                    # Construct the output file path (replace extension with .json)
                    output_filename = item_path.stem + ".json"
                    output_file_path = output_dir / output_filename
                    
                    # Convert the result to a JSON string
                    # Use default=str for non-serializable types like datetime or numpy types
                    output_json = json.dumps(result, indent=4, default=str)
                    
                    # Save the output to the corresponding file
                    with open(output_file_path, 'w') as f:
                        f.write(output_json)
                    print(f"  -> Output saved to: {output_file_path.name}")
                    processed_files += 1
                    
                except (FileNotFoundError, ValueError, Exception) as e:
                    # Catch errors during extraction or saving for a specific file
                    print(f"Failed to process file '{item_path.name}': {str(e)}")
                    failed_files += 1
            else:
                # Inform about skipped files (optional)
                # print(f"Skipping unsupported file: {item_path.name}")
                pass # Silently skip unsupported files

    # --- Summary --- 
    total_end_time = time.time()
    print("\n--- Extraction Summary ---")
    print(f"Total time taken: {total_end_time - total_start_time:.2f} seconds")
    print(f"Successfully processed files: {processed_files}")
    print(f"Failed files: {failed_files}")
    print(f"Results saved in: {output_dir}")

# Entry point for the script
if __name__ == "__main__":
    main() 