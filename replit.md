# Overview

Game Tec Edition is a gamified student tracking and ranking system built with Flask. The application manages student registrations across different educational modalities (Aprendizagem, Técnico, Técnico NEM) and implements a point-based scoring system where students earn or lose points based on various academic and behavioral criteria. The system features individual and bulk student registration, real-time rankings, and a gaming-themed interface to make educational progress tracking more engaging.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- **Styling**: CSS with gaming theme using custom variables and dark color scheme
- **JavaScript**: Vanilla JavaScript for form validation, tooltip initialization, and auto-refresh functionality
- **UI Framework**: Bootstrap 5 with Font Awesome icons for a modern, responsive interface

## Backend Architecture
- **Web Framework**: Flask with modular route organization
- **Application Structure**: Separated into main application file (`app.py`), routes module (`routes.py`), and utilities (`utils.py`)
- **File Upload**: Werkzeug for secure file handling with size limits (16MB) and extension validation
- **Session Management**: Flask's built-in session handling with configurable secret key

## Data Storage
- **Primary Storage**: JSON file-based persistence (`game_tec_data.json`)
- **File Processing**: Pandas for CSV/Excel file parsing during bulk imports
- **Temporary Storage**: System temp directory for uploaded file processing

## Scoring System
- **Criteria Engine**: Predefined point values for academic and behavioral criteria
- **Point Calculation**: Positive and negative point assignments based on student actions
- **Variable Scoring**: Support for dynamic point values (e.g., competition results)

## Key Features
- **Multi-Modal Support**: Three educational tracks (Aprendizagem, Técnico, Técnico NEM)
- **Dual Registration**: Individual student entry and bulk CSV/Excel import
- **Real-Time Rankings**: Dynamic leaderboards with gaming elements (medals, positions)
- **Gamification**: Gaming-themed UI with glow effects, animations, and achievement-style feedback

# External Dependencies

## Python Libraries
- **Flask**: Web framework for application structure and routing
- **Pandas**: Data processing for CSV/Excel file imports and manipulation
- **Werkzeug**: Secure filename handling and file upload utilities

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Font Awesome 6.4.0**: Icon library for gaming-themed visual elements

## File Format Support
- **CSV Files**: Comma-separated values for bulk student imports
- **Excel Files**: .xlsx and .xls formats supported through pandas

## Configuration Dependencies
- **Environment Variables**: SESSION_SECRET for Flask session security
- **File System**: Local file storage for JSON data persistence and temporary file processing