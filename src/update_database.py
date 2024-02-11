import sqlite3
import pandas as pd

# Connect to your SQLite database
db_path = 'new_test_database.db'  # Change this to your actual database path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS breed_requirements")
cursor.execute("DROP TABLE IF EXISTS breeds")

# Recreate 'breeds' table
cursor.execute("""
    CREATE TABLE breeds (
        id INTEGER PRIMARY KEY,
        target TEXT
    )
""")

# Recreate 'breed_requirements' table
cursor.execute("""
    CREATE TABLE breed_requirements (
        id INTEGER PRIMARY KEY,
        breed_id INTEGER,
        requirement_type TEXT,
        requirement_value TEXT,
        FOREIGN KEY (breed_id) REFERENCES breeds (id)
    )
""")

# Read CSV data into a pandas DataFrame
csv_path = 'updated_breeding_pairs.csv'  # Change this to your actual CSV file path
df = pd.read_csv(csv_path, header=None, names=['base', 'mate', 'offspring'])

# Function to insert new breeds and requirements into the database
def insert_breed_and_requirements(base, mate, offspring):
    # Insert breed into 'breeds' table
    cursor.execute("INSERT INTO breeds (target) VALUES (?)", (offspring,))
    conn.commit()

    # Get the newly inserted breed_id
    breed_id = cursor.lastrowid

    # Insert requirements into 'breed_requirements' table
    cursor.execute("INSERT INTO breed_requirements (breed_id, requirement_type, requirement_value) VALUES (?, 'base', ?)", (breed_id, base))
    cursor.execute("INSERT INTO breed_requirements (breed_id, requirement_type, requirement_value) VALUES (?, 'mate', ?)", (breed_id, mate))
    conn.commit()

# Iterate through each row in the DataFrame and insert data into the database
for index, row in df.iterrows():
    insert_breed_and_requirements(row['base'], row['mate'], row['offspring'])

# Close the database connection
conn.close()
