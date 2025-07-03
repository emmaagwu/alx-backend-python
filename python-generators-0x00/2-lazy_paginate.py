#!/usr/bin/env python3
import mysql.connector
from seed import connect_to_prodev


def paginate_users(page_size, offset):
    """
    Fetches a page of users starting from the given offset.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily paginates users by page size.
    Only one loop is used as required.
    """
    offset = 0
    while True:  # ✅ This is the one and only loop allowed
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
