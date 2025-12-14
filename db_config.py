import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="priya@2004",
        database="movie_ticket_db"
    )



