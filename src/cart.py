class Cart:
    """
    Alışveriş sepetini temsil eden sınıf.
    Kullanıcının seçtiği ürünleri ve bu ürünlerin miktarlarını yönetir.
    Sepete ürün ekleme, sepeti boşaltma, sepetin boş olup olmadığını kontrol etme
    ve sepetteki toplam ürün sayısını alma gibi işlevsellikler sunar.
    """
    def __init__(self):
        self.items = []  

    def add(self, product, quantity):
        """
        Belirtilen ürünü ve miktarını sepete ekler.
        Eğer ürün zaten sepetteyse, mevcut miktarını artırır.
        Ürün sepette yoksa, yeni bir öğe olarak ekler.

        Args:
            product (Product): Sepete eklenecek Product nesnesi.
            quantity (int): Eklenecek ürünün miktarı. Pozitif bir tam sayı olmalıdır.
        """
        for i, (p, q) in enumerate(self.items):
            if p.id == product.id:
                self.items[i] = (p, q + quantity)
                return
        self.items.append((product, quantity))

    def is_empty(self):
        """
        Sepetin boş olup olmadığını kontrol eder.

        Returns:
            bool: Sepet boşsa True, doluysa False.
        """
        return len(self.items) == 0

    def clear(self):
        """
        Sepetteki tüm ürünleri temizler ve sepeti boş hale getirir.
        """
        self.items = []

    def total_items(self):
        """
        Sepetteki tüm ürünlerin toplam miktarını döndürür.
        Farklı türdeki ürünlerin toplam adetini verir.

        Returns:
            int: Sepetteki toplam ürün adedi.
        """
        return sum(q for _, q in self.items)

    def get_products(self):
        """
        Sepetteki tüm ürün nesnelerini, miktarları kadar tekrar ederek içeren bir liste döndürür.
        Örneğin, sepette 2 adet 'A' ürünü varsa, döndürülen listede 'A' ürünü iki kez yer alır.

        Returns:
            list: Sepetteki tüm ürün nesnelerini içeren liste.
        """
        result = []
        for product, quantity in self.items:
            result.extend([product] * quantity)
        return result

    def __iter__(self):
        """
        Sepet nesnesinin üzerinde döngü (iterate) yapılabilmesini sağlar.
        Bu sayede `for item in cart:` gibi yapılarla sepetin içeriği (ürün, miktar çiftleri) gezilebilir.

        Returns:
            iterator: Sepetteki (ürün, miktar) çiftleri üzerinde bir yineleyici.
        """
        return iter(self.items)