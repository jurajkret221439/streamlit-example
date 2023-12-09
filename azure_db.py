

import pyodbc

# Replace these variables with your own configuration
server = 'thestreetfoodclub.database.windows.net'
database = 'TSFC'
username = 'jurajkret'
password = 'Smetisko123'
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

conn = pyodbc.connect(connectionString)
