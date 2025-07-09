#!/usr/bin/env python3
import aiosqlite
import asyncio

DB_NAME = "users.db"

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        await cursor.close()
        print("[All Users]", users)
        return users

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        older_users = await cursor.fetchall()
        await cursor.close()
        print("[Users > 40]", older_users)
        return older_users

# Function to run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run the concurrent query execution
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
