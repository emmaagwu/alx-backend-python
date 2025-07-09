#!/usr/bin/env python3
import mysql.connector
from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator that yields user ages one at a time from the user_data table.
    """
    conn = connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # ✅ 1st and ONLY loop here
        yield age

    cursor.close()
    conn.close()


def calculate_average_age():
    """
    Calculates and prints the average age using the generator.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # ✅ 2nd loop
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.1f}")


# Run the script
if __name__ == "__main__":
    calculate_average_age()