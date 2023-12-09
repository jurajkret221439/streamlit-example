import pyodbc
import os
# Replace the following strings with your actual server and database information
server = 'thestreetfoodclub.database.windows.net'  # Your server name
database = 'TSFC'  # Your database name
username = 'jurajkret'  # Your username
password = 'Smetisko123'  # Your password

# Connection string
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Attempt to connect to the database
try:
    with pyodbc.connect(connection_string, timeout=10) as conn:
        print("Connection successful.")
except Exception as e:
    print(f"Error connecting to the database: {e}")

# If the script outputs "Connection successful.", the connection works.
# If it prints an error message, that message will help diagnose the problem.