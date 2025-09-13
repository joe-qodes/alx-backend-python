#!/usr/bin/env python3
import asyncio
import aiosqlite


async def async_fetch_users():
    """
    Fetch all users asynchronously from the database.
    """
    async with aiosqlite.connect("my_database.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    """
    Fetch users older than 40 asynchronously from the database.
    """
    async with aiosqlite.connect("my_database.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """
    Run multiple database queries concurrently using asyncio.gather.
    """
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All users:")
    print(users)

    print("\nUsers older than 40:")
    print(older_users)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
