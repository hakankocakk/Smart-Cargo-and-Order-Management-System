import sqlite3
from src.product import Product
from src.product_factory import ProductFactory
from src.electronics_product import ElectronicsProduct
from src.book_product import BookProduct 


#Singleton Desing Pattern
class ProductManager:
    """
    Bu class, store veritabani işlemlerini yönetmek için Singleton tasarim desenini uygular.
    Bu sayede ProductManager classinin yalnizca bir örneği oluşturulabilir ve
    uygulama genelinde ayni veritabani bağlantisi kullanilabilir.

    Veritabani etkileşimlerini (ürün ekleme, stok güncelleme, ürün listeleme vb.)
    merkezi bir yerden yönetir.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton desenini uygulayan özel metod.
        Classin yalnizca bir örneğinin oluşturulmasini sağlar.
        """
        if not cls._instance:
            cls._instance = super(ProductManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name="databases/store.db"):
        """
        ProductManager classinin başlatici metodu.
        Veritabani bağlantisini kurar ve ürün tablosunu oluşturur.
        Yalnizca bir kez başlatildiğindan emin olmak için 'hasattr' kullanilir.

        Args:
            db_name (str): Bağlanılacak SQLite veritabani dosyasinin yolu.
        """
        if not hasattr(self, 'conn'):
            self.conn = sqlite3.connect(db_name)
            self.create_table()
            self.product_factory = ProductFactory()


    def create_table(self):
        """
        'Product' tablosunu veritabaninda oluşturur.
        Eğer tablo zaten varsa, yeniden oluşturmaz (IF NOT EXISTS).
        Tüm ürün tiplerinin özelliklerini tek bir tabloda tutar.
        """
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
        """
        Belirtilen ada sahip bir ürünün stokta olup olmadiğini kontrol eder.

        Args:
            name (str): Kontrol edilecek ürünün adi.

        Returns:
            bool: Ürün stokta ise True, değilse False.
        """
        try:
            cursor = self.conn.execute("SELECT stock FROM Product WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result[0] > 0 if result else False
        except Exception as e:
                print(f"Error: {e}")


    def add_product(self, product: Product):
        """
        Yeni bir ürün ekler veya mevcut bir ürünün stoğunu günceller.
        Eğer ürün zaten varsa, stoğunu artirir; yoksa yeni ürün olarak ekler.

        Args:
            product (Product): Eklenecek veya stoğu güncellenecek ürün nesnesi.
                               (Product, ElectronicsProduct veya BookProduct olabilir)
        """
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
        """
        Belirtilen ada sahip ürünün stoğunu azaltir.

        Args:
            name (str): Stoğu azaltilacak ürünün adi.
            quantity (int): Stoktan düşülecek miktar.

        Returns:
            str: İşlemin sonucunu belirten bir mesaj.
        """
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
        Yardimci metot: Veritabanindan çekilen bir satiri uygun Product nesnesine dönüştürür.
        Bu metod, Factory desenini kullanarak doğru ürün classi örneğini oluşturur.

        Args:
            row (tuple): Veritabani sorgusundan dönen tek bir ürün satiri.

        Returns:
            Product: Oluşturulan Product, ElectronicsProduct veya BookProduct nesnesi.
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
        """
        Veritabanindaki tüm ürünleri listeler.
        Her veritabani satirini uygun Product nesnesine dönüştürür.

        Returns:
            list[Product]: Tüm ürün nesnelerinin bir listesi. Hata durumunda boş liste döner.
        """
        try:
            cursor = self.conn.execute("SELECT id, name, category, stock, price, warranty_years, author, publisher FROM Product")
            return [self._create_product_from_row(row) for row in cursor]
        except Exception as e:
                print(f"Error: {e}")


    def filter_by_category(self, category: str):
        """
        Belirli bir kategoriye ait ürünleri filtreler ve listeler.

        Args:
            category (str): Filtrelenecek ürün kategorisi.

        Returns:
            list[Product]: Belirtilen kategoriye ait ürün nesnelerinin bir listesi. Hata durumunda boş liste döner.
        """
        try:
            cursor = self.conn.execute("SELECT id, name, category, stock, price, warranty_years, author, publisher FROM Product WHERE category = ?", (category,))
            return [self._create_product_from_row(row) for row in cursor]
        except Exception as e:
                print(f"Error: {e}")


    def update_stock(self, product_id: int, new_stock: int):
        """
        Belirtilen ürünün stoğunu günceller.

        Args:
            product_id (int): Stoğu güncellenecek ürünün ID'si.
            new_stock (int): Ürünün yeni stok miktarı.
        """
        try:
            self.conn.execute("UPDATE Product SET stock = ? WHERE id = ?", (new_stock, product_id))
            self.conn.commit()
        except Exception as e:
                print(f"Error: {e}")


    def get_stock(self, product_id: int):
        """
        Belirtilen ürünün mevcut stok miktarini döndürür.

        Args:
            product_id (int): Stoğu sorgulanacak ürünün ID'si.

        Returns:
            int or str: Ürünün stok miktari (int) veya ürün bulunamazsa/stokta yoksa bir mesaj (str).
        """
        try:
            cursor = self.conn.execute("SELECT stock FROM Product WHERE id = ?", (product_id,))
            result = cursor.fetchone()
            return result[0] if result else "Product is out of stock"
        except Exception as e:
                print(f"Error: {e}")
