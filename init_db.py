import sqlite3
from werkzeug.security import generate_password_hash

connection=sqlite3.connect("muffin_stop.db")
cursor=connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

users = [
    (
        "Alinoor",
        "Alinoor@muffinstop.local",
        generate_password_hash("The_B0s$_muff1n"),
        "admin"
    ),
    (
        "Melita",
        "melita@rakshitha.com",
        generate_password_hash("banana123"),
        "customer"
    ),
    (
        "Asha",
        "asha@adrielle.com",
        generate_password_hash("muffin123"),
        "customer"
    ),
    (
        "Gigi",
        "gigi@ain.com",
        generate_password_hash("yummy123"),
        "customer"
    )
]

for user in users:
    try:
        cursor.execute("""
        INSERT INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
        """, user)
    except sqlite3.IntegrityError:
        pass

connection.commit()
connection.close()

print("Database created successfully.")
