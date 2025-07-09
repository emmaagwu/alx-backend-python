#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=(), db_name="users.db"):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# === Usage Example ===
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    print(results)
