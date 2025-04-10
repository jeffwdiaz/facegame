"""
Main entry point for the Data Chunker package.

This module provides the command-line interface for the Data Chunker tool.
It automatically processes all JSON files in the package's input directory
and saves the chunks to the output directory.
"""

from pathlib import Path
from . import DataChunker


def main():
    """
    Main function to run the Data Chunker.
    Automatically processes all JSON files in the input directory
    and saves chunks to the output directory.
    """
    # Get the package directory
    package_dir = Path(__file__).parent
    
    # Define input and output directories relative to the package
    input_dir = package_dir / "input"
    output_dir = package_dir / "output"
    
    # Default chunk size
    chunk_size = 1000

    # Create DataChunker instance
    chunker = DataChunker(
        chunk_size=chunk_size,
        input_dir=str(input_dir),
        output_dir=str(output_dir)
    )

    # Process all files in the input directory
    print(f"Processing files from: {input_dir}")
    print(f"Saving chunks to: {output_dir}")
    print(f"Chunk size: {chunk_size} rows")
    
    try:
        chunker.process_all_files()
        print("Processing completed successfully!")
    except Exception as e:
        print(f"Error during processing: {str(e)}")


if __name__ == "__main__":
    main() 