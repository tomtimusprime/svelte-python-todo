from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
import pyodbc

# print(pyodbc.drivers())
# cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for SQL Server};Server=TOMSM16;Database=Todolistdb;User ID=TomsM16\\tombl;Trusted_Connection=yes;')

connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=TOMSM16;DATABASE=Todolistdb;Trusted_Connection=yes;'

cnxn = pyodbc.connect(connectionString)
# cursor = cnxn.cursor()
# cursor.execute("INSERT INTO TodoItems (title, notes, completed) VALUES ('Test', 'Test Entry', 1)") 

cursor = cnxn.cursor()	
print(cursor.execute("SELECT * FROM TodoItems"))
row = cursor.fetchall()
while row:
    print (row) 
    row = cursor.fetchone()

app = FastAPI()
