from flask import Flask, render_template

app = Flask(__name__)

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


@app.route("/login")
def login():
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


@app.route("/profiles")
def profile():
    return render_template("profiles.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)