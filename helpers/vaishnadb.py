import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path="bot/.env")

class VaishnaDBPG():

    dbname = os.getenv('PGDATABASE')
    host = os.getenv('PGHOST')
    user = os.getenv('PGUSER')
    password = os.getenv('PGPASSWORD')
    port = os.getenv('PGPORT')
    

    def get_db_connection(self):
        conn = psycopg2.connect(
            dbname=self.dbname,
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )

        if conn.status == 1:
            return conn
        else:
            raise Exception("Connection failed")


    def get_iskcon_events(self, data, fetch_by):
        with self.get_db_connection() as conn:
            with conn.cursor() as cursor:
                if fetch_by == "year":
                    cursor.execute("SELECT * FROM iskcon_events WHERE year=%s", (data,))
                    return cursor.fetchall()
                elif fetch_by == "month":
                    cursor.execute("SELECT * FROM iskcon_events WHERE month=%s", (data,))
                    return cursor.fetchall()
                else:
                    cursor.execute("SELECT * FROM iskcon_events WHERE month=%s AND year =%s", (data[0], data[1]))
                    return cursor.fetchall()
                

    def get_ekadasi_events(self, data, fetch_by):
        with self.get_db_connection() as conn:
            with conn.cursor() as cursor:
                if fetch_by == "year":
                    cursor.execute("SELECT * FROM ekadasi_events WHERE year=%s", (data,))
                    return cursor.fetchall()
                elif fetch_by == "month":
                    cursor.execute("SELECT * FROM ekadasi_events WHERE month=%s", (data,))
                    return cursor.fetchall()
                else:
                    cursor.execute("SELECT * FROM ekadasi_events WHERE month=%s AND year =%s", (data[0], data[1]))
                    return cursor.fetchall()