import sqlite3
import csv
import os


def create_table_from_schema(cursor, schema_file, table_name):
    """
    Creates an SQLite table based on schema information from a CSV file.

    Args:
      cursor: The SQLite cursor object.
      schema_file: Path to the CSV file containing the schema.
    """
    with open(schema_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        # Build the CREATE TABLE statement
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for row in reader:
            column_name, data_type, data_length, pkey, fkey = row

            # Map VARCHAR2 to TEXT (SQLite data type)
            if data_type == 'VARCHAR2':
                data_type = 'TEXT'

            # Add column definition
            create_table_sql += f"{column_name} {data_type}"
            if data_length:
                create_table_sql += f"({data_length})"

            if pkey == 'PRIMARY KEY':
                create_table_sql += " PRIMARY KEY"

            if 'FOREIGN KEY' in fkey:
                create_table_sql += f" {fkey}"

            # Add a comma if it's not the last column
            create_table_sql += ", "

        # Remove the trailing comma and space, and close the statement
        create_table_sql = create_table_sql[:-2] + ")"

        # Execute the CREATE TABLE statement
        cursor.execute(create_table_sql)

def load_table_content(cursor, content_file, table_name)
        with open(content_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row if present

            # Insert data into the table
            cursor.executemany(f'INSERT INTO {table_name} VALUES (?, ?, ?)', reader)


# Specify the directory containing your CSV files
schema_directory = 'schema'
db_csv_directory = 'actual'

db_name = 'dw.sqlite'
db_path = os.path.join(db_csv_directory, db_name)
for filename in os.listdir(db_csv_directory):
    if filename.endswith('.csv'):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        table_name = os.path.splitext(filename)[0]
        schema_file = os.path.join(schema_directory, table_name + ".csv")
        content_file = os.path.join(db_csv_directory, table_name + ".csv")
        create_table_from_schema(cursor, schema_file, table_name)
        load_table_content(cursor, content_file, table_name)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Databases created successfully!")