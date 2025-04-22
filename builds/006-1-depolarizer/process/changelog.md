# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Initial changelog file created in the process folder.
- Frontend layout and styling for Depolarizer implemented.
- Article section and polarizing-language markup added.
- Project summary added to header description.

### Changed
- Switched main layout to a 5-column CSS grid: fixed-width sidebars and a 3-column center.
- Updated `.main-content` to use a minimal, grid-friendly style and removed excess padding/margins.
- Header and URL input now span all 3 columns; header description appears top-right.
- Article section spans all 3 columns.
- Restored `.header h1` CSS for prominent heading.

### Removed
- Old flexbox and max-width layout styles from `.main-content`.
- Redundant/legacy header description and main-content column markup.
