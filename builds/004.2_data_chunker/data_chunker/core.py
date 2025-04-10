"""
Core functionality for the Data Chunker module.

This module provides the main DataChunker class that coordinates the chunking process.
"""

from pathlib import Path
from typing import Any, Generator, List, Optional, Union
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
from .file_handler import FileHandler
from .chunk_processor import ChunkProcessor


class DataChunker:
    """
    A class for chunking large datasets into smaller, manageable pieces.

    This class coordinates the file handling and chunk processing operations
    to provide a high-level interface for chunking data.

    Attributes:
        chunk_size (int): The size of each data chunk.
        input_dir (Path): Path to the input directory.
        output_dir (Path): Path to the output directory.
        current_file (Path): Current file being processed.
        total_rows (int): Total number of rows in the dataset.
        current_chunk (int): Current chunk number being processed.
    """

    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        'json': '.json',
        # Add other file extensions here in the future
        # 'csv': '.csv',
        # 'parquet': '.parquet',
    }

    def __init__(self, chunk_size: int = 1000, input_dir: Union[str, Path] = "input", 
                 output_dir: Union[str, Path] = "output") -> None:
        """
        Initialize the DataChunker.

        Args:
            chunk_size (int): The number of rows per chunk. Defaults to 1000.
            input_dir (Union[str, Path]): Path to the input directory. Defaults to "input".
            output_dir (Union[str, Path]): Path to the output directory. Defaults to "output".
        """
        self.file_handler = FileHandler(Path(input_dir), Path(output_dir))
        self.chunk_processor = ChunkProcessor(chunk_size)
        self.current_file: Optional[Path] = None
        self.total_rows: int = 0
        self.current_chunk: int = 0

        # Create directories if they don't exist
        self.file_handler.input_dir.mkdir(exist_ok=True)
        self.file_handler.output_dir.mkdir(exist_ok=True)

    def process_all_files(self) -> None:
        """
        Process all files in the input directory.

        This method will:
        1. Find all supported files in the input directory
        2. Process each file in chunks
        3. Save the processed chunks to the output directory
        """
        files = self.file_handler.get_supported_files()
        for file_path in files:
            self.process_file(file_path)

    def process_file(self, file_path: Union[str, Path]) -> None:
        """
        Process a single file from the input directory.

        Args:
            file_path (Union[str, Path]): Path to the input file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported.
        """
        file_path = Path(file_path)
        self.current_file = file_path

        # Validate the file
        self.file_handler.validate_file(file_path)

        # Process the file
        for chunk in self.chunk_processor.process_json_file(file_path):
            # Save the chunk
            self.save_chunk(chunk, self.chunk_processor.current_chunk)

    def get_chunk(self) -> Generator[Union[pd.DataFrame, np.ndarray], None, None]:
        """
        Get the next chunk of data from the current file.

        Yields:
            Union[pd.DataFrame, np.ndarray]: The next chunk of data.

        Raises:
            RuntimeError: If no file is loaded.
        """
        pass

    def save_chunk(self, chunk: Union[pd.DataFrame, np.ndarray], chunk_number: int) -> None:
        """
        Save a chunk to the output directory.

        Args:
            chunk (Union[pd.DataFrame, np.ndarray]): The chunk to save.
            chunk_number (int): The chunk number for naming the output file.

        Raises:
            RuntimeError: If no file is loaded.
        """
        if self.current_file is None:
            raise RuntimeError("No file is currently loaded")

        # Create output filename
        output_file = self.file_handler.output_dir / f"{self.current_file.stem}_chunk_{chunk_number}.json"
        
        # Save the chunk
        if isinstance(chunk, pd.DataFrame):
            chunk.to_json(output_file, orient='records')
        else:
            # Handle numpy array
            pd.DataFrame(chunk).to_json(output_file, orient='records')

    def get_total_chunks(self) -> int:
        """
        Calculate the total number of chunks for the current file.

        Returns:
            int: Total number of chunks.

        Raises:
            RuntimeError: If no file is loaded.
        """
        pass

    def reset(self) -> None:
        """
        Reset the chunker to its initial state.

        This method resets the current chunk counter and allows the chunker
        to be reused with the same file.
        """
        pass

    def _validate_file(self) -> None:
        """
        Validate the current file.

        This internal method checks if the file exists and is in a supported format.
        For JSON files, it also performs a basic validation of the JSON structure.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported or the file is invalid.
            RuntimeError: If no file is currently loaded.
        """
        if self.current_file is None:
            raise RuntimeError("No file is currently loaded")

        # Check if file exists
        if not self.current_file.exists():
            raise FileNotFoundError(f"File not found: {self.current_file}")

        # Check if file is readable
        if not os.access(self.current_file, os.R_OK):
            raise ValueError(f"File is not readable: {self.current_file}")

        # Get the file format
        file_format = self._get_file_format()

        # Validate based on file format
        if file_format == 'json':
            try:
                # Basic JSON validation - try to read the file
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    import json
                    json.load(f)  # This will raise json.JSONDecodeError if invalid
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON file: {self.current_file}. Error: {str(e)}")
            except Exception as e:
                raise ValueError(f"Error reading JSON file: {self.current_file}. Error: {str(e)}")

    def _get_file_format(self) -> str:
        """
        Determine the format of the current file.

        Returns:
            str: The file format (e.g., 'json').

        Raises:
            ValueError: If the file format cannot be determined.
            RuntimeError: If no file is currently loaded.
        """
        if self.current_file is None:
            raise RuntimeError("No file is currently loaded")

        # Get the file extension in lowercase
        extension = self.current_file.suffix.lower()

        # Find the format name for the extension
        for format_name, format_extension in self.SUPPORTED_EXTENSIONS.items():
            if extension == format_extension:
                return format_name

        # If we get here, the extension is not supported
        raise ValueError(f"Unsupported file format: {extension}. Supported formats: {list(self.SUPPORTED_EXTENSIONS.keys())}")

    def _get_supported_files(self) -> List[Path]:
        """
        Get a list of supported files in the input directory.

        Returns:
            List[Path]: List of paths to supported files.

        Note:
            Currently only supports JSON files, but the structure allows for easy
            addition of other file types in the future.
        """
        supported_files: List[Path] = []
        
        # Check if input directory exists
        if not self.file_handler.input_dir.exists():
            return supported_files

        # Get all files in the input directory
        for file_path in self.file_handler.input_dir.glob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS.values():
                supported_files.append(file_path)

        return supported_files
