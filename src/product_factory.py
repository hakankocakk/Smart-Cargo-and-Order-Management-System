from src.product import Product
from src.electronics_product import ElectronicsProduct
from src.book_product import BookProduct


class ProductFactory:
    def create_product(self, product_type: str, id: int, name: str, stock: int, price: float, **kwargs) -> Product:
        """
        Factory Method: Belirtilen türe göre uygun ürün nesnesini oluşturur.
        """
        if product_type.lower() == "electronics":
            warranty_years = kwargs.get("warranty_years", 1)
            return ElectronicsProduct(id, name, stock, price, warranty_years)
        elif product_type.lower() == "book":
            author = kwargs.get("author", "None")
            publisher = kwargs.get("publisher", "None")
            return BookProduct(id, name, stock, price, author, publisher)
        else:
            return Product(id, name, product_type, stock, price)