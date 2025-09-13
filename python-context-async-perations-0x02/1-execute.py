#!/usr/bin/env python3
import sqlite3


class ExecuteQuery:
    """
    Custom context manager to execute a query with parameters,
    managing both connection and execution.
    """

    def __init__(self, query, params=None, db_name="my_database.db"):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is not None:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery(query, param) as results:
        print(results)
