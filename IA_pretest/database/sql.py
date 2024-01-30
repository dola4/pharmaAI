import mysql.connector 

def get_cursor():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pharmaai"
    )
    cursor = connection.cursor()
    return cursor, connection