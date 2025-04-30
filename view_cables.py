import sqlite3

def view_cables():
    conn = sqlite3.connect('cables.db')
    c = conn.cursor()


    # Fetch entries
    c.execute('SELECT name, city, state, country FROM cables ORDER BY name')
    rows = c.fetchall()

    for row in rows:
        print(f"Cable: {row[0]} | City: {row[1]} | State (US-only): {row[2]} | Country: {row[3]}")

    # check count of records in table
    c.execute('SELECT COUNT(*) FROM cables')
    total = c.fetchone()[0]
    print(f"\n📦 Total records in 'cables' table: {total}\n")

    conn.close()

if __name__ == "__main__":
    view_cables()
