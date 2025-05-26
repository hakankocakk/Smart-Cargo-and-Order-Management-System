from src.product import Product

class BookProduct(Product):
    """
    Bu class, bir 'Product' classindan türetilmiş, kitaba özel ürün özelliklerini temsil eder.
    Kitaplarin yazar ve yayinevi gibi ek bilgilerini içerir.

    Attributes:
        id (int): Ürünün benzersiz kimliği. (Superclasstan inheritance alinir)
        name (str): Ürünün adi. (Superclasstan inheritance alinir)
        category (str): Ürünün kategorisi (Sabit olarak "Books" olarak ayarlanır). (Superclasstan inheritance alinir)
        stock (int): Ürünün mevcut stoğu. (Superclasstan inheritance alinir)
        price (float): Ürünün birim fiyatı. (Superclasstan inheritance alinir)
        author (str): Kitabin yazari.
        publisher (str): Kitabin yayinevi.
    """
    def __init__(self, id: int, name: str, stock: int, price: float, author: str, publisher: str):
        super().__init__(id, name, "Books", stock, price)
        self.author = author
        self.publisher = publisher

    def __repr__(self):
        """
        BookProduct nesnesinin geliştirici dostu bir temsilini döndürür.
        Bu temsil, hata ayıklama ve loglama için kullanışlıdır.
        """
        return f"<BookProduct id={self.id} name='{self.name}' stock={self.stock} author='{self.author}'>"

    def get_book_details(self):
        """
        Kitabin yazar ve yayinevi bilgilerini içeren bir string döndürür.

        Returns:
            str: "Author: [Yazar Adi], Publisher: [Yayinevi Adi]" formatinda detaylar.
        """
        return f"Author: {self.author}, Publisher: {self.publisher}"