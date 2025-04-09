import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


class ConnectDB:
    def __init__(self) -> None:
        self.dbhost = os.environ["DBHOST"]
        self.dbname = os.environ["DBNAME"]
        self.password = os.environ["PASSWORD"]
        self.dbuser = os.environ["DBUSER"]
        self.sslmode = os.environ["SSLMODE"]

    def get_connection_uri(self):
        db_uri = f"""
            host={self.dbhost}
            dbname={self.dbname}
            user={self.dbuser}
            password={self.password}
            sslmode={self.sslmode}
        """
        return db_uri

    def get_connection_cls(self, db_uri):
        conn = psycopg2.connect(db_uri)
        return conn


try:
    connect_db = ConnectDB()
    conn_string = connect_db.get_connection_uri()
    conn = connect_db.get_connection_cls(conn_string)
    print("connected")
    cursor = conn.cursor()
    print(type(conn))
    print(type(cursor))
    print("OK")
except Exception as e:
    print(f"Error:{e}")
