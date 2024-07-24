
import os
import pandas as pd
import sqlite3

# Paths
csv_file_path = 'newData/treatments_costs table_DP.csv'
sqlite_db_path = 'askdatanew.db'
table_name = 'treatments_costs'

# Check if database file already exists and is not a database
if os.path.exists(sqlite_db_path):
    try:
        # Try connecting to see if it's a valid database
        conn = sqlite3.connect(sqlite_db_path)
        conn.execute('SELECT name FROM sqlite_master WHERE type="table";')
        conn.close()
    except sqlite3.DatabaseError:
        print(f"File {sqlite_db_path} exists and is not a valid database. Removing it.")
        os.remove(sqlite_db_path)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)
print(f"CSV file {csv_file_path} loaded successfully.")

# Connect to (or create) an SQLite database
conn = sqlite3.connect(sqlite_db_path)
print(f"Connected to SQLite database at {sqlite_db_path}.")

# Create a table in the SQLite database

df.to_sql(table_name, conn, if_exists='replace', index=False)
print(f"Data from {csv_file_path} has been uploaded to the {sqlite_db_path} database.")

# Commit and close the connection
conn.commit()
conn.close()
print("Database connection closed.")
