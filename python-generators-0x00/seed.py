#!/usr/bin/python3

import mysql.connector
import csv
import os
from config import DB_CONFIG
import uuid

def connect_db():
    try:
        return mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None
    
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Database creation error: {err}")

def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
    except mysql.connector.Error as err:
        print(f"Connection to ALX_prodev failed: {err}")
        return None
    
def create_table(connection):
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Table creation failed: {err}")

def insert_data(connection, csv_file):
    try:
        # Check if CSV file exists
        if not os.path.exists(csv_file):
            print(f"CSV file {csv_file} not found")
            return
            
        cursor = connection.cursor()
        
        # Check if table is already populated
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        if count > 0:
            print("Data already inserted.")
            cursor.close()
            return

        # Insert CSV data
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows_inserted = 0
            
            for row in reader:
                try:
                    # Validate required fields
                    name = row.get('name', '').strip()
                    email = row.get('email', '').strip()
                    age_str = row.get('age', '').strip()
                    
                    # Skip rows with missing data
                    if not name or not email or not age_str:
                        print(f"Skipping row with missing data: {row}")
                        continue
                    
                    # Convert age to integer
                    try:
                        age = int(float(age_str))
                        if age <= 0:
                            print(f"Skipping row with invalid age: {age}")
                            continue
                    except (ValueError, TypeError):
                        print(f"Skipping row with invalid age format: {age_str}")
                        continue
                    
                    # Generate UUID or use provided one
                    user_id = row.get('user_id', '').strip()
                    if not user_id or len(user_id) != 36:
                        user_id = str(uuid.uuid4())
                    
                    query = """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """
                    values = (user_id, name, email, age)
                    cursor.execute(query, values)
                    rows_inserted += 1
                    
                except Exception as row_error:
                    print(f"Error processing row {row}: {row_error}")
                    continue

        connection.commit()
        cursor.close()
        print(f"Data from {csv_file} inserted successfully. {rows_inserted} rows inserted.")
        
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")
    except Exception as e:
        print(f"Error inserting data: {e}")
        if connection and connection.is_connected():
            connection.rollback()