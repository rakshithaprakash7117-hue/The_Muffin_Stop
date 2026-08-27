from flask import Flask, render_template,request,redirect,url_for,session
import sqlite3
from werkzeug.security import check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-secret")

def get_db_connection():
    connection = sqlite3.connect("muffin_stop.db")
    connection.row_factory = sqlite3.Row
    return connection

#muffin ids
muffins_data = {
    1: {
        "name": "Banana Ice Cream Muffin",
        "price": 5.50,
        "description": "Warm banana muffin paired with creamy banana ice cream and caramel sauce.",
        "image": "banana_ice_cream_muffin.png"
    },
    2: {
        "name": "Classic Banana Muffin",
        "price": 3.50,
        "description": "Simple, moist, golden banana muffin baked with ripe bananas.",
        "image": "classic_banana_muffin.png"
    },
    3: {
        "name": "Choco-Chip Banana Muffin",
        "price": 4.25,
        "description": "Banana muffin packed with rich chocolate chips.",
        "image": "choco_chip_muffin.png"
    },
    4: {
        "name": "Walnut Banana Muffin",
        "price": 4.50,
        "description": "Banana muffin topped with toasted walnut pieces.",
        "image": "walnut_banana_muffin.png"
    },
    5: {
        "name": "Caramel Banana Muffin",
        "price": 4.75,
        "description": "Banana muffin finished with a rich caramel drizzle.",
        "image": "caramel_banana_muffin.png"
    },
    6: {
        "name": "Cinnamon Banana Muffin",
        "price": 4.25,
        "description": "Banana muffin topped with buttery cinnamon brown sugar crumble.",
        "image": "cinnamon_muffin.png"
    },
    7: {
        "name": "Chocolate Banana Muffin",
        "price": 4.50,
        "description": "Rich chocolate banana muffin with cocoa and sweet banana.",
        "image": "chocolate_banana_muffin.png"
    }
}

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
    return render_template("muffins.html")


@app.route("/muffin/<int:muffin_id>")
def muffin(muffin_id):
    muffin = muffins_data.get(muffin_id)

    if muffin is None:
        return "Muffin not found", 404

    return render_template("muffin.html", muffin=muffin)


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

    user_count = connection.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    connection.close()

    return render_template(
        "admin.html",
        users=users,
        user_count=user_count
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)