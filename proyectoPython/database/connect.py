from dotenv import load_dotenv
import psycopg2
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_NAME = os.getenv("DB_NAME")
# DB_PORT = os.getenv("DB_PORT")


def create_connection():
    conn = psycopg2.connect(
        host="192.168.4.64",
        user="usrsrgbp",
        password=123456,
        dbname="bd_srgbp",
        port=5432
    )
    return conn

def close_connection(conn):
    conn.close()
