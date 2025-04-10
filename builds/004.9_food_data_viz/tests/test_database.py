"""
Tests for the database module.
"""
import os
import sqlite3
import pytest
from food_impact.database import create_database

def test_database_creation():
    """Test that the database is created correctly."""
    # Create a temporary database
    db_path = "test_food_environment.db"
    create_database(db_path)
    
    # Verify the database exists
    assert os.path.exists(db_path)
    
    # Verify the table structure
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if the foods table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='foods'")
    assert cursor.fetchone() is not None
    
    # Check if the table has the correct columns
    cursor.execute("PRAGMA table_info(foods)")
    columns = [col[1] for col in cursor.fetchall()]
    expected_columns = ['id', 'name', 'food_type', 'serving_size_grams', 
                       'ghg_emissions', 'water_usage', 'land_use', 
                       'data_source', 'notes']
    assert all(col in columns for col in expected_columns)
    
    # Clean up
    conn.close()
    os.remove(db_path) 