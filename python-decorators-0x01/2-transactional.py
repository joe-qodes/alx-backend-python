#!/usr/bin/env python3
import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that provides a SQLite database connection to the wrapped function.
    Ensures the connection is closed after execution.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("my_database.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def transactional(func):
    """
    Decorator that manages database transactions.
    Commits if the function executes successfully, otherwise rolls back.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email with automatic transaction handling.
    """
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )


if __name__ == "__main__":
    update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
