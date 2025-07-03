# #!/usr/bin/env python3
# import mysql.connector
# from config import DB_CONFIG

# def stream_users_in_batches(batch_size):
#     """
#     Generator that yields users in batches from the user_data table.
#     Each batch contains up to `batch_size` user rows as a list of dicts.
#     """
#     connection = None
#     cursor = None

#     try:
#         connection = mysql.connector.connect(
#             host=DB_CONFIG["host"],
#             user=DB_CONFIG["user"],
#             password=DB_CONFIG["password"],
#             database=DB_CONFIG["database"]
#         )
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT user_id, name, email, age FROM user_data")

#         # Loop over cursor in chunks of batch_size
#         while True:
#             batch = cursor.fetchmany(batch_size)
#             if not batch:
#                 break
#             yield batch

    
#     finally:
#         # Clear any unread results (avoids "Unread result found")
#         if cursor:
#             try:
#                 while cursor.nextset():
#                     pass
#             except:
#                 pass
#             try:
#                 cursor.close()
#             except:
#                 pass
#         if connection and connection.is_connected():
#             try:
#                 connection.close()
#             except:
#                 pass


# def batch_processing(batch_size):
#     """
#     Processes users batch by batch and prints those over age 25.
#     """
#     for batch in stream_users_in_batches(batch_size):  # loop 1
#         for user in batch:  # loop 2
#             if user["age"] > 25:
#                 print(user)


#!/usr/bin/env python3
import mysql.connector
from config import DB_CONFIG

def stream_users_in_batches(batch_size):
    """
    Generator that yields users in batches from the user_data table.
    Each batch contains up to `batch_size` user rows as a list of dicts.
    """
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        # Use iter to avoid explicit while loop
        fetch_batch = cursor.fetchmany
        for batch in iter(lambda: fetch_batch(batch_size), []):  # loop 1
            yield batch

    finally:
        if cursor:
            try:
                while cursor.nextset():
                    pass
            except:
                pass
            try:
                cursor.close()
            except:
                pass
        if connection and connection.is_connected():
            try:
                connection.close()
            except:
                pass


def batch_processing(batch_size):
    """
    Processes users batch by batch and prints those over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 2
        for user in batch:  # loop 3
            if user["age"] > 25:
                print(user)
