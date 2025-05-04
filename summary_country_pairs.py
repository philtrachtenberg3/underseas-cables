import sqlite3
from collections import defaultdict, Counter
from itertools import combinations

def country_connections():
    conn = sqlite3.connect('cables.db')
    c = conn.cursor()

    # Get cable name and country
    c.execute('SELECT name, country FROM cables WHERE country != ""')
    rows = c.fetchall()

    # Build cable -> set of countries
    cable_countries = defaultdict(set)
    for name, country in rows:
        cable_countries[name].add(country)

    # Build country pairs and count
    pair_counter = Counter()
    for countries in cable_countries.values():
        for pair in combinations(sorted(countries), 2):
            pair_counter[pair] += 1

    # Show top 20 country-to-country connections
    print("🌍 Top Country-to-Country Connections by Shared Cables\n")
    for (country1, country2), count in pair_counter.most_common(20):
        print(f"{country1} <-> {country2}: {count} cables")

    conn.close()

if __name__ == "__main__":
    country_connections()
