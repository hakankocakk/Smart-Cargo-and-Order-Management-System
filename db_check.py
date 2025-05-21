import sqlite3

def print_orders_db(db_path="databases/orders.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    print("Orders in orders.db:\n")
    print("\t".join(columns))
    for row in rows:
        print("\t".join(str(item) for item in row))

    conn.close()

if __name__ == "__main__":
    print_orders_db()