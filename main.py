from fastapi import FastAPI
from pydantic import BaseModel, Field
import pyodbc

# print(pyodbc.drivers())
# cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for SQL Server};Server=TOMSM16;Database=Todolistdb;User ID=TomsM16\\tombl;Trusted_connection=yes;')

connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=TOMSM16;DATABASE=Todolistdb;Trusted_connection=yes;'

try:
    cnxn = pyodbc.connect(connectionString)
    print("Connected to the database.")
except pyodbc.Error as e:
    print(e)
    exit()

# Function to return the sql results as a dict. 
# It also maps the column names and values for the dict
# Returns no results found if there are no records
def mssql_result2dict(cursor):
    try: 
        result = []
        # columns = [column[0] for column in cursor.description]
        # for row in  cursor.fetchall():
        #     result.append(dict(zip(columns,row)))
        
        fetched_rows = cursor.fetchall()

        # Check if fetched_rows is not None before attempting to iterate
        if fetched_rows is not None:
            for row in fetched_rows:
                result.append(dict(zip(columns, row)))
        
        print(result)

        #Check for results
        if len(result) > 0:
            ret = result
        else:
            ret = {"message": "no results found"}
    except pyodbc.Error as e:
        print(e)
        ret = { "message": "Internal Database Query Error"}
    
    return ret

# CLRUD aka CRUD model to update your database
# Create - Create record in the database
# List - List all records
# Read - Read one record
# Update - Update one record
# Delete - Delete one record
class TodoTableModel:
    # Database table
    table = "dbo.TodoItems"

    def create(self, data):
        sql = f'INSERT INTO {self.table} ([title],[notes],[completed]) OUTPUT INSERTED.id VALUES (?,?,?);'
        
        try:
            cursor = cnxn.cursor()
            row = cursor.execute(sql, data.title, data.notes, data.completed).fetchone()
            cnxn.commit()
            ret = {"message": "created", "id": row[0]}
        except pyodbc.Error as e:
            print(f'Insert Failed')
            print(e)
            ret = {"message": "failed to create record"}
       
        return ret

    
    def list(self, id = None):
        sql = f'SELECT * FROM {self.table}'
        
        try:
            cursor = cnxn.cursor()
            cursor.execute(sql)
            ret = mssql_result2dict(cursor)
            cnxn.commit()
        except pyodbc.Error as e:
            print(f'SQL Query Failed: {e}')
            ret = {"message": "system error"}
        
        return ret

    def read(self, id = None):
        if not id: 
            return {"message": "id not set"}

        sql = f'SELECT * FROM {self.table} WHERE id=?'
        
        try:
            cursor = cnxn.cursor()
            cursor.execute(sql, id)
            ret = mssql_result2dict(cursor)
            cnxn.commit()
        except pyodbc.Error as e:
            print(f'SQL Query Failed: {e}')
            ret = {"message": "system error"}
        
        return ret
    
    
    def update(self,id = None, data = None):
        if not id: 
            return {"message": "id not set"}

        sql = f'UPDATE {self.table} set name=?, value=?, date=?, comment=? WHERE id=?'
        
        try:
            cursor = cnxn.cursor()
            cursor.execute(sql, data.name, data.value, data.date, data.comment, id)
            ret = {"message": "updated"}
            cnxn.commit()
        except pyodbc.Error as e:
            print(f'SQL Query Failed: {e}')
            ret = {"message": "system error"}
        
        return ret

    def delete(self,id = None):
        if not id: 
            return {"message": "id not set"}

        sql = f'DELETE FROM {self.table} WHERE id=?'
        
        try:
            cursor = cnxn.cursor()
            cursor.execute(sql, id)
            ret = {"message": "deleted"}
            cnxn.commit()
        except pyodbc.Error as e:
            print(f'SQL Query Failed: {e}')
            ret = {"message": "system error"}
        
        return ret

# cursor = cnxn.cursor()
# cursor.execute("INSERT INTO TodoItems (title, notes, completed) VALUES ('Test', 'Test Entry', 1)") 

# print(mssql_result2dict(cnxn.cursor()))

cursor = cnxn.cursor()	
print(mssql_result2dict(cursor))
# print(cursor.execute("SELECT * FROM TodoItems"))
# row = cursor.fetchall()
# while row:
#     print (row) 
#     row = cursor.fetchone()

# app = FastAPI()
# Testing
