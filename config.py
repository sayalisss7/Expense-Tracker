import mysql.connector

DEFAULT_USER_ID = 1

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_tracker",
      
    )



def get_cursor():
    conn = get_connection()
    return conn, conn.cursor(dictionary=True)