"""
Script to parse Excel file containing environmental impact data.
Extracts and processes data from Table 8 of the supplementary material.
"""
import os
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
import re
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def clean_html_text(text: str) -> str:
    """
    Clean HTML-like formatting from text.
    
    Args:
        text: Text containing HTML-like tags
        
    Returns:
        Cleaned text
    """
    if pd.isna(text):
        return text
    # Convert to string if not already
    text = str(text)
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text

def read_excel_sheet(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """
    Read an Excel file and return the specified sheet as a DataFrame.
    
    Args:
        file_path: Path to the Excel file
        sheet_name: Name of the sheet to read (if None, reads first sheet)
        
    Returns:
        DataFrame containing the sheet data
    """
    try:
        logger.info(f"Reading Excel file: {file_path}")
        
        # Try to read all sheets first to see what's available
        xls = pd.ExcelFile(file_path)
        logger.info(f"Available sheets: {xls.sheet_names}")
        
        # Read the specified sheet or the first one
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path, sheet_name=0)
            
        # Clean HTML-like formatting from all cells
        for col in df.columns:
            df[col] = df[col].apply(clean_html_text)
            
        # Log basic information about the data
        logger.info(f"Shape of data: {df.shape}")
        logger.info("Column names:")
        for col in df.columns:
            logger.info(f"  - {col}")
            
        return df
    except Exception as e:
        logger.error(f"Error reading Excel file: {str(e)}")
        raise

def parse_metric_name(text: str) -> Dict[str, str]:
    """
    Parse a metric name into components.
    
    Args:
        text: Raw metric text
        
    Returns:
        Dictionary containing metric components
    """
    if pd.isna(text):
        return {'name': '', 'unit': '', 'notes': ''}
    
    text = str(text)
    # Match pattern: metric name (unit) note
    pattern = r'^(.*?)(?:\s*\((.*?)\))?\s*([^()]*)?$'
    match = re.match(pattern, text)
    
    if match:
        name = match.group(1).strip()
        unit = match.group(2) or ''
        notes = match.group(3) or ''
        return {'name': name, 'unit': unit, 'notes': notes}
    return {'name': text, 'unit': '', 'notes': ''}

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names by removing special characters and standardizing format.
    
    Args:
        df: DataFrame with raw column names
        
    Returns:
        DataFrame with cleaned column names
    """
    # Create a copy to avoid modifying the original
    df = df.copy()
    
    # Log original column names
    logger.info("Original column names:")
    for col in df.columns:
        logger.info(f"  - {col}")
    
    def clean_name(name):
        name = str(name).lower()
        name = re.sub(r'[^a-z0-9_\s]', '', name)
        name = name.replace(' ', '_')
        name = re.sub(r'_{2,}', '_', name)
        if name.startswith('rl'):
            name = 'rl_to_' + name[2:]
        elif name.startswith('sp'):
            name = 'sp_to_' + name[2:]
        return name
    
    cleaned_names = {col: clean_name(col) for col in df.columns}
    df = df.rename(columns=cleaned_names)
    
    # Log cleaned column names
    logger.info("Cleaned column names:")
    for col in df.columns:
        logger.info(f"  - {col}")
    
    return df

def clean_numeric_value(value):
    """Clean and convert string to numeric value."""
    if pd.isna(value):
        return np.nan
    
    # Convert to string and clean
    value = str(value)
    # Remove any non-numeric characters except decimal points and negative signs
    value = re.sub(r'[^0-9\.-]', '', value)
    
    try:
        return float(value)
    except ValueError:
        return np.nan

def process_metric_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process metric data by cleaning and standardizing values.
    
    Args:
        df: DataFrame containing metric data
        
    Returns:
        Processed DataFrame with standardized columns
    """
    # Initialize lists to store processed data
    processed_rows = []
    current_category = None
    current_metric_info = {'unit': '', 'notes': ''}
    
    # Production system mapping
    system_mapping = {
        'rl_to_rl': 'Range Land to Range Land',
        'rl_to_sp': 'Range Land to Semi-Pasture',
        'rl_to_fl': 'Range Land to Feed Lot',
        'sp_to_sp': 'Semi-Pasture to Semi-Pasture',
        'sp_to_fl': 'Semi-Pasture to Feed Lot'
    }
    
    # Process each row
    for _, row in df.iterrows():
        # Get the metric name from the first column
        metric_text = row.iloc[0]
        if pd.notna(metric_text):
            metric_info = parse_metric_name(metric_text)
            if metric_info['name']:  # Only update if we have a valid name
                current_category = metric_info['name']
                current_metric_info = metric_info
        
        if current_category:  # Only process if we have a valid category
            # Create base record
            base_record = {
                'metric_name': current_category,
                'unit': current_metric_info['unit'],
                'notes': current_metric_info['notes'],
                'source': 'Rotz et al. 2019',
                'year': 2018
            }
            
            # Process each production system
            for col in df.columns[2:]:  # Skip first two columns
                if col in system_mapping:
                    value = clean_numeric_value(row[col])
                    if not pd.isna(value):
                        record = base_record.copy()
                        record.update({
                            'value': value,
                            'production_system': system_mapping[col]
                        })
                        processed_rows.append(record)
    
    # Create DataFrame from processed rows
    result_df = pd.DataFrame(processed_rows)
    
    # Log data info
    logger.info("\nProcessed data info:")
    logger.info(result_df.info())
    
    return result_df

def save_processed_data(df: pd.DataFrame, output_dir: str):
    """
    Save processed data to CSV files.
    
    Args:
        df: DataFrame to save
        output_dir: Directory to save the files
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save main dataset
    output_file = output_dir / 'beef_emissions_impacts.csv'
    df.to_csv(output_file, index=False)
    
    logger.info(f"\nSaved emissions data to {output_file}")
    logger.info(f"Shape: {df.shape}")
    logger.info("Columns:")
    for col in df.columns:
        non_null = df[col].notna().sum()
        total = len(df)
        logger.info(f"  - {col}: {non_null}/{total} non-null values")
    
    # Create and save summary statistics
    try:
        numeric_df = df.copy()
        numeric_df['value'] = pd.to_numeric(numeric_df['value'], errors='coerce')
        
        summary = numeric_df.groupby(['metric_name', 'production_system']).agg({
            'value': ['count', 'mean', 'std', 'min', 'max']
        }).reset_index()
        
        # Flatten column names
        summary.columns = ['metric_name', 'production_system', 'count', 'mean', 'std', 'min', 'max']
        
        summary_file = output_dir / 'beef_emissions_summary.csv'
        summary.to_csv(summary_file, index=False)
        logger.info(f"\nSaved summary statistics to {summary_file}")
        
    except Exception as e:
        logger.error(f"Error creating summary statistics: {str(e)}")

def main():
    """Main function to process the Excel file."""
    # Set up paths
    input_file = "data/raw/Table8.xls"
    output_dir = "data/processed"
    
    try:
        # Read Excel file
        df = read_excel_sheet(input_file)
        
        # Clean column names
        df = clean_column_names(df)
        logger.info(f"\nFound {len(df.columns)} columns in the Excel file")
        
        # Process the data
        processed_data = process_metric_data(df)
        
        # Save the processed data
        save_processed_data(processed_data, output_dir)
        
    except Exception as e:
        logger.error(f"Error processing Excel file: {str(e)}")
        raise

if __name__ == "__main__":
    main() 