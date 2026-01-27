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
        (1, 'artificer', 'intelligence', '-mad scientist personified-'),
        (2, 'barbarian', 'strength', '-big fuck-off muscles-'),
        (3, 'bard', 'charisma', '-dms beware, no character is safe-'),
        (4, 'cleric', 'wisdom', '-never piss off the healer-'),
        (5, 'druid', 'wisdom', '-hippies-'),
        (6, 'fighter', 'strength', '-big stick go BONK-'),
        (7, 'monk', 'dexterity', '-i punch this guy 18 times!-'),
        (8, 'paladin', 'strength', '-murdering with the power of god-'),
        (9, 'ranger', 'dexterity', '-the sniper *queue TF2 music*-'),
        (10, 'rogue', 'dexterity', '-i sneak attack him foooor... 55d6 damage-'),
        (11, 'sorcerer', 'charisma', '-magic through the power of rizz-'),
        (12, 'warlock', 'charisma', '-magic through the power of sugar daddies-'),
        (13, 'wizard', 'intelligence', '-spend 20 years reading books, just to find out you just have to believe hard enough-'),
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
