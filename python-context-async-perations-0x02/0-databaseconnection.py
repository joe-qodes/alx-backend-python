#!/usr/bin/env python3
import sqlite3


class DatabaseConnection:
    """
    Custom context manager to handle opening and closing
    SQLite database connections automatically.
    """

    def __init__(self, db_name="my_database.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is not None:
                # Rollback if there was an exception
                self.conn.rollback()
            else:
                # Commit changes if no exception
                self.conn.commit()
            self.conn.close()


if __name__ == "__main__":
    with DatabaseConnection("my_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
