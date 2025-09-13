#!/usr/bin/env python3
import time
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


def retry_on_failure(retries=3, delay=2):
    """
    Decorator factory that retries the wrapped function if it raises an exception.
    Retries up to `retries` times with `delay` seconds between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users from the database with automatic retry on failure.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print(users)
    except Exception as e:
        print(f"Operation failed after retries: {e}")
