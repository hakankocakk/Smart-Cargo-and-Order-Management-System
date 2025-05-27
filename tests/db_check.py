import sqlite3

def print_orders_db(db_path="databases/orders.db"):

    """
    Belirtilen SQLite veritabanı yolundaki 'istenen' tablosnun tüm içeriğini okur
    ve sütun başlıklarıyla birlikte konsola yazdırır.
    Bu fonksiyon, veritabanı içeriğini hızlıca görüntülemek ve doğruluk kontrolü yapmak
    için kullanışlıdır.

    Args:
        db_path (str): 'orders.db' veritabanı dosyasının yolu.
                       Varsayılan olarak "databases/orders.db" olarak ayarlanmıştır.
    """
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