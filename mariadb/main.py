import pymysql
import pandas as pd

# Database connection details
db_config = {
    "host": "localhost",          # e.g., 'localhost'
    "user": "root",      # e.g., 'root'
    "password": "root",  # e.g., 'password'
    "database": "shippix"   # e.g., 'test_db'
}

# CSV file details
csv_file_path = "worldcitiespop.csv"  # Path to your CSV file
table_name = "worldcitiespop"        # Name of the table to insert data

# Establish database connection
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    print("Connected to the database successfully!")

    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Handle NaN values (replace with empty string or NULL)
    df.fillna(value='', inplace=True)  # Replace NaN with empty string

    # Create table query (adjust columns and types as needed)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join([f'{col} TEXT' for col in df.columns])}
    )
    """
    cursor.execute(create_table_query)
    print(f"Table `{table_name}` created successfully (if it didn't already exist).")

    # Insert DataFrame into the database table
    for index, row in df.iterrows():
        placeholders = ", ".join(["%s"] * len(row))
        insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"
        cursor.execute(insert_query, tuple(row))

    connection.commit()
    print("Data inserted into the table successfully!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if connection:
        connection.close()
        print("Database connection closed.")

# import pymysql
# import pandas as pd

# # Database connection details
# db_config = {
#     "host": "localhost",          # e.g., 'localhost'
#     "user": "root",      # e.g., 'root'
#     "password": "root",  # e.g., 'password'
#     "database": "shippix"   # e.g., 'test_db'
# }

# # CSV file details
# csv_file_path = "worldcitiespop.csv"  # Path to your CSV file
# table_name = "worldcitiespop"        # Name of the table to insert data

# # Establish database connection
# try:
#     connection = pymysql.connect(**db_config)
#     cursor = connection.cursor()
#     print("Connected to the database successfully!")

#     # Read CSV file into a DataFrame
#     df = pd.read_csv(csv_file_path)

#     # Create table query (adjust columns and types as needed)
#     create_table_query = f"""
#     CREATE TABLE IF NOT EXISTS {table_name} (
#         {', '.join([f'{col} TEXT' for col in df.columns])}
#     )
#     """
#     cursor.execute(create_table_query)
#     print(f"Table `{table_name}` created successfully (if it didn't already exist).")

#     # Insert DataFrame into the database table
#     for index, row in df.iterrows():
#         placeholders = ", ".join(["%s"] * len(row))
#         insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"
#         cursor.execute(insert_query, tuple(row))

#     connection.commit()
#     print("Data inserted into the table successfully!")

# except Exception as e:
#     print(f"An error occurred: {e}")

# finally:
#     if connection:
#         connection.close()
#         print("Database connection closed.")
