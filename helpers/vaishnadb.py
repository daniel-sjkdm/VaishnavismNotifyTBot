import os
import psycopg2
import sqlite3


class VaishnaDBPG():
    def __init__(self):
        self.dbname = dbname=os.getenv('PGDATABASE'),
        self.host = os.getenv('PGHOST'),
        self.user = os.getenv('PGUSER'),
        self.password = os.getenv('PGPASSWORD'),
        self.port = os.getenv('PGPORT')


    def get_db_connection(self):

        connection = psycopg2.connect(
            dbname=self.dbname,
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )

        return connection


    def get_iskcon_events(self, data, fetch_by):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            if fetch_by == "year":
                cursor.execute("SELECT * FROM iskcon_events WHERE year=%s", (data,))
            elif fetch_by == "month":
                cursor.execute("SELECT * FROM iskcon_events WHERE month=%s", (data,))
            else:
                cursor.execute("SELECT * FROM iskcon_events WHERE month=%s AND year=%s", (data[0], data[1]))
            events = cursor.fetchall()
            return events


    def get_ekadasi_events(self, data, fetch_by):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            if fetch_by == "year":
                cursor.execute("SELECT * FROM ekadasi_events WHERE year=%s", (data,))
            elif fetch_by == "month":
                cursor.execute("SELECT * FROM ekadasi_events WHERE month=%s", (data,))
            else:
                cursor.execute("SELECT * FROM ekadasi_events WHERE month=%s AND year=%s", (data[0], data[1]))
        events = cursor.fetchall()
        return events



class VaishnaDBSQLite():
    
    def get_iskcon_events(self, data, fetch_by):
        print(data, fetch_by)
        with sqlite3.connect("data/vaishnadb.db") as conn:
            print(conn)
            cursor = conn.cursor()
            if fetch_by == "year":
                print("fetch by year")
                cursor.execute("SELECT * FROM iskcon_events WHERE year=?", (data,))
            elif fetch_by == "month":
                print("fetch by month")
                cursor.execute("SELECT * FROM iskcon_events WHERE month=?", (data,))
            else:
                print("fetch by month and year")
                cursor.execute("SELECT * FROM iskcon_events WHERE month=? AND year=?", (data[0], data[1]))
            events = cursor.fetchall()
            print(events)
            return events


    def get_ekadasi_events(self, data, fetch_by):
        print(data)
        with sqlite3.connect("data/vaishnadb.db") as conn:
            print(conn, fetch_by)
            cursor = conn.cursor()
            if fetch_by == "year":
                print("fetch by year")
                cursor.execute("SELECT * FROM ekadasi_dates WHERE year=?", (data,))
            elif fetch_by == "month":
                print("fetch by month")
                cursor.execute("SELECT * FROM ekadasi_dates WHERE month=?", (data,))
            else:
                print("fetch by month and year")
                cursor.execute("SELECT * FROM ekadasi_dates WHERE month=? AND year=?", (data[0], data[1]))
            events = cursor.fetchall()
            print(events)
            return events