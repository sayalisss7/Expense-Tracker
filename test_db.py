import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_tracker"
    )
    print("CONNECTED SUCCESSFULLY")
except Exception as e:
    print("ERROR:", e)