import sqlite3
from src.product import Product
from src.product_factory import ProductFactory
from src.electronics_product import ElectronicsProduct
from src.book_product import BookProduct 


#Singleton Desing Pattern
class ProductManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProductManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name="databases/store.db"):
        if not hasattr(self, 'conn'):
            self.conn = sqlite3.connect(db_name)
            self.create_table()
            self.product_factory = ProductFactory()


    def create_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS Product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                stock INTEGER NOT NULL,
                price REAL NOT NULL,
                warranty_years INTEGER,
                author TEXT,              
                publisher TEXT            
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
                query = "INSERT INTO Product (id, name, category, stock, price, warranty_years, author, publisher) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

                warranty_years = None
                author = None
                publisher = None

                if isinstance(product, ElectronicsProduct):
                    warranty_years = product.warranty_years
                    product.category = "Electronics"
                elif isinstance(product, BookProduct):
                    author = product.author
                    publisher = product.publisher
                    product.category = "Books"
                self.conn.execute(query, (product.id, product.name, product.category, product.stock, product.price, warranty_years, author, publisher))
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

    
    def _create_product_from_row(self, row) -> Product:
        """
        Yardımcı metot: Veritabanından çekilen bir satırı uygun Product nesnesine dönüştürür.
        """
        product_id, name, category, stock, price, warranty_years, author, publisher = row

        if category.lower() == "electronics":
            return self.product_factory.create_product(
                "electronics", id=product_id, name=name, stock=stock, price=price, warranty_years=warranty_years
            )
        elif category.lower() == "books":
            return self.product_factory.create_product(
                "book", id=product_id, name=name, stock=stock, price=price, author=author, publisher=publisher
            )
        else:
            return self.product_factory.create_product(
                "standard", id=product_id, name=name, category=category, stock=stock, price=price
            )


    def list_products(self):
        try:
            cursor = self.conn.execute("SELECT id, name, category, stock, price, warranty_years, author, publisher FROM Product")
            return [self._create_product_from_row(row) for row in cursor]
        except Exception as e:
                print(f"Error: {e}")


    def filter_by_category(self, category: str):
        try:
            cursor = self.conn.execute("SELECT id, name, category, stock, price, warranty_years, author, publisher FROM Product WHERE category = ?", (category,))
            return [self._create_product_from_row(row) for row in cursor]
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
