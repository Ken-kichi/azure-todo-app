import pytz
from datetime import datetime


class DatabaseManager:

    def create_record(self, conn, title, description):
        created_time = datetime.now(pytz.timezone(
            'Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S.%f")
        cursor = conn.cursor()
        cursor.execute("""
 INSERT INTO todos (
                    title,
                    description,
                    completed,
                    created_at,
                    updated_at
                    )
                       VALUES (%s, %s, %s, %s, %s);
""", (title, description, False, created_time, created_time))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "TODO is created"}

    def read_all_record(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos;")
        rows = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()
        return rows

    def read_record(self, conn, id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = %s;", (id,))
        row = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()
        return row

    def upload_record(self, conn, id, title, description, completed):
        updated_time = datetime.now(pytz.timezone(
            'Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S.%f")
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET title = %s,description=%s,completed=%s,updated_at = %s WHERE id = %s",
                       (title, description, completed, updated_time, id))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "TODO is updated"}

    def delete_record(self, conn, id):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = %s", (id,))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "TODO is deleted"}

    def get_current_time_japan(self):
        japan_tz = pytz.timezone('Asia/Tokyo')
        current_time = datetime.now(japan_tz)
        return current_time.strftime("%Y-%m-%d %H:%M:%S")
