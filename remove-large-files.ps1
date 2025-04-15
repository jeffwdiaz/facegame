# List of files to remove
$files = @(
    "builds/004.1_data_extraction/src/input/Environment_Emissions_intensities_E_All_Data_(Normalized).csv",
    "builds/004.2_data_chunker/data_chunker/input/Environment_Emissions_intensities_E_All_Data_(Normalized).json",
    "builds/004.1_data_extraction/src/output/Environment_Emissions_intensities_E_All_Data_(Normalized).json",
    "builds/004_data_extraction/src/output/Environment_Emissions_intensities_E_All_Data_(Normalized).json"
)

# Create a backup branch
git branch backup-before-filter

# Remove each file from Git history
foreach ($file in $files) {
    Write-Host "Removing $file from Git history..."
    git filter-branch --force --index-filter "git rm --cached --ignore-unmatch '$file'" --prune-empty --tag-name-filter cat -- --all
}

# Clean up Git references
git for-each-ref --format="delete %(refname)" refs/original/ | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive 