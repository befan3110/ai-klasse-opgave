import sqlite3
from pathlib import Path
from klasseopgave import dnd_class

BASE_DIR = Path(__file__).resolve().parent
DB_DND = str((BASE_DIR / "dndclass.db").resolve())


class Database:
    def __init__(self, db_path: str = DB_DND):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _execute(self, query, params=()):
        with self._connect() as conn:
            conn.execute(query, params)
            conn.commit()

    def _query(self, query, params=()):
        with self._connect() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def _row_to_class(self, row):
        """Convert database row to dnd_class object"""
        return dnd_class(
            class_id=row["class_id"],
            class_name=row["class_name"],
            class_ability=row["class_ability"],
            class_description=row["class_description"]
        )

    def search(self, term: str):
        """Search for classes by name or ability"""
        query = "SELECT * FROM dnd5_classes WHERE class_name LIKE ? OR class_ability LIKE ?"
        rows = self._query(query, (f"%{term}%", f"%{term}%"))
        return [self._row_to_class(row) for row in rows]

    def load(self, class_id: int):
        """Load a single class by ID"""
        query = "SELECT * FROM dnd5_classes WHERE class_id = ?"
        rows = self._query(query, (class_id,))
        return self._row_to_class(rows[0]) if rows else None

    def load_all(self):
        """Load all classes"""
        query = "SELECT * FROM dnd5_classes"
        rows = self._query(query)
        return [self._row_to_class(row) for row in rows]

    def insert(self, class_name, class_ability, class_description):
        """Insert a new class"""
        query = "INSERT INTO dnd5_classes (class_name, class_ability, class_description) VALUES (?, ?, ?)"
        self._execute(query, (class_name, class_ability, class_description))

    def update(self, class_id: int, updated: dnd_class):
        """Update a class"""
        query = "UPDATE dnd5_classes SET class_name = ?, class_ability = ?, class_description = ? WHERE class_id = ?"
        self._execute(query, (updated.class_name, updated.class_ability, updated.class_description, class_id))

    def delete(self, class_id: int):
        """Delete a class"""
        query = "DELETE FROM dnd5_classes WHERE class_id = ?"
        self._execute(query, (class_id,))


if __name__ == "__main__":
    db = Database()
    print("All classes:")
    for row in db.load_all():
        print(f"  • {row.class_name} ({row.class_ability})")

