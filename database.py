import mysql.connector

def get_db():
    return mysql.connector.connect(
        user="root",
        password="root123",
        database="job_tracker",
        unix_socket="/tmp/mysql.sock"
    )