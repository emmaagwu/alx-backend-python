# Python Generator: MySQL Seeder

This script connects to a MySQL database server, creates a database and table if they don't exist, and populates it with user data from a CSV file using memory-efficient practices.

## Features
- Database: `ALX_prodev`
- Table: `user_data`
- Fields: `user_id (UUID)`, `name`, `email`, `age`
- CSV-driven data population
- Skips insertion if data already exists

## Usage

```bash
chmod +x 0-main.py
./0-main.py
