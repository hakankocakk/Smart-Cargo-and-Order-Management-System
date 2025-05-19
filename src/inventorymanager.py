import sqlite3
from src.product import Product


class ProductManager:
    def __init__(self, db_name="databases/store.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()


    def create_table(self):
        try:
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
        except Exception as e:
                print(f"Error: {e}")


    def is_in_stock(self, name):
        try:
            cursor = self.conn.execute("SELECT stock FROM Product WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result[0] > 0 if result else False
        except Exception as e:
                print(f"Error: {e}")


    def add_product(self, product: Product):
        try:
            cursor = self.conn.execute("Select stock FROM Product WHERE id = ?", (product.id,))
            result = cursor.fetchone()

            if  result:
                new_stock = result[0] + product.stock
                self.conn.execute("UPDATE Product SET stock = ? WHERE id = ?", (new_stock, product.id))
                self.conn.commit()
            else:
                query = "INSERT INTO Product (id, name, category, stock, price) VALUES (?, ?, ?, ?, ?)"
                self.conn.execute(query, (product.id, product.name, product.category, product.stock, product.price))
                self.conn.commit()
        except Exception as e:
                print(f"Error: {e}")


    def reduce_stock(self, name, quantity):
        try:
            cursor = self.conn.execute("SELECT stock FROM Product WHERE name = ?", (name,))
            result = cursor.fetchone()

            if result:
                current_stock = result[0]
                if current_stock >= quantity:
                    self.conn.execute("UPDATE Product SET stock = stock - ? WHERE name = ?", (quantity, name))
                    self.conn.commit()
                    return f"{quantity} item(s) have been removed from stock."
                else:
                    return "Insufficient stock."
            else:
                return "Product not found."
        except Exception as e:
                print(f"Error: {e}")


    def list_products(self):
        try:
            cursor = self.conn.execute("SELECT id, name, category, stock, price FROM Product")
            return [Product(id=row[0], name=row[1], category=row[2], stock=row[3], price=row[4]) for row in cursor]
        except Exception as e:
                print(f"Error: {e}")


    def filter_by_category(self, category: str):
        try:
            cursor = self.conn.execute("SELECT id, name, category, stock, price FROM Product WHERE category = ?", (category,))
            return [Product(id=row[0], name=row[1], category=row[2], stock=row[3], price=row[4]) for row in cursor]
        except Exception as e:
                print(f"Error: {e}")


    def update_stock(self, product_id: int, new_stock: int):
        try:
            self.conn.execute("UPDATE Product SET stock = ? WHERE id = ?", (new_stock, product_id))
            self.conn.commit()
        except Exception as e:
                print(f"Error: {e}")


    def get_stock(self, product_id: int):
        try:
            cursor = self.conn.execute("SELECT stock FROM Product WHERE id = ?", (product_id,))
            result = cursor.fetchone()
            return result[0] if result else "Product is out of stock"
        except Exception as e:
                print(f"Error: {e}")
