"""
Database models and setup for food environmental impact data.
"""
import sqlite3
import os

def create_database(db_path: str = None) -> None:
    """
    Create the SQLite database with the foods table.
    
    Args:
        db_path (str, optional): Path to the database file. If None, uses default path.
    """
    if db_path is None:
        # Default path is in the data directory
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        db_path = os.path.join(current_dir, 'data', 'food_environment.db')
    
    # Create database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the foods table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,                    -- Name of the food (e.g., "Beef", "Lentils")
        food_type TEXT NOT NULL,               -- "animal" or "plant"
        serving_size_grams REAL NOT NULL,      -- Standard serving size in grams
        ghg_emissions REAL NOT NULL,           -- Greenhouse gas emissions in kg CO2e per serving
        water_usage REAL NOT NULL,             -- Water usage in liters per serving
        land_use REAL NOT NULL,                -- Land use in square meters per serving
        data_source TEXT NOT NULL,             -- Source of the data (e.g., "World Resources Institute")
        notes TEXT                             -- Any additional notes or context
    )
    ''')

    # Create an index on food name for faster searches
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_food_name ON foods(name)')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database created successfully!")
    print(f"Database file location: {db_path}")

class Food:
    """
    Represents a food item and its environmental impact data.
    """
    def __init__(self, name: str, food_type: str, serving_size_grams: float,
                 ghg_emissions: float, water_usage: float, land_use: float,
                 data_source: str, notes: str = None):
        self.name = name
        self.food_type = food_type
        self.serving_size_grams = serving_size_grams
        self.ghg_emissions = ghg_emissions
        self.water_usage = water_usage
        self.land_use = land_use
        self.data_source = data_source
        self.notes = notes

    def to_dict(self) -> dict:
        """Convert the Food object to a dictionary."""
        return {
            'name': self.name,
            'food_type': self.food_type,
            'serving_size_grams': self.serving_size_grams,
            'ghg_emissions': self.ghg_emissions,
            'water_usage': self.water_usage,
            'land_use': self.land_use,
            'data_source': self.data_source,
            'notes': self.notes
        } 