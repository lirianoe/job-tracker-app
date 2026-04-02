import mysql.connector
import os

def get_db():
    return mysql.connector.connect(
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="job_tracker",
        unix_socket="/tmp/mysql.sock"
    )