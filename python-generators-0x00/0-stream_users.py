#!/usr/bin/env python

import mysql.connector
from config import DB_CONFIG

def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    
    Yields:
        dict: A dictionary containing user data with keys: user_id, name, email, age
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Execute query to fetch all users
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        # Yield each row one by one
        try:
            for row in cursor:
                yield row
        finally:
            # This inner finally ensures cleanup happens even if generator is not exhausted
            if cursor:
                try:
                    # Consume remaining results if any
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
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return


# This makes the module callable - when someone calls the imported module,
# it will actually call the stream_users function
def __call__():
    return stream_users()

# Alternative approach: replace the module with the function
import sys
sys.modules[__name__] = stream_users