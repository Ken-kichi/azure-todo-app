from flask import Flask, render_template, request, redirect, url_for
from connect_db import ConnectDB
from db_manager import DatabaseManager
from datetime import datetime
import pytz

app = Flask(__name__)


@app.route('/')
def index():
    try:
        connect_db = ConnectDB()
        conn_string = connect_db.get_connection_uri()
        conn = connect_db.get_connection_cls(conn_string)
        db_maanger = DatabaseManager()
        rows = db_maanger.read_all_record(conn)

        todos = [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "completed": row[3],
                "created_at": row[4],
                "updated_at": row[5]
            } for row in rows
        ]
        message = None
    except Exception as e:
        print(f"Error:{e}")
        todos = []
        message = "Failed to retrieve Todos"
    return render_template('index.html', todos=todos, message=message)


@app.route('/add', methods=['POST', 'GET'])
def add_todo():
    if request.method == "POST":
        try:
            title = request.form.get("title")
            description = request.form.get("description")

            connect_db = ConnectDB()
            conn_string = connect_db.get_connection_uri()
            conn = connect_db.get_connection_cls(conn_string)
            db_manager = DatabaseManager()
            message = db_manager.create_record(
                conn,
                title,
                description
            )["message"]
        except Exception as e:
            print(f"Error:{e}")
            message = "Failed to create Todo"
        return render_template("message.html", message=message)
    return render_template("add.html")


@app.route('/edit/<int:todo_id>', methods=['POST', 'GET'])
def edit_todo(todo_id):
    if todo_id == None:
        redirect(url_for('index'))

    if request.method == "POST":
        try:
            title = request.form.get("title")
            description = request.form.get("description")
            completed = request.form.get("completed")

            connect_db = ConnectDB()
            conn_string = connect_db.get_connection_uri()
            conn = connect_db.get_connection_cls(conn_string)
            db_manager = DatabaseManager()
            message = db_manager.upload_record(
                conn=conn,
                id=todo_id,
                title=title,
                description=description,
                completed=completed
            )["message"]
            return render_template('message.html', message=message)
        except Exception as e:
            message = "Failed to update Todo"
            return render_template('message.html', message=message)

    connect_db = ConnectDB()
    conn_string = connect_db.get_connection_uri()
    conn = connect_db.get_connection_cls(conn_string)
    db_manager = DatabaseManager()
    row = db_manager.read_record(conn, id=todo_id)[0]
    todo = {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "completed": row[3],
        "created_at": row[4].strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": row[5].strftime("%Y-%m-%d %H:%M:%S"),
    }
    message = None
    return render_template('edit.html', todo=todo, message=message)


@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    try:
        connect_db = ConnectDB()
        conn_string = connect_db.get_connection_uri()
        conn = connect_db.get_connection_cls(conn_string)
        db_manager = DatabaseManager()
        message = db_manager.delete_record(conn, id=todo_id)["message"]
    except Exception as e:
        message = "Failed to delete Todo"

    return render_template('message.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
