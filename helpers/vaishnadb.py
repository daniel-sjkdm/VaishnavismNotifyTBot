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

        connection = psycopg2.connect(
            dbname=self.dbname,
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )

        if connection.status == 1:
            print("Connected to the postgresql database")
            return connection
        else:
            print("There was an error")


    def get_iskcon_events(self, data, fetch_by):
        print("fetch iskcon events")
        with self.get_db_connection() as conn:
            with conn.cursor() as cursor:
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
                return events

    def get_ekadasi_events(self, data, fetch_by):
        print("Fetch ekadasi events")
        with self.get_db_connection() as conn:
            with conn as cursor:
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
                return events
