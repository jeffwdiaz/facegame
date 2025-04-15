#!/bin/bash

# List of files to remove
FILES=(
    "builds/004.1_data_extraction/src/input/Environment_Emissions_intensities_E_All_Data_(Normalized).csv"
    "builds/004.2_data_chunker/data_chunker/input/Environment_Emissions_intensities_E_All_Data_(Normalized).json"
    "builds/004.1_data_extraction/src/output/Environment_Emissions_intensities_E_All_Data_(Normalized).json"
    "builds/004_data_extraction/src/output/Environment_Emissions_intensities_E_All_Data_(Normalized).json"
)

# Create the filter command
FILTER_CMD="git rm --cached --ignore-unmatch"
for file in "${FILES[@]}"; do
    FILTER_CMD="$FILTER_CMD '$file'"
done

# Run git filter-branch
git filter-branch --force --index-filter "$FILTER_CMD" --prune-empty --tag-name-filter cat -- --all 