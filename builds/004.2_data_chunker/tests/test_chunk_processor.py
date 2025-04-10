"""
Tests for the ChunkProcessor class.
"""

import pytest
from pathlib import Path
import json
import tempfile
from datetime import datetime
from data_chunker.chunk_processor import ChunkProcessor, DataStructure

@pytest.fixture
def sample_json_file():
    """Create a temporary JSON file with sample data."""
    data = {
        "data": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        return Path(f.name)

@pytest.fixture
def processor():
    """Create a ChunkProcessor instance."""
    return ChunkProcessor(chunk_size=2)

def test_metadata_fields(processor, sample_json_file):
    """Test that all metadata fields are present in the output DataFrame."""
    # Process the file
    chunks = list(processor.process_json_file(sample_json_file))
    
    # Check that we got the expected number of chunks
    assert len(chunks) == 2  # 3 items with chunk_size=2
    
    # Check metadata fields in the first chunk
    df = chunks[0]
    expected_metadata_fields = {
        'chunk_id',
        'source_file',
        'chunk_number',
        'total_chunks',
        'processing_timestamp',
        'data_structure',
        'record_count',
        'chunk_size'
    }
    
    # Verify all metadata fields are present
    assert all(field in df.columns for field in expected_metadata_fields)
    
    # Verify metadata values
    assert df['source_file'].iloc[0] == sample_json_file.name
    assert df['chunk_number'].iloc[0] == 1
    assert df['total_chunks'].iloc[0] == 2
    assert df['data_structure'].iloc[0] == DataStructure.DICT_LIST.value
    assert df['record_count'].iloc[0] == 2
    assert df['chunk_size'].iloc[0] == 2
    
    # Verify timestamp is valid ISO format
    datetime.fromisoformat(df['processing_timestamp'].iloc[0])

def test_chunk_id_uniqueness(processor, sample_json_file):
    """Test that chunk IDs are unique."""
    chunks = list(processor.process_json_file(sample_json_file))
    
    # Get all chunk IDs
    chunk_ids = set()
    for df in chunks:
        chunk_ids.add(df['chunk_id'].iloc[0])
    
    # Verify all chunk IDs are unique
    assert len(chunk_ids) == len(chunks)

def test_metadata_consistency(processor, sample_json_file):
    """Test that metadata is consistent within each chunk."""
    chunks = list(processor.process_json_file(sample_json_file))
    
    for df in chunks:
        # Get the first row's metadata
        first_row_metadata = {col: df[col].iloc[0] for col in df.columns 
                            if col in ['chunk_id', 'source_file', 'chunk_number', 
                                     'total_chunks', 'processing_timestamp', 
                                     'data_structure', 'record_count', 'chunk_size']}
        
        # Verify all rows in the chunk have the same metadata
        for col, value in first_row_metadata.items():
            assert (df[col] == value).all(), f"Metadata field {col} is not consistent within chunk" 