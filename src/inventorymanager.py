import sqlite3
from src.product import Product

class ProductManager:
    def __init__(self, db_name="store.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            stock INTEGER NOT NULL,
            price REAL NOT NULL
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_product(self, product: Product):
        query = "INSERT INTO Product (name, category, stock, price) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (product.name, product.category, product.stock, product.price))
        self.conn.commit()

    def list_products(self):
        cursor = self.conn.execute("SELECT id, name, category, stock, price FROM Product")
        return [Product(id=row[0], name=row[1], category=row[2], stock=row[3], price=row[4]) for row in cursor]

    def filter_by_category(self, category: str):
        cursor = self.conn.execute("SELECT id, name, category, stock, price FROM Product WHERE category = ?", (category,))
        return [Product(id=row[0], name=row[1], category=row[2], stock=row[3], price=row[4]) for row in cursor]

    def update_stock(self, product_id: int, new_stock: int):
        self.conn.execute("UPDATE Product SET stock = ? WHERE id = ?", (new_stock, product_id))
        self.conn.commit()

    def get_stock(self, product_id: int):
        cursor = self.conn.execute("SELECT stock FROM Product WHERE id = ?", (product_id,))
        result = cursor.fetchone()
        return result[0] if result else None
