import pyodbc

connectionString = 'DRIVER={SQL Server};SERVER=TOMSM16;DATABASE=Todolistdb;Trusted_cnxnection=yes;'
print(pyodbc.drivers())
try:
    cnxn = pyodbc.connect(connectionString)
except pyodbc.Error as e:
    print(e)
    exit()

cursor = cnxn.cursor()	
print(cursor.execute("SELECT * FROM TodoItems"))
row = cursor.fetchall()
while row:
    print (row) 
    row = cursor.fetchone()