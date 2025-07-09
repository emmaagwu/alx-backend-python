#!/usr/bin/env python3
import time
import sqlite3
import functools

# === Paste your with_db_connection from Task 1 ===
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# === Retry-on-failure decorator ===
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"[TRY] Attempt {attempt} of {retries}")
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[WARN] Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"[INFO] Retrying in {delay} seconds...")
                        time.sleep(delay)
            print("[ERROR] All retry attempts failed.")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# === Attempt to fetch users with automatic retry on failure ===
users = fetch_users_with_retry()
print(users)
