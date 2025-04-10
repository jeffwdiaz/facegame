"""
Shared test fixtures for the food impact project.
"""
import os
import pytest
import tempfile
from food_impact.database import create_database

@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Create a temporary file
    fd, path = tempfile.mkstemp()
    os.close(fd)
    
    # Create the database
    create_database(path)
    
    yield path
    
    # Cleanup
    os.unlink(path)

@pytest.fixture
def sample_food_data():
    """Return sample food data for testing."""
    return [
        {
            'name': 'Beef (ground)',
            'food_type': 'animal',
            'serving_size_grams': 100,
            'ghg_emissions': 13.3,
            'water_usage': 1451.2,
            'land_use': 164.9,
            'data_source': 'World Resources Institute',
            'notes': 'Global average values'
        },
        {
            'name': 'Beyond Burger',
            'food_type': 'plant',
            'serving_size_grams': 100,
            'ghg_emissions': 3.5,
            'water_usage': 521.6,
            'land_use': 2.4,
            'data_source': 'Beyond Meat LCA Study',
            'notes': '2018 production data'
        }
    ] 