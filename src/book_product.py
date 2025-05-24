from src.product import Product

class BookProduct(Product):
    def __init__(self, id: int, name: str, stock: int, price: float, author: str, publisher: str):
        super().__init__(id, name, "Books", stock, price)
        self.author = author
        self.publisher = publisher

    def __repr__(self):
        return f"<BookProduct id={self.id} name='{self.name}' stock={self.stock} author='{self.author}'>"

    def get_book_details(self):
        return f"Author: {self.author}, Publisher: {self.publisher}"