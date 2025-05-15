import sqlite3

class Product:
    def __init__(self, id: int, name: str, category: str, stock: int, price: float, ):
        self.id = id
        self.name = name
        self.category = category
        self.stock = stock
        self.price = price

    def __repr__(self):
        return f"<Product id={self.id} name='{self.name}' stock={self.stock}>"
