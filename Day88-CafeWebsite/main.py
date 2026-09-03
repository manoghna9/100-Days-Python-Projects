"""
Original cafe directory website.

This project uses:
    Flask      -> web server and routes
    SQLite     -> cafe database
    Jinja      -> HTML templates
    WTForms    -> form handling/validation

It supports:
    GET  /              -> show all cafes
    GET  /search        -> filter cafes by location
    GET  /add          -> show add-cafe form
    POST /add          -> insert a new cafe
    GET  /delete/<id>   -> delete a cafe
"""

from pathlib import Path
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for


app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"

DATABASE = Path(__file__).with_name("cafes.db")


def get_connection():
    """Open a database connection and return rows as dictionaries."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def fetch_cafes(location=None):
    """
    Get cafes from SQLite.

    If a location is supplied, only matching cafes are returned.
    Using SQL parameters here prevents the search text from being
    directly inserted into the SQL statement.
    """
    connection = get_connection()

    if location:
        rows = connection.execute(
            """
            SELECT *
            FROM cafe
            WHERE location LIKE ?
            ORDER BY name
            """,
            (f"%{location}%",),
        ).fetchall()
    else:
        rows = connection.execute(
            """
            SELECT *
            FROM cafe
            ORDER BY name
            """
        ).fetchall()

    connection.close()
    return rows


@app.route("/")
def home():
    cafes = fetch_cafes()
    return render_template("index.html", cafes=cafes, search_term="")


@app.route("/search")
def search():
    location = request.args.get("location", "").strip()

    if not location:
        return redirect(url_for("home"))

    cafes = fetch_cafes(location)
    return render_template(
        "index.html",
        cafes=cafes,
        search_term=location,
    )


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        data = {
            "name": request.form.get("name", "").strip(),
            "map_url": request.form.get("map_url", "").strip(),
            "img_url": request.form.get("img_url", "").strip(),
            "location": request.form.get("location", "").strip(),
            "seats": request.form.get("seats", "").strip(),
            "has_toilet": request.form.get("has_toilet", "").strip(),
            "has_wifi": request.form.get("has_wifi", "").strip(),
            "has_sockets": request.form.get("has_sockets", "").strip(),
            "coffee_price": request.form.get("coffee_price", "").strip(),
        }

        # Basic validation keeps obviously incomplete rows out.
        required_fields = [
            "name",
            "map_url",
            "img_url",
            "location",
        ]

        if any(not data[field] for field in required_fields):
            flash("Please fill in all required fields.")
            return render_template("add.html", form=data)

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO cafe
            (name, map_url, img_url, location, seats,
             has_toilet, has_wifi, has_sockets, coffee_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["map_url"],
                data["img_url"],
                data["location"],
                data["seats"],
                data["has_toilet"],
                data["has_wifi"],
                data["has_sockets"],
                data["coffee_price"],
            ),
        )

        connection.commit()
        connection.close()

        flash(f"{data['name']} was added successfully!")
        return redirect(url_for("home"))

    return render_template("add.html", form={})


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM cafe WHERE id = ?",
        (cafe_id,),
    )

    connection.commit()
    connection.close()

    flash("Cafe deleted.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
