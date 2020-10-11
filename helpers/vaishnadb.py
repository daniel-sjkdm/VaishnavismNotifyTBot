import os
import psycopg2


class VaishnaDB:

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
                    cursor.execute("SELECT * FROM iskcon_event WHERE event_date::TEXT LIKE %(year)s", {"year": f"{data}%"})
                    return cursor.fetchall()
                elif fetch_by == "month":
                    cursor.execute("SELECT * FROM iskcon_event WHERE event_date::TEXT LIKE %(month)s", {"month": f"%-{data}-%"})
                    return cursor.fetchall()
                else:
                    cursor.execute("SELECT * FROM iskcon_event WHERE event_date::TEXT LIKE %(yearmonth)s", {"yearmonth": f"{data[0]}-{data[1]}-%"})
                    return cursor.fetchall()
                

    def get_ekadasi_events(self, data, fetch_by):
        with self.get_db_connection() as conn:
            with conn.cursor() as cursor:
                if fetch_by == "year":
                    cursor.execute("""SELECT * FROM ekadasi_date JOIN ekadasi
                    ON ekadasi_date.ekadasi_id=ekadasi.id  WHERE event_date::TEXT LIKE %(year)s""", {"year": f"{data}%"})
                    return cursor.fetchall()
                elif fetch_by == "month":
                    cursor.execute("""SELECT * FROM ekadasi_date JOIN ekadasi
                    ON ekadasi.id=ekadasi_date.ekadasi_id WHERE event_date::TEXT LIKE %(month)s""", {"month": f"%-{data}-%"})
                    return cursor.fetchall()
                else:
                    cursor.execute("""SELECT * FROM ekadasi_date JOIN ekadasi
                    ON ekadasi.id=ekadasi_date.ekadasi_id WHERE event_date::TEXT LIKE %(yearmonth)s""", {"yearmonth": f"{data[0]}-{data[1]}-%"})
                    return cursor.fetchall()