import sqlite3
import csv
import json
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

        metadata = {
                'columns': list(),
                'primary_keys': list(),
                'foreign_keys': list()
                }
        # Build the CREATE TABLE statement
        fkeys = []
        pkey_exist = False #disable pkey as the original DB violates UNIQUE constraints
        col_idx = 0
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
                #create_table_sql += " PRIMARY KEY"
                # to avoid: sqlite3.OperationalError: table "LIBRARY_MATERIAL_STATUS" has more than one primary key
                metadata['primary_keys'].append(col_idx)

            if 'FOREIGN KEY' in fkey:
                fkey_parent = fkey.split("FOREIGN KEY")[-1].strip()
                fkeys.append(f" FOREIGN KEY ({column_name}) REFERENCES {fkey_parent}")
            
            metadata['columns'].append((column_name, data_type))
            col_idx += 1

            # Add a comma if it's not the last column
            create_table_sql += ", "
        if len(metadata['primary_keys']) > 0:
            pkeys = []
            for idx in metadata['primary_keys']:
                pkeys.append(metadata['columns'][idx][0])
            pkey_str = f'PRIMARY KEY ({",".join(pkeys)})'
            create_table_sql += pkey_str + ", "

        # Remove the trailing comma and space, and close the statement
        if len(fkeys) > 0:
            create_table_sql += ", ".join(fkeys) + ")"
        else:
            create_table_sql = create_table_sql[:-2] + ")"
        # Execute the CREATE TABLE statement
        cursor.execute(create_table_sql)

        # Return the table object
        return metadata

def load_table_content(cursor, content_file, table_name):
        with open(content_file, 'r') as file:
            reader = csv.reader(file)
            header = next(reader) 
            num_columns = len(header)
            print(f"Number of columns: {num_columns}")
            cols = ", ".join(["?"] * num_columns)

            # Insert data into the table by row to avoid any integriy error:
            # sqlite3.IntegrityError: UNIQUE constraint failed: ...
            for row in reader:
                try:
                    cursor.execute(f'INSERT OR IGNORE INTO {table_name} VALUES ({",".join(["?"] * len(row))})', row)
                except sqlite3.Error as e:
                    print(e)
                    raise


schema_directory = 'schema/dw'
db_csv_directory = 'actual'

db_name = 'dw.sqlite'
db_path = os.path.join('databases/dw', db_name)
db_tables = {'db_id': 'dw', 
             'table_names_original': list(), 
             'table_names': list(),
             'column_names_original': list(),
             'column_names': list(),
             'column_types': list(),
             'primary_keys': list(),
             'foreign_keys': list()
             }
tbl_idx = 0
for filename in os.listdir(db_csv_directory):
    if filename.endswith('.csv'):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        table_name = os.path.splitext(filename)[0]
        db_tables['table_names_original'].append(table_name)
        db_tables['table_names'].append(table_name)
        schema_file = os.path.join(schema_directory, table_name + ".csv")
        content_file = os.path.join(db_csv_directory, table_name + ".csv")
        metadata = create_table_from_schema(cursor, schema_file, table_name)
        load_table_content(cursor, content_file, table_name)
        # Commit changes and close the connection
        conn.commit()
        conn.close()

        db_tables['column_names_original'].append([-1, "*"])
        db_tables['column_names'].append([-1, "*"])
        db_tables['column_types'].append("text")
        for c in metadata['columns']:
            db_tables['column_names_original'].append([tbl_idx, c[0]])
            db_tables['column_names'].append([tbl_idx, c[0]])
            db_tables['column_types'].append([tbl_idx, c[1]])
        pkeys = metadata['primary_keys']
        if len(pkeys) == 1:
            db_tables['primary_keys'].append(pkeys[0])
        elif len(pkeys) > 1:
            db_tables['primary_keys'].append(pkeys)
        tbl_idx += 1



print("Databases created successfully!")

with open(os.path.join('tables.json'), 'w') as file:
    file.write(json.dumps([db_tables]))

print("Tables metadata file created successfully!")
