import os  
server = os.environ.get('DB_SERVER')
database = os.environ.get('DB_DATABASE')
username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
driver = '{ODBC Driver 18 for SQL Server}'
l = [server, database, username, password, driver]

print(l)