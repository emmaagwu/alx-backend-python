#!/usr/bin/env python3
import time
import sqlite3
import functools

# Cache storage
query_cache = {}

# === Paste from Task 1: with_db_connection ===
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# === Cache Query Decorator ===
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = None

        # Try to extract SQL query string from arguments
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 0:
            query = args[0]  # assumes query is the first positional argument after conn

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]

        print(f"[CACHE MISS] Executing and caching query: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# === First call: Executes and caches ===
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# === Second call: Returns from cache ===
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
