from src.product import Product
from src.electronics_product import ElectronicsProduct
from src.book_product import BookProduct


class ProductFactory:
    """
    Bu class, bir product nesnesini tipine göre dinamik olarak oluşturan bir Fabrika (Factory) olarak görev yapar.
    Bu tasarim deseni, nesne oluşturma mantiğini merkezi bir yere taşiyarak kodun daha düzenli, esnek ve genişletilebilir olmasini sağlar.

    Yeni ürün tipleri eklendiğinde, sadece 'create_product' metodunun güncellenmesi yeterlidir,
    bu da istemci kodunun (ürünleri oluşturan kodun) değişmesini engeller.
    """
    def create_product(self, product_type: str, id: int, name: str, stock: int, price: float, **kwargs) -> Product:
        """
        Factory Method: Belirtilen türe göre uygun ürün nesnesini oluşturur.

        Args:
            product_type (str): Oluşturulacak ürünün tipi (örn: "electronics", "book", "food").
            id (int): Ürünün benzersiz kimliği.
            name (str): Ürünün adi.
            stock (int): Ürünün mevcut stok adedi.
            price (float): Ürünün birim fiyati.
            **kwargs: Ürün tipine özgü ek argümanlar.
                      - "electronics" için: 'warranty_years' (int, varsayilan 1)
                      - "book" için: 'author' (str, varsayilan "None"), 'publisher' (str, varsayilan "None")

        Returns:
            Product: Oluşturulan ürün nesnesi (Product, ElectronicsProduct veya BookProduct türünde olabilir).
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