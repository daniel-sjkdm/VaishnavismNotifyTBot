import os
import psycopg2


class VaishnaDB():
    def __init__(self):
        self.dbname = dbname=os.getenv('PGDATABASE'),
        self.host = os.getenv('PGHOST'),
        self.user = os.getenv('PGUSER'),
        self.password = os.getenv('PGPASSWORD'),
        self.port = os.getenv('PGPORT')


    def get_db_connection(self):

        print("Requested a connection to the database")

        connection = psycopg2.connect(
            dbname=self.dbname,
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )

        print("Connection was created, not sure if valid...")
        print(f"Connection: {connection}")

        return connection


    def get_iskcon_events(self, data, fetch_by):
        print("1. Fetch iskcon events")
        conn = self.get_db_connection()
        print("1.2 Connection = ", conn.status)
        with conn.cursor() as cursor:
            print("2. Cursor = ", cursor)
            if fetch_by == "year":
                cursor.execute("SELECT * FROM iskcon_events WHERE year=%s", (data,))
                events = cursor.fetchall()
            elif fetch_by == "month":
                cursor.execute("SELECT * FROM iskcon_events WHERE month=%s", (data,))
                events = cursor.fetchall()
            else:
                cursor.execute("SELECT * FROM iskcon_events WHERE month=%s AND year =%s", (data[0], data[1]))
                events = cursor.fetchall()
            print(events)
        conn.close()
        return events


    def get_ekadasi_events(self, data, fetch_by):
        print("1. Fetch ekadasi events")
        conn = self.get_db_connection()
        print("2. Connection = ", conn.status)
        with conn as cursor:
            print("3. Cursor = ", cursor)
            if fetch_by == "year":
                cursor.execute("SELECT * FROM ekadasi_events WHERE year=%s", (data,))
                events = cursor.fetchall()
            elif fetch_by == "month":
                cursor.execute("SELECT * FROM ekadasi_events WHERE month=%s", (data,))
                events = cursor.fetchall()
            else:
                cursor.execute("SELECT * FROM ekadasi_events WHERE month=%s AND year =%s", (data[0], data[1]))
                events = cursor.fetchall()
            print(events)
        conn.close()
        return events