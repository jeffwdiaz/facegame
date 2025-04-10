"""
Script to visualize environmental impact data from the cattle farming tables.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('bmh')  # Using a built-in style
sns.set_palette("husl")

# Define paths
ROOT_DIR = Path(__file__).parent.parent
PROCESSED_DATA_DIR = ROOT_DIR / "data" / "processed"
FIGURES_DIR = ROOT_DIR / "figures"

def load_resource_tables():
    """Load the resource use and emission tables."""
    tables = {}
    regions = {
        14: "Northeast",
        15: "Northern Plains",
        16: "Northwest"
    }
    
    for table_num in regions.keys():
        file_path = PROCESSED_DATA_DIR / f"table_{table_num}.csv"
        print(f"\nLoading {file_path}")
        
        df = pd.read_csv(file_path)
        print(f"Columns: {df.columns.tolist()}")
        print(f"Sample data:\n{df.head()}")
        
        # Clean up the data
        df = df[df['Resource use or emission'].notna()]  # Remove empty rows
        df['Region'] = regions[table_num]
        tables[regions[table_num]] = df
    
    return tables

def plot_total_emissions(tables):
    """Plot total emissions for each region."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Prepare data for plotting
    plot_data = []
    for region, df in tables.items():
        # Find rows with GHG emissions and 'Total' column
        emissions = df[
            (df['Resource use or emission'].str.contains('GHG', na=False)) &
            (df['Total'].notna())
        ]
        
        if not emissions.empty:
            for _, row in emissions.iterrows():
                plot_data.append({
                    'Region': region,
                    'Emission Type': row['Resource use or emission'],
                    'Total Emissions': pd.to_numeric(row['Total'], errors='coerce')
                })
    
    if plot_data:
        plot_df = pd.DataFrame(plot_data)
        print("\nPlot data:")
        print(plot_df)
        
        # Create bar plot
        sns.barplot(data=plot_df, x='Region', y='Total Emissions', hue='Emission Type', ax=ax)
        ax.set_title('Total GHG Emissions by Region')
        ax.set_ylabel('Emissions')
        plt.xticks(rotation=45)
        plt.tight_layout()
    else:
        print("No emission data found for plotting")
    
    return fig

def plot_resource_usage(tables):
    """Plot resource usage comparison."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Prepare data for plotting
    plot_data = []
    resources_of_interest = ['Water', 'Energy', 'Land']
    
    for region, df in tables.items():
        for resource in resources_of_interest:
            resource_rows = df[
                df['Resource use or emission'].str.contains(resource, na=False, case=False)
            ]
            
            if not resource_rows.empty:
                for _, row in resource_rows.iterrows():
                    plot_data.append({
                        'Region': region,
                        'Resource': row['Resource use or emission'],
                        'Amount': pd.to_numeric(row['Total'], errors='coerce')
                    })
    
    if plot_data:
        plot_df = pd.DataFrame(plot_data)
        print("\nResource usage data:")
        print(plot_df)
        
        # Create bar plot
        sns.barplot(data=plot_df, x='Region', y='Amount', hue='Resource', ax=ax)
        ax.set_title('Resource Usage by Region')
        ax.set_ylabel('Amount (see units in data)')
        plt.xticks(rotation=45)
        plt.tight_layout()
    else:
        print("No resource usage data found for plotting")
    
    return fig

def main():
    """Main function to create visualizations."""
    # Create figures directory if it doesn't exist
    FIGURES_DIR.mkdir(exist_ok=True)
    
    # Load the data
    print("Loading data...")
    tables = load_resource_tables()
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    # Plot total emissions
    emissions_fig = plot_total_emissions(tables)
    emissions_path = FIGURES_DIR / 'total_emissions.png'
    print(f"Saving emissions plot to {emissions_path}")
    emissions_fig.savefig(emissions_path)
    
    # Plot resource usage
    resource_fig = plot_resource_usage(tables)
    resource_path = FIGURES_DIR / 'resource_usage.png'
    print(f"Saving resource usage plot to {resource_path}")
    resource_fig.savefig(resource_path)
    
    print(f"\nVisualizations saved to {FIGURES_DIR}")

if __name__ == "__main__":
    main() 