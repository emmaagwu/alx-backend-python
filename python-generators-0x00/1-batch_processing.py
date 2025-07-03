# import mysql.connector
# from config import DB_CONFIG


# def stream_users_in_batches(batch_size):
#     """
#     Generator that yields rows from user_data in batches.
#     """
#     connection = mysql.connector.connect(
#             host=DB_CONFIG["host"],
#             user=DB_CONFIG["user"],
#             password=DB_CONFIG["password"],
#             database=DB_CONFIG["database"]
#     )
#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("SELECT * FROM user_data")
#         while True:
#             batch = cursor.fetchmany(batch_size)
#             if not batch:
#                 break
#             yield batch
#     finally:
#         cursor.close()
#         connection.close()


# def batch_processing(batch_size):
#     """
#     Generator that yields only users over age 25 from batches.
#     """
#     for batch in stream_users_in_batches(batch_size):  # 1st loop
#         print("BATCH:", batch)
#         filtered = [user for user in batch if user['age'] > 25]  # 2nd loop
#         for user in filtered:  # 3rd loop
#             yield user

#     return 


# if __name__ == "__main__":
#     for user in batch_processing(batch_size=3):
#         print(user)


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

        # Loop over cursor in chunks of batch_size
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        # Clear any unread results (avoids "Unread result found")
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
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user["age"] > 25:
                print(user)
    return
