"""
Script to visualize environmental impact data from processed CSV files.
Creates bar charts and infographics comparing different impact metrics.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
import numpy as np

def load_processed_data(data_dir: str) -> Dict[str, pd.DataFrame]:
    """
    Load all processed environmental impact data files.
    
    Args:
        data_dir: Directory containing processed CSV files
        
    Returns:
        Dictionary mapping category names to DataFrames
    """
    data = {}
    for file in os.listdir(data_dir):
        if file.startswith('environmental_') and file.endswith('.csv'):
            category = file.replace('environmental_', '').replace('.csv', '')
            file_path = os.path.join(data_dir, file)
            data[category] = pd.read_csv(file_path)
    return data

def create_emissions_plot(df: pd.DataFrame, output_dir: str):
    """
    Create a bar chart showing greenhouse gas emissions by type.
    
    Args:
        df: DataFrame containing emissions data
        output_dir: Directory to save the plot
    """
    # Filter for GHG emissions
    ghg_data = df[df['Resource use or emission'].str.contains('Greenhouse gas', case=False, na=False)]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=ghg_data,
        x='Resource use or emission',
        y='Total',
        palette='viridis'
    )
    
    plt.title('Greenhouse Gas Emissions by Production Stage')
    plt.xlabel('Production Stage')
    plt.ylabel('kg CO2e/kg CW')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(os.path.join(output_dir, 'ghg_emissions.png'))
    plt.close()

def create_water_plot(df: pd.DataFrame, output_dir: str):
    """
    Create a bar chart showing water usage by type.
    
    Args:
        df: DataFrame containing water usage data
        output_dir: Directory to save the plot
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df,
        x='Resource use or emission',
        y='Total',
        palette='Blues'
    )
    
    plt.title('Water Usage by Type')
    plt.xlabel('Water Type')
    plt.ylabel('liters/kg CW')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(os.path.join(output_dir, 'water_usage.png'))
    plt.close()

def create_energy_plot(df: pd.DataFrame, output_dir: str):
    """
    Create a bar chart showing energy use by type.
    
    Args:
        df: DataFrame containing energy use data
        output_dir: Directory to save the plot
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df,
        x='Resource use or emission',
        y='Total',
        palette='Reds'
    )
    
    plt.title('Energy Use by Type')
    plt.xlabel('Energy Type')
    plt.ylabel('MJ/kg CW')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(os.path.join(output_dir, 'energy_use.png'))
    plt.close()

def create_comparison_plot(data: Dict[str, pd.DataFrame], output_dir: str):
    """
    Create a comparison plot showing all environmental impacts.
    
    Args:
        data: Dictionary of DataFrames containing all impact data
        output_dir: Directory to save the plot
    """
    # Extract total values for each category
    comparison_data = []
    
    # Get GHG emissions
    ghg_data = data['emissions'][data['emissions']['Resource use or emission'].str.contains('Greenhouse gas', case=False, na=False)]
    comparison_data.append({
        'Category': 'GHG Emissions',
        'Value': ghg_data['Total'].mean(),
        'Unit': 'kg CO2e/kg CW'
    })
    
    # Get water usage
    water_data = data['water'][data['water']['Resource use or emission'].str.contains('Blue water', case=False, na=False)]
    comparison_data.append({
        'Category': 'Water Usage',
        'Value': water_data['Total'].mean(),
        'Unit': 'liters/kg CW'
    })
    
    # Get energy use
    energy_data = data['energy'][data['energy']['Resource use or emission'].str.contains('Energy use', case=False, na=False)]
    comparison_data.append({
        'Category': 'Energy Use',
        'Value': energy_data['Total'].mean(),
        'Unit': 'MJ/kg CW'
    })
    
    # Create DataFrame for plotting
    df = pd.DataFrame(comparison_data)
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=df,
        x='Category',
        y='Value',
        palette='Set2'
    )
    
    plt.title('Environmental Impact Comparison')
    plt.xlabel('Impact Category')
    plt.ylabel('Impact Value')
    
    # Add unit labels
    for i, row in df.iterrows():
        plt.text(i, row['Value'], row['Unit'], ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(os.path.join(output_dir, 'impact_comparison.png'))
    plt.close()

def main():
    """Main function to create visualizations of environmental impact data."""
    # Set up directories
    data_dir = "data/processed"
    output_dir = "data/visualizations"
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.dpi'] = 300
    
    # Load data
    print("Loading processed data...")
    data = load_processed_data(data_dir)
    
    # Create individual plots
    print("Creating individual impact plots...")
    if 'emissions' in data:
        create_emissions_plot(data['emissions'], output_dir)
    if 'water' in data:
        create_water_plot(data['water'], output_dir)
    if 'energy' in data:
        create_energy_plot(data['energy'], output_dir)
    
    # Create comparison plot
    print("Creating comparison plot...")
    create_comparison_plot(data, output_dir)
    
    print(f"\nVisualizations saved to: {output_dir}")

if __name__ == "__main__":
    main() 