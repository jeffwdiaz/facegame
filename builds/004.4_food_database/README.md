# Document Database Project

A structured document database system for managing and processing data.

## Project Structure

```
.
├── src/
│   └── database/
│       ├── models/      # Database models and schemas
│       ├── repositories/# Database access and CRUD operations
│       ├── services/    # Business logic and data processing
│       ├── types/       # TypeScript type definitions
│       └── utils/       # Database utility functions
├── data/
│   └── processed/       # Processed JSON data files
├── .gitignore          # Git ignore rules
└── CHANGELOG.md        # Project changelog
```

## Directory Descriptions

### `src/database/`

- **models/**: Contains document schemas and data models
  - Define data structures
  - Validation rules
  - Schema definitions

- **repositories/**: Database access layer
  - CRUD operations
  - Query builders
  - Database connections

- **services/**: Business logic layer
  - Data processing
  - Business rules
  - Complex operations

- **types/**: TypeScript definitions
  - Interfaces
  - Type definitions
  - Shared types

- **utils/**: Helper functions
  - Database utilities
  - Common functions
  - Error handling

### `data/processed/`

- Stores processed JSON data files
- Subdirectories can be created for different data categories
- Files in this directory are ignored by git (except schema files)

## Setup

1. Clone the repository
2. Install dependencies (when added)
3. Configure environment variables (when needed)
4. Process your data files into the `data/processed/` directory

## Data Management

- Place processed JSON files in `data/processed/`
- Create subdirectories for different data categories
- Use descriptive filenames (e.g., `category-date.json`)
- Schema files are version controlled, other data files are not

## Development

- Follow TypeScript best practices
- Maintain type safety throughout the codebase
- Use the repository pattern for database access
- Keep business logic in services
- Update CHANGELOG.md for all notable changes

## Git Ignore Rules

The `.gitignore` file is configured to:
- Ignore all JSON files in `data/processed/`
- Keep schema files for version control
- Exclude common development files
- Ignore build outputs and dependencies

## Contributing

1. Follow the project structure
2. Maintain type safety
3. Add appropriate documentation
4. Follow the repository pattern

## License

[Add your license information here] 