import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "dndclass.db"


def init_database():
    """Initialize the database with D&D class tables"""
    
    # Remove existing database to start fresh
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Removed existing database")
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Create tables for SQLite
    print("Creating tables...")
    
    cursor.execute("""
        CREATE TABLE dnd5_classes (
            class_id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            class_ability TEXT,
            class_description TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE dnd5_spells (
            spell_id INTEGER PRIMARY KEY AUTOINCREMENT,
            spell_name TEXT NOT NULL,
            spell_level INTEGER,
            spell_type TEXT,
            casting_time TEXT,
            spell_range TEXT,
            components TEXT,
            duration TEXT,
            description TEXT,
            higher_levels TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE dnd5_class_spells (
            class_id INTEGER,
            spell_id INTEGER,
            FOREIGN KEY(class_id) REFERENCES dnd5_classes(class_id),
            FOREIGN KEY(spell_id) REFERENCES dnd5_spells(spell_id)
        )
    """)
    
    # Insert D&D classes with abilities and descriptions
    classes_data = [
        (1, 'Barbarian', 'Strength', 'A fierce warrior fueled by rage and primal power'),
        (2, 'Bard', 'Charisma', 'A charming performer who weaves magic through art and music'),
        (3, 'Cleric', 'Wisdom', 'A devoted servant of a deity who channels divine magic'),
        (4, 'Druid', 'Wisdom', 'A shapeshifter connected to nature and its primal forces'),
        (5, 'Fighter', 'Strength', 'A master of combat with extensive martial training'),
        (6, 'Monk', 'Dexterity', 'A disciplined martial artist with supernatural abilities'),
        (7, 'Paladin', 'Strength', 'A righteous warrior bound by sacred oath and conviction'),
        (8, 'Ranger', 'Dexterity', 'A skilled tracker and archer of the wilderness'),
        (9, 'Rogue', 'Dexterity', 'A cunning operative specializing in stealth and precision'),
        (10, 'Sorcerer', 'Charisma', 'A spellcaster with innate magical blood and power'),
        (11, 'Warlock', 'Charisma', 'A spellcaster bound by pact with an otherworldly patron'),
        (12, 'Wizard', 'Intelligence', 'A scholarly mage who masters magic through study'),
    ]
    
    cursor.executemany("""
        INSERT INTO dnd5_classes (class_id, class_name, class_ability, class_description)
        VALUES (?, ?, ?, ?)
    """, classes_data)
    
    conn.commit()
    conn.close()
    print(f"Database initialized successfully at {DB_PATH}")


if __name__ == "__main__":
    init_database()
