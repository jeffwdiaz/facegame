"""
Script to extract environmental impact data from Table S8 of the supplementary data.
Focus on resource inputs and emissions for beef production stages.
"""
import os
import pandas as pd
import numpy as np
from docx import Document
from typing import List, Dict, Optional, Tuple

def get_table_dimensions(table) -> Tuple[int, int]:
    """
    Get the dimensions of a table (rows, columns).
    
    Args:
        table: A table object from python-docx
        
    Returns:
        Tuple of (number of rows, number of columns)
    """
    if not table.rows:
        return 0, 0
    return len(table.rows), max(len(row.cells) for row in table.rows)

def get_table_header(table) -> List[str]:
    """
    Extract and clean the header row from a table.
    
    Args:
        table: A table object from python-docx
        
    Returns:
        List of cleaned header strings
    """
    if not table.rows:
        return []
    return [cell.text.strip() for cell in table.rows[0].cells]

def get_table_content(table) -> List[List[str]]:
    """
    Extract all content from a table, ensuring consistent column count.
    
    Args:
        table: A table object from python-docx
        
    Returns:
        List of lists containing table data
    """
    if not table.rows:
        return []
        
    # Get maximum number of columns
    max_cols = get_table_dimensions(table)[1]
    
    # Extract and clean data
    data = []
    for row in table.rows:
        row_data = [cell.text.strip() for cell in row.cells]
        # Pad row if needed
        if len(row_data) < max_cols:
            row_data.extend([''] * (max_cols - len(row_data)))
        data.append(row_data)
    
    return data

def find_table_by_content(doc, required_keywords: List[str], min_rows: int = 2) -> Optional[Document]:
    """
    Find a table in the document based on its content.
    
    Args:
        doc: Document object from python-docx
        required_keywords: List of keywords that must be present
        min_rows: Minimum number of rows the table should have
        
    Returns:
        Table object if found, None otherwise
    """
    for i, table in enumerate(doc.tables, 1):
        rows, cols = get_table_dimensions(table)
        if rows < min_rows:
            continue
            
        # Get text from first few rows
        content = get_table_content(table)
        first_rows_text = ' '.join(
            ' '.join(row) 
            for row in content[:3]
        ).lower()
        
        print(f"\nTable {i} first rows:", first_rows_text[:100] + "...")
        
        # Check if all required keywords are present
        if all(keyword in first_rows_text for keyword in required_keywords):
            print(f"\nFound target table (Table {i})")
            return table
                
    print("\nWarning: Could not find target table in the document")
    return None

def clean_table_data(data: List[List[str]]) -> pd.DataFrame:
    """
    Convert raw table data to a cleaned pandas DataFrame.
    
    Args:
        data: List of lists containing table data
        
    Returns:
        Cleaned pandas DataFrame
    """
    if not data:
        return pd.DataFrame()
        
    # Convert to DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Clean up the data
    df = df.replace(['', '-', 'na', 'N/A', 'n/a'], np.nan)
    
    # Convert numeric columns
    for col in df.columns:
        if col not in ['Resource use or emission', 'Units']:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except Exception as e:
                print(f"Warning: Could not convert column {col} to numeric: {str(e)}")
            
    return df

def categorize_metrics(df: pd.DataFrame, categories: Dict[str, List[str]]) -> Dict[str, pd.DataFrame]:
    """
    Categorize metrics into different environmental impact categories.
    
    Args:
        df: DataFrame containing the metrics
        categories: Dictionary mapping category names to keyword lists
        
    Returns:
        Dictionary of categorized DataFrames
    """
    results = {}
    for category, keywords in categories.items():
        pattern = '|'.join(keywords)
        mask = (
            df['Resource use or emission'].str.contains(pattern, case=False, na=False) |
            df['Units'].str.contains(pattern, case=False, na=False)
        )
        if mask.any():
            results[category] = df[mask].copy()
            
    return results

def main():
    """Main function to process the Word document and extract environmental data."""
    input_file = "data/raw/1-s2.0-S0308521X18305675-mmc1.docx"
    output_dir = "data/processed"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print("Reading Word document...")
    doc = Document(input_file)
    
    # Define categories for environmental metrics
    categories = {
        'emissions': ['CO2', 'CH4', 'N2O', 'NH3', 'NO3', 'GHG', 'emission'],
        'water': ['water', 'precipitation', 'irrigation'],
        'land': ['land', 'soil', 'area', 'forage'],
        'energy': ['energy', 'fuel', 'electricity']
    }
    
    # Find the target table
    table = find_table_by_content(
        doc, 
        required_keywords=['resource use', 'emission', 'units']
    )
    
    if table:
        print("\nExtracting data from table...")
        raw_data = get_table_content(table)
        df = clean_table_data(raw_data)
        
        # Save full table data
        full_table_path = os.path.join(output_dir, "table_s8_full.csv")
        df.to_csv(full_table_path, index=False)
        print(f"\nSaved full table data to: {full_table_path}")
        
        # Process and save individual metric data
        print("\nProcessing environmental metrics...")
        metric_data = categorize_metrics(df, categories)
        
        for metric, data in metric_data.items():
            output_path = os.path.join(output_dir, f"environmental_{metric}.csv")
            data.to_csv(output_path, index=False)
            print(f"Saved {metric} data to: {output_path}")
            print(f"\n{metric.title()} metrics summary:")
            print(data[['Resource use or emission', 'Units', 'Total']].to_string())
            
    else:
        print("Error: Could not find target table in the document")

if __name__ == "__main__":
    main() 