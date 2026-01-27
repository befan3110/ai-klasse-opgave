# D&D Class Browser Application

A simple three-page tkinter application for browsing, searching, and creating D&D 5e classes.

## Features

### Page 1: Search
- Enter a search term to find D&D classes by name or ability
- Click "Load All" to view all classes in the database

### Page 2: Results
- View search results in a scrollable list
- See class name, ability, and description for each result

### Page 3: Create Entry
- Add new D&D classes to the database
- Fill in: Class Name, Class Ability, and Description
- Click "Create" to save or "Clear" to reset fields

## Project Structure

```
løsning3/
├── main3.py           # Entry point
├── ttkv3.py          # GUI application
├── database.py       # Database operations
├── klasseopgave.py   # Data model (dnd_class)
├── init_db.py        # Database initialization script
└── dndclass.db       # SQLite database
```

## Setup

1. Ensure Python 3.x is installed
2. Install required packages:
   ```bash
   pip install tkinter
   ```

3. Initialize the database (one-time setup):
   ```bash
   python init_db.py
   ```

## Running the Application

```bash
python main3.py
```

## Database

The application uses SQLite with the following tables:
- `dnd5_classes` - Stores D&D class information
- `dnd5_class_spells` - Maps classes to spells
- `dnd5_spells` - Stores spell information

## Navigation

- Click the buttons at the top to switch between pages:
  - 🔍 Search - Search for classes
  - 📋 Results - View search results
  - ➕ Create - Create new classes

## Data Model

Each D&D class has:
- `class_id` - Unique identifier
- `class_name` - Name of the class
- `class_ability` - Primary ability score
- `class_description` - Description of the class
