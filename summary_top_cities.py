import sqlite3

def top_cities_by_cables():
    conn = sqlite3.connect('cables.db')
    c = conn.cursor()

    c.execute('''
    SELECT city, country, COUNT(DISTINCT name) as cable_count
    FROM cables
    GROUP BY city, country
    ORDER BY cable_count DESC
    LIMIT 20
    ''')

    rows = c.fetchall()
    print("🏙️ Top 20 Cities by Number of Unique Cables\n")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row[0]}, {row[1]} — {row[2]} cables")

    conn.close()

if __name__ == "__main__":
    top_cities_by_cables()
