from src.product import Product

class ElectronicsProduct(Product):
    """
    Bu class, bir 'Product' classından türetilmiş, elektronik ürün özelliklerini temsil eder.
    Elektronik ürünlerin garanti süresi gibi ek bilgilerini içerir.

    Attributes:
        id (int): Ürünün benzersiz kimliği. (Superclasstan inheritance alinir)
        name (str): Ürünün adi. (Superclasstan inheritance alinir)
        category (str): Ürünün kategorisi (Sabit olarak "Electronics" olarak ayarlanir). (Superclasstan inheritance alinir)
        stock (int): Ürünün mevcut stoğu. (Superclasstan inheritance alinir)
        price (float): Ürünün birim fiyati. (Superclasstan inheritance alinir)
        warranty_years (int): Elektronik ürünün garanti süresi (yil cinsinden).
    """

    def __init__(self, id: int, name: str, stock: int, price: float, warranty_years: int):
        super().__init__(id, name, "Electronics", stock, price)
        self.warranty_years = warranty_years

    def __repr__(self):
        """
        ElectronicsProduct nesnesinin geliştirici dostu bir temsilini döndürür.
        Bu temsil, hata ayiklama ve loglama için kullanişlidir.
        """
        return f"<ElectronicsProduct id={self.id} name='{self.name}' stock={self.stock} warranty={self.warranty_years} years>"

    def get_warranty_info(self):
        """
        Elektronik ürünün garanti bilgilerini içeren bir string döndürür.

        Returns:
            str: "[Garanti Süresi] yil garanti." formatinda garanti bilgisi.
        """
        return f"{self.warranty_years} yil garanti."