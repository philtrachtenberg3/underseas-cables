import sqlite3

def top_countries_by_cables():
    conn = sqlite3.connect('cables.db')
    c = conn.cursor()

    c.execute('''
    SELECT country, COUNT(DISTINCT name) as cable_count
    FROM cables
    GROUP BY country
    ORDER BY cable_count DESC
    LIMIT 20
    ''')

    rows = c.fetchall()
    print("🌍 Top 20 Countries by Number of Unique Cables\n")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row[0]} — {row[1]} cables")

    conn.close()

if __name__ == "__main__":
    top_countries_by_cables()
