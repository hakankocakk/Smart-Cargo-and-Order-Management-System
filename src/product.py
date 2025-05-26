import sqlite3

class Product:
    """
    Genel bir ürünün temel özelliklerini temsil eder.
    Diğer ürün türleri (örn. Kitaplar) bu classtan türetilebilir.

    Attributes:
        id (int): Ürünün benzersiz kimliği.
        name (str): Ürünün adi.
        category (str): Ürünün ait olduğu kategori (örn. "Elektronik", "Gida", "Kitaplar").
        stock (int): Ürünün mevcut stok adedi.
        price (float): Ürünün birim fiyati.
    """
    def __init__(self, id: int, name: str, category: str, stock: int, price: float, ):
        self.id = id
        self.name = name
        self.category = category
        self.stock = stock
        self.price = price

    def __repr__(self):
        """
        Product nesnesinin geliştirici dostu bir temsilini döndürür.
        Bu temsil, hata ayiklama ve loglama için kullanişlidir.
        """
        return f"<Product id={self.id} name='{self.name}' stock={self.stock}>"
    
