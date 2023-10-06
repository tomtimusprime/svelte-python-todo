from fastapi import FastAPI
from pydantic import BaseModel, Field
import pyodbc
from config import CONNECTION_STRING
import uvicorn

app = FastAPI()
# print(pyodbc.drivers())
# cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for SQL Server};Server=TOMSM16;Database=Todolistdb;User ID=TomsM16\\tombl;Trusted_connection=yes;')

# connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=TOMSM16;DATABASE=Todolistdb;Trusted_connection=yes;'

def get_db_connection(connectionString):
    return pyodbc.connect(connectionString)

class TodoItem(BaseModel):
    title: str
    notes: str
    completed: bool


@app.get("/")
def home():
    return {"message": "Welcome to the todo api."}

# Endpoint to create a new todo item
@app.post("/todos/")
def createToDo(todo: TodoItem):
    try:
        connection = get_db_connection(CONNECTION_STRING)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO TodoItems (title, notes, completed) VALUES (?, ?, ?)", todo.title, todo.notes, todo.completed)
        connection.commit()
        
        #Closing the database connection.
        connection.close()

        return {"message": "Todo item created successfully"}     
    except Exception as e:
        return {"Error": str(e)}
    
@app.get("/get-todos/")
def getAllToDos():
    try:
        connection = get_db_connection(CONNECTION_STRING)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM TodoItems")
        rows = cursor.fetchall()
        connection.close()

        todos = []
        for row in rows:
            todo_id, title, notes, completed = row
            todos.append({"id": todo_id, "title": title, "notes": notes, "completed": bool(completed)})
        
        return todos
    except Exception as e:
        return {"Error": str(e)}
    
@app.get("/todo/{todo_id}/")
def getTodo(todo_id: int):
    try:
        connection = get_db_connection(CONNECTION_STRING)
        cursor = connection.cursor()

        cursor.execute("Select * From TodoItems WHERE id = ?", todo_id)
        row = cursor.fetchone()
        connection.close()

        if row:
            todo_id, title, notes, completed = row
            return {"id": todo_id, "title": title, "notes": notes, "completed": bool(completed)}
        else:
            return {"message": "Todo item with that Id not found"}
        
    except Exception as e:
        return {"Error":str(e)}

# connection = get_db_connection(CONNECTION_STRING)
# cursor = connection.cursor()
# cursor.execute("INSERT INTO TodoItems (title, notes, completed) VALUES ('Test', 'Another Entry from main1.py program', 1)")
# connection.commit()     

if __name__ == '__main__':
    uvicorn.run(app, port=9000, host='0.0.0.0')

# try:
#     cnxn = pyodbc.connect(connectionString)
#     print("Connected to the database.")
# except pyodbc.Error as e:
#     print(e)
#     exit()