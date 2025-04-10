"""
Script to select and extract specific columns from a CSV file.
"""

import sys
from pathlib import Path
from extractors.csv_extractor import CSVExtractor
import json

def main():
    if len(sys.argv) != 2:
        print("Usage: python select_columns.py <path_to_csv_file>")
        sys.exit(1)
        
    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)
        
    # First, get all headers
    print("\nAvailable columns:")
    headers = CSVExtractor.get_headers(str(csv_path))
    for i, header in enumerate(headers, 1):
        print(f"{i}. {header}")
        
    # Get user selection
    print("\nEnter the numbers of columns you want to extract (comma-separated)")
    print("Example: 1,3,5")
    print("Or press Enter to extract all columns")
    
    selection = input("Your selection: ").strip()
    
    if selection:
        try:
            # Convert selection to column names
            selected_indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_columns = [headers[i] for i in selected_indices]
        except (ValueError, IndexError) as e:
            print(f"Error: Invalid selection. {str(e)}")
            sys.exit(1)
    else:
        selected_columns = None
        
    # Create extractor with selected columns
    extractor = CSVExtractor(preview_lines=5, selected_columns=selected_columns)
    
    try:
        # Extract data
        result = extractor.extract_data(str(csv_path))
        
        # Print basic info
        print(f"\nFile: {csv_path.name}")
        print(f"Selected columns: {selected_columns if selected_columns else 'all'}")
        print(f"Shape: {result['shape'][0]} rows, {result['shape'][1]} columns")
        
        print("\nPreview:")
        for row in result['preview']:
            print(row)
            
        # Save results
        output_path = csv_path.with_suffix('.json')
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=4, default=str)
        print(f"\nFull results saved to: {output_path}")
        
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 