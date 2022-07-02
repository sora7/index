import pyodbc

connect_str = (
    'DRIVER={Microsoft Access Driver (*.mdb)};'
    'DBQ=e:/OneWayRoad/titles.mdb;'
    )

connection = pyodbc.connect(connect_str)
cursor = connection.cursor()

query = 'SELECT ALL FROM titles;'

cursor.execute(query)

for row in cursor.fetchall():
    print(row)

##row = cursor.fetchone() 
##while row: 
##    print(row[0])
##    row = cursor.fetchone()
