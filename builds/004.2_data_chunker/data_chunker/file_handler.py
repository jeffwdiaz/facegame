"""
File handling operations for the Data Chunker module.

This module provides functionality for file validation, format detection,
and file operations.
"""

from pathlib import Path
from typing import List
import os
import json


class FileHandler:
    """
    Handles file operations for the Data Chunker.

    This class provides methods for validating files, detecting formats,
    and managing file operations.
    """

    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        'json': '.json',
        # Add other file extensions here in the future
        # 'csv': '.csv',
        # 'parquet': '.parquet',
    }

    def __init__(self, input_dir: Path, output_dir: Path):
        """
        Initialize the FileHandler.

        Args:
            input_dir (Path): Path to the input directory.
            output_dir (Path): Path to the output directory.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir

        # Create directories if they don't exist
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

    def get_supported_files(self) -> List[Path]:
        """
        Get a list of supported files in the input directory.

        Returns:
            List[Path]: List of paths to supported files.
        """
        supported_files: List[Path] = []
        
        # Check if input directory exists
        if not self.input_dir.exists():
            return supported_files

        # Get all files in the input directory
        for file_path in self.input_dir.glob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS.values():
                supported_files.append(file_path)

        return supported_files

    def validate_file(self, file_path: Path) -> None:
        """
        Validate a file.

        Args:
            file_path (Path): Path to the file to validate.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported or the file is invalid.
        """
        # Check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check if file is readable
        if not os.access(file_path, os.R_OK):
            raise ValueError(f"File is not readable: {file_path}")

        # Get the file format
        file_format = self._get_file_format(file_path)

        # Validate based on file format
        if file_format == 'json':
            try:
                # Basic JSON validation - try to read the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    json.load(f)  # This will raise json.JSONDecodeError if invalid
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON file: {file_path}. Error: {str(e)}")
            except Exception as e:
                raise ValueError(f"Error reading JSON file: {file_path}. Error: {str(e)}")

    def _get_file_format(self, file_path: Path) -> str:
        """
        Determine the format of a file.

        Args:
            file_path (Path): Path to the file.

        Returns:
            str: The file format (e.g., 'json').

        Raises:
            ValueError: If the file format cannot be determined.
        """
        # Get the file extension in lowercase
        extension = file_path.suffix.lower()

        # Find the format name for the extension
        for format_name, format_extension in self.SUPPORTED_EXTENSIONS.items():
            if extension == format_extension:
                return format_name

        # If we get here, the extension is not supported
        raise ValueError(f"Unsupported file format: {extension}. Supported formats: {list(self.SUPPORTED_EXTENSIONS.keys())}") 