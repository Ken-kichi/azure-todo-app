from connect_db import ConnectDB


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS todos;")
    print("Finished dropping table (if existed)")

    cursor.execute(f"""
                   CREATE TABLE todos (id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                   """)
    cursor.execute("SET timezone TO 'Asia/Tokyo';")

    cursor.execute(
        "INSERT INTO todos (title, description, completed) VALUES (%s, %s, %s);", (
            "ABCD", "食事に行く", False)
    )
    cursor.execute(
        "INSERT INTO todos (title, description, completed) VALUES (%s, %s, %s);", (
            "EFGH", "料理を作る", False)
    )
    cursor.execute(
        "INSERT INTO todos (title, description, completed) VALUES (%s, %s, %s);", (
            "IJKL", "買い物をする", False)
    )

    conn.commit()
    cursor.close()
    conn.close()


try:
    connect_db = ConnectDB()
    conn_string = connect_db.get_connection_uri()
    conn = connect_db.get_connection_cls(conn_string)
    create_table(conn)
    print("created database")
except Exception as e:
    print(f"Error:{e}")
