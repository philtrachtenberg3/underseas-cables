import sqlite3

def view_cables():
    conn = sqlite3.connect('cables.db')
    c = conn.cursor()

    # Fetch first 10 entries
    c.execute('SELECT name, landing_point FROM cables ORDER BY name')
    rows = c.fetchall()

    for row in rows:
        print(f"Cable: {row[0]} | Landing Point: {row[1]}")

    conn.close()

if __name__ == "__main__":
    view_cables()
