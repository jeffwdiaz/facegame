# Changelog

## [Unreleased]

### Added
- Added gender property to person data structure in `data.json`
- Added support for gender-based game modes and filtering

### Removed
- Removed all animations and transitions
- Removed swipe/drag functionality
- Removed high score system
- Removed game timer
- Removed game over modal
- Removed complex event handling

### Changed
- Simplified game to basic click interactions
- Reduced UI to essential elements
- Streamlined game flow
- Simplified name display logic
- Made game over return to start screen

### Technical Details
- Game now uses simple click detection for top/bottom half
- Basic score tracking only
- Minimal UI with just score, face, and names
- Simple wrong answer feedback
- Direct game flow without extra states

### Added
- Created new, simplified animation system in `src/js/utils/animationsManager.js`
- Implemented a flexible animation manager that can animate any CSS property
- Added support for different easing functions:
  - Linear
  - EaseInOutQuad
  - EaseInOutCubic
- Added animation cleanup and management features
- Implemented Hammer.js for touch gesture handling
- Added velocity-based swipe detection for more natural interaction
- Added vertical pan gesture support for image movement

### Changed
- Simplified animation implementation in `GameScreen.js`
- Improved animation control with proper cleanup
- Enhanced animation timing and smoothness
- Made animations more maintainable and extensible
- Simplified touch/mouse event handling using Hammer.js
- Improved swipe detection accuracy
- Consolidated answer handling logic
- Removed redundant event listeners and code

### Removed
- Manual touch and mouse event listeners
- Redundant position tracking code

### Technical Details
- Uses requestAnimationFrame for smooth animations
- Supports numeric and non-numeric property animations
- Includes proper animation cleanup to prevent memory leaks
- Provides flexible easing functions for different animation effects
- Allows for easy addition of new animation types 