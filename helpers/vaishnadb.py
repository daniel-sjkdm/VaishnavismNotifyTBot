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
        return psycopg2.connect(
            dbname=self.dbname,
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )


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
                    events = cursor.fetchall()
                    print(events)
                    return events

    def get_ekadasi_events(self, data, fetch_by):
        with self.get_db_connection() as conn:
            with conn as cursor:
                if fetch_by == "year":
                    cursor.execute("SELECT * FROM ekadasi_events WHERE year=%s", (data,))
                    return cursor.fetchall()
                elif fetch_by == "month":
                    cursor.execute("SELECT * FROM ekadasi_events WHERE month=%s", (data,))
                    return cursor.fetchall()
                else:
                    cursor.execute("SELECT * FROM ekadasi_events WHERE month=%s AND year =%s", (data[0], data[1]))
                    events = cursor.fetchall()
                    print(events)
                    return events
