# Cafe Finder

This is an original Flask + SQLite implementation.

## 1. Put the database here

Place the course-provided `cafes.db` in this folder:

    cafe_website/
    ├── cafes.db
    ├── main.py
    ├── requirements.txt
    ├── templates/
    └── static/

## 2. Install Flask

```bash
python3 -m pip install -r requirements.txt
```

## 3. Run

```bash
python3 main.py
```

Then open the local address shown in the terminal.

## Important database note

This implementation expects the standard Angela Yu cafe table named
`cafe`, with columns such as:

    id
    name
    map_url
    img_url
    location
    seats
    has_toilet
    has_wifi
    has_sockets
    coffee_price

If your supplied database uses different column names, inspect it with:

```bash
sqlite3 cafes.db
.schema
```

and adjust the SQL in `main.py`.
