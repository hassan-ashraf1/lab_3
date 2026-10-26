import os
import re
from functools import wraps

import bcrypt
import pymysql
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET", "dev-only-change-this-secret")


def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database="registration",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        charset="utf8mb4",
    )


def get_library_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database="library",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        charset="utf8mb4",
    )


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def clean_text(value):
    return (value or "").strip()


def valid_email(email):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


def render_register(name="", email="", errors=None):
    return render_template("register.html", name=name, email=email, errors=errors or [])


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("todos"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_register()

    name = clean_text(request.form.get("name"))
    email = clean_text(request.form.get("email")).lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")
    errors = []

    if not name:
        errors.append("Name is required")
    if not email:
        errors.append("Email is required")
    elif not valid_email(email):
        # The handout does not specify an email-format message; keep the required message.
        errors.append("Email is required")
    if not password:
        errors.append("Password is required")
    if not confirm_password:
        errors.append("Confirm password is required")
    if password and confirm_password and password != confirm_password:
        errors.append("Passwords do not match")

    if errors:
        return render_register(name, email, errors), 400

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
                (email, name, password_hash),
            )
            user_id = cursor.lastrowid
    except pymysql.err.IntegrityError:
        return render_register(name, email, ["Email Already Exists"]), 409
    finally:
        connection.close()

    session.clear()
    session["user_id"] = user_id
    session["name"] = name
    return redirect(url_for("todos"))


@app.route("/login", methods=["GET", "POST"])
def login():
    errors = []
    email = ""
    if request.method == "POST":
        email = clean_text(request.form.get("email")).lower()
        password = request.form.get("password", "")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if errors:
            return render_template("login.html", email=email, errors=errors), 400

        connection = get_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, name, password_hash FROM users WHERE email = %s",
                    (email,),
                )
                user = cursor.fetchone()
        finally:
            connection.close()

        if (not user) or (not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8"))):
            return render_template("login.html", email=email, errors=["Invalid email or password"]), 401

        session.clear()
        session["user_id"] = user["user_id"]
        session["name"] = user["name"]
        return redirect(url_for("todos"))

    return render_template("login.html", email=email, errors=errors)


@app.route("/todos", methods=["GET"])
@login_required
def todos():
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC",
                (session["user_id"],),
            )
            items = cursor.fetchall()
    finally:
        connection.close()
    return render_template("todos.html", items=items)


@app.route("/todos/add", methods=["POST"])
@login_required
def add_todo():
    title = clean_text(request.form.get("title"))
    errors = []
    if not title:
        errors.append("Title is required")
    elif len(title) > 200:
        errors.append("Title is too long (200 characters at most)")
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("todos"))

    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO todos (user_id, title) VALUES (%s, %s)",
                (session["user_id"], title),
            )
    finally:
        connection.close()
    flash("Task added.", "success")
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
@login_required
def edit_todo(todo_id):
    title = clean_text(request.form.get("title"))
    if not title:
        flash("Title is required", "error")
    elif len(title) > 200:
        flash("Title is too long (200 characters at most)", "error")
    else:
        connection = get_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
                    (title, todo_id, session["user_id"]),
                )
                if cursor.rowcount:
                    flash("Task updated.", "success")
        finally:
            connection.close()
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
@login_required
def toggle_todo(todo_id):
    is_done = 1 if request.form.get("is_done") == "1" else 0
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s",
                (is_done, todo_id, session["user_id"]),
            )
    finally:
        connection.close()
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
@login_required
def delete_todo(todo_id):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM todos WHERE todo_id = %s AND user_id = %s",
                (todo_id, session["user_id"]),
            )
    finally:
        connection.close()
    flash("Task deleted.", "success")
    return redirect(url_for("todos"))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.errorhandler(500)
def server_error(_error):
    return render_template("error.html"), 500


@app.route("/library")
@login_required
def library():
    connection = get_library_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM BOOK")
            books = cursor.fetchall()

            cursor.execute("SELECT * FROM AUTHOR")
            authors = cursor.fetchall()
    finally:
        connection.close()

    return render_template(
        "library.html",
        books=books,
        authors=authors
    )


@app.route("/authors/add", methods=["POST"])
@login_required
def add_author():
    name = clean_text(request.form.get("name"))
    country = clean_text(request.form.get("country"))

    connection = get_library_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO AUTHOR (author_id, name, country) "
                "VALUES ((SELECT COALESCE(MAX(author_id), 0) + 1 FROM AUTHOR a), %s, %s)",
                (name, country),
            )
    finally:
        connection.close()

    return redirect(url_for("library"))


@app.route("/authors/<int:author_id>/edit", methods=["POST"])
@login_required
def edit_author(author_id):
    name = clean_text(request.form.get("name"))
    country = clean_text(request.form.get("country"))

    connection = get_library_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE AUTHOR SET name = %s, country = %s WHERE author_id = %s",
                (name, country, author_id),
            )
    finally:
        connection.close()

    return redirect(url_for("library"))


@app.route("/authors/<int:author_id>/delete", methods=["POST"])
@login_required
def delete_author(author_id):
    connection = get_library_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM AUTHOR WHERE author_id = %s",
                (author_id,)
            )
    finally:
        connection.close()

    return redirect(url_for("library"))


@app.route("/books/add", methods=["POST"])
@login_required
def add_book():
    title = clean_text(request.form.get("title"))
    price = request.form.get("price")
    author_id = request.form.get("author_id")

    connection = get_library_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO BOOK (book_id, title, price, author_id) "
                "VALUES ((SELECT COALESCE(MAX(book_id), 0) + 1 FROM BOOK b), %s, %s, %s)",
                (title, price, author_id),
            )
    finally:
        connection.close()

    return redirect(url_for("library"))


@app.route("/books/<int:book_id>/edit", methods=["POST"])
@login_required
def edit_book(book_id):
    title = clean_text(request.form.get("title"))
    price = request.form.get("price")
    author_id = request.form.get("author_id")

    connection = get_library_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE BOOK SET title = %s, price = %s, author_id = %s WHERE book_id = %s",
                (title, price, author_id, book_id),
            )
    finally:
        connection.close()

    return redirect(url_for("library"))


@app.route("/books/<int:book_id>/delete", methods=["POST"])
@login_required
def delete_book(book_id):
    connection = get_library_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM BOOK WHERE book_id = %s",
                (book_id,)
            )
    finally:
        connection.close()

    return redirect(url_for("library"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
