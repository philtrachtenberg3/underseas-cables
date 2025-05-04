from flask import Flask, render_template
import sqlite3
from collections import defaultdict, Counter
from itertools import combinations

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cables.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/top-countries")
def top_countries():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT country, COUNT(DISTINCT name) as cable_count
        FROM cables
        WHERE country != ""
        GROUP BY country
        ORDER BY cable_count DESC
        LIMIT 20
    ''')
    countries = c.fetchall()
    conn.close()
    return render_template("top_countries.html", countries=countries)

@app.route("/top-cities")
def top_cities():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT city, country, COUNT(DISTINCT name) as cable_count
        FROM cables
        WHERE city != ""
        GROUP BY city, country
        ORDER BY cable_count DESC
        LIMIT 20
    ''')
    cities = c.fetchall()
    conn.close()
    return render_template("top_cities.html", cities=cities)

@app.route("/country-pairs")
def country_pairs():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT name, country FROM cables WHERE country != ""')
    rows = c.fetchall()

    # Build cable -> set of countries
    cable_countries = defaultdict(set)
    for row in rows:
        cable_countries[row["name"]].add(row["country"])

    # Build pairs and count
    pair_counter = Counter()
    for countries in cable_countries.values():
        for pair in combinations(sorted(countries), 2):
            pair_counter[pair] += 1

    top_pairs = pair_counter.most_common(20)
    conn.close()

    return render_template("country_pairs.html", pairs=top_pairs)

if __name__ == "__main__":
    app.run(debug=True)
