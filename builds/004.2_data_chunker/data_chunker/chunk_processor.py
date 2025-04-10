"""
Chunk processing operations for the Data Chunker module.

This module provides functionality for processing data in chunks.
It supports various data formats and structures, making it robust
for different types of datasets.
"""

from pathlib import Path
from typing import Generator, Union, Dict, List, Any, Optional
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import logging
from datetime import datetime
import uuid
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataStructure(Enum):
    """Represents different data structures that can be processed."""
    FLAT_LIST = "flat_list"  # Simple list of items
    DICT_LIST = "dict_list"  # List of dictionaries
    NESTED_DICT = "nested_dict"  # Dictionary with nested data
    UNKNOWN = "unknown"  # Structure not yet identified


class ChunkProcessor:
    """
    Handles chunk processing operations for the Data Chunker.

    This class provides methods for processing data in chunks and managing
    the chunking process. It supports various data formats and structures.
    """

    def __init__(self, chunk_size: int = 1000):
        """
        Initialize the ChunkProcessor.

        Args:
            chunk_size (int): The number of rows per chunk. Defaults to 1000.
        """
        self.chunk_size = chunk_size
        self.current_chunk: int = 0
        self.total_rows: int = 0
        self.data_structure: Optional[DataStructure] = None

    def process_json_file(self, file_path: Path) -> Generator[pd.DataFrame, None, None]:
        """
        Process a JSON file in chunks.

        Args:
            file_path (Path): Path to the JSON file.

        Yields:
            pd.DataFrame: The next chunk of data.

        Raises:
            ValueError: If the JSON file has an unsupported structure.
        """
        # Reset state for new file
        self.reset()

        try:
            # Read and validate the JSON file
            data = self._read_json_file(file_path)
            
            # Identify the data structure
            self.data_structure = self._identify_structure(data)
            logger.info(f"Identified data structure: {self.data_structure}")
            
            # Extract the records based on the structure
            records = self._extract_records(data)
            self.total_rows = len(records)
            logger.info(f"Total records to process: {self.total_rows}")
            
            # Process in chunks
            for chunk_df in self._process_chunks(records, file_path):
                yield chunk_df
                
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise

    def _read_json_file(self, file_path: Path) -> Any:
        """Read and validate a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")

    def _identify_structure(self, data: Any) -> DataStructure:
        """Identify the structure of the data."""
        if isinstance(data, list):
            if data and isinstance(data[0], dict):
                return DataStructure.DICT_LIST
            return DataStructure.FLAT_LIST
        elif isinstance(data, dict):
            if 'data' in data:
                if isinstance(data['data'], list):
                    return DataStructure.DICT_LIST
                elif isinstance(data['data'], dict) and 'data' in data['data']:
                    return DataStructure.NESTED_DICT
            return DataStructure.DICT_LIST
        return DataStructure.UNKNOWN

    def _extract_records(self, data: Any) -> List[Any]:
        """Extract records based on the identified structure."""
        if self.data_structure == DataStructure.FLAT_LIST:
            return data
        elif self.data_structure == DataStructure.DICT_LIST:
            return data if isinstance(data, list) else data.get('data', [])
        elif self.data_structure == DataStructure.NESTED_DICT:
            return data['data']['data'] if isinstance(data['data'], dict) else data['data']
        else:
            raise ValueError(f"Unsupported data structure: {self.data_structure}")

    def _process_chunks(self, records: List[Any], file_path: Path) -> Generator[pd.DataFrame, None, None]:
        """Process records in chunks and yield DataFrames with metadata."""
        for i in tqdm(range(0, len(records), self.chunk_size), 
                     desc=f"Processing {file_path.name}"):
            chunk = records[i:i + self.chunk_size]
            self.current_chunk += 1
            
            try:
                # Create DataFrame based on record type
                if isinstance(chunk[0], dict):
                    df = pd.DataFrame.from_records(chunk)
                else:
                    df = pd.DataFrame(chunk, columns=['value'])
                
                # Add chunk metadata
                metadata = {
                    'chunk_id': str(uuid.uuid4()),
                    'source_file': file_path.name,
                    'chunk_number': self.current_chunk,
                    'total_chunks': self.get_total_chunks(),
                    'processing_timestamp': datetime.now().isoformat(),
                    'data_structure': self.data_structure.name if self.data_structure else 'unknown',
                    'record_count': len(chunk),
                    'chunk_size': self.chunk_size
                }
                
                # Add metadata as columns to the DataFrame
                for key, value in metadata.items():
                    df[key] = value
                
                yield df
                
            except Exception as e:
                logger.error(f"Error processing chunk {self.current_chunk}: {str(e)}")
                raise

    def get_total_chunks(self) -> int:
        """
        Get the total number of chunks that will be generated.

        Returns:
            int: Total number of chunks.
        """
        return (self.total_rows + self.chunk_size - 1) // self.chunk_size

    def reset(self) -> None:
        """
        Reset the processor state.
        """
        self.current_chunk = 0
        self.total_rows = 0
        self.data_structure = None 