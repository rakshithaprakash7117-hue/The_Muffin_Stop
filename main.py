from flask import Flask, render_template,request,redirect,url_for,session
import sqlite3
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

def get_db_connection():
    connection = sqlite3.connect("muffin_stop.db")
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username, username)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password_hash"], password):

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin"))

            return redirect(url_for("profile"))

        return "Invalid username or password"

    return render_template("login.html")


@app.route("/muffins")
def muffins():
    connection = get_db_connection()

    muffins = connection.execute(
        "SELECT * FROM muffins"
    ).fetchall()

    connection.close()

    return render_template(
        "muffins.html",
        muffins=muffins
    )


@app.route("/muffin/<int:muffin_id>")
def muffin(muffin_id):
    connection = get_db_connection()

    muffin = connection.execute(
        "SELECT * FROM muffins WHERE id = ?",
        (muffin_id,)
    ).fetchone()

    connection.close()

    if muffin is None:
        return "Muffin not found", 404

    return render_template(
        "muffin.html",
        muffin=muffin
    )

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    connection.close()

    return render_template("profiles.html", user=user)


@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Access denied", 403

    connection = get_db_connection()

    users = connection.execute(
        "SELECT id, username, email, role FROM users"
    ).fetchall()

    muffins = connection.execute(
        "SELECT * FROM muffins"
    ).fetchall()

    user_count = connection.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    muffin_count = connection.execute(
        "SELECT COUNT(*) FROM muffins"
    ).fetchone()[0]

    connection.close()

    return render_template(
        "admin.html",
        users=users,
        muffins=muffins,
        user_count=user_count,
        muffin_count=muffin_count
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)