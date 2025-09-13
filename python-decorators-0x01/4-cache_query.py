#!/usr/bin/env python3
import time
import sqlite3
import functools


query_cache = {}


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


def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    Prevents redundant database calls for the same query.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            return query_cache[query]
        print(f"[CACHE MISS] Executing query: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Execute a SQL query and return results with caching enabled.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call → hits DB and caches result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call → returns cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
