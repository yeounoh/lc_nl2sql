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
        fkeys = []
        pkey_exist = False
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

            if pkey == 'PRIMARY KEY' and not pkey_exist:
                create_table_sql += " PRIMARY KEY"
                # to avoid: sqlite3.OperationalError: table "LIBRARY_MATERIAL_STATUS" has more than one primary key
                pkey_exist = True

            if 'FOREIGN KEY' in fkey:
                fkey_parent = fkey.split("FOREIGN KEY")[-1].strip()
                fkeys.append(f" FOREIGN KEY ({column_name}) REFERENCES {fkey_parent}")

            # Add a comma if it's not the last column
            create_table_sql += ", "

        # Remove the trailing comma and space, and close the statement
        if len(fkeys) > 0:
            create_table_sql += ", ".join(fkeys) + ")"
        else:
            create_table_sql = create_table_sql[:-2] + ")"

        # Execute the CREATE TABLE statement
        cursor.execute(create_table_sql)

def load_table_content(cursor, content_file, table_name):
        with open(content_file, 'r') as file:
            reader = csv.reader(file)
            header = next(reader) 
            num_columns = len(header)
            print(f"Number of columns: {num_columns}")
            cols = ", ".join(["?"] * num_columns)

            # Insert data into the table by row to avoid any integriy error:
            # sqlite3.IntegrityError: UNIQUE constraint failed: FCLT_BUILDING_ADDRESS.FCLT_BUILDING_ADDRESS_KEY
            for row in reader:
                try:
                    cursor.execute(f'INSERT INTO {table_name} VALUES ({",".join(["?"] * len(row))})', row)
                except sqlite3.Error as e:
                    print(e)
                    continue


schema_directory = 'schema/dw'
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