import sqlite3
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

admin_password = os.environ["ADMIN_PASSWORD"]
generate_password_hash(admin_password)

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
        generate_password_hash(admin_password),
        "admin"
    ),
    (
        "Melita",
        "melita@rakshitha.com",
        generate_password_hash(os.environ["MELITA_PASSWORD"]),
        "customer"
    ),
    (
        "Asha",
        "asha@adrielle.com",
        generate_password_hash(os.environ["ASHA_PASSWORD"]),
        "customer"
    ),
    (
        "Gigi",
        "gigi@ain.com",
        generate_password_hash(os.environ["GIGI_PASSWORD"]),
        "customer"
    )
]

connection.execute("""
CREATE TABLE IF NOT EXISTS muffins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL,
    image TEXT NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    is_new INTEGER NOT NULL DEFAULT 0
)
""")

muffins = [
    (
        "Banana Ice Cream Muffin",
        "Warm banana muffin paired with creamy banana ice cream and caramel sauce.",
        5.50,
        "Signature Dessert",
        "banana_ice_cream_muffin.png",
        20,
        1
    ),
    (
        "Classic Banana Muffin",
        "Simple, moist, golden banana muffin baked with ripe bananas.",
        3.50,
        "Classic",
        "classic_banana_muffin.png",
        40,
        0
    ),
    (
        "Choco-Chip Banana Muffin",
        "Banana muffin packed with rich chocolate chips.",
        4.25,
        "Chocolate",
        "choco_chip_muffin.png",
        30,
        0
    ),
    (
        "Walnut Banana Muffin",
        "Banana muffin topped with toasted walnut pieces.",
        4.50,
        "Nuts",
        "walnut_banana_muffin.png",
        25,
        0
    ),
    (
        "Caramel Banana Muffin",
        "Banana muffin finished with rich caramel drizzle.",
        4.75,
        "Sweet",
        "caramel_banana_muffin.png",
        25,
        0
    ),
    (
        "Cinnamon Banana Muffin",
        "Banana muffin topped with buttery cinnamon brown sugar crumble.",
        4.25,
        "Classic",
        "cinnamon_muffin.png",
        30,
        0
    ),
    (
        "Chocolate Banana Muffin",
        "Rich chocolate banana muffin with cocoa and sweet banana.",
        4.50,
        "Chocolate",
        "chocolate_banana_muffin.png",
        30,
        0
    )
]

count = connection.execute(
    "SELECT COUNT(*) FROM muffins"
).fetchone()[0]

if count == 0:
    connection.executemany("""
        INSERT INTO muffins
        (name, description, price, category, image, stock, is_new)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, muffins)

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
