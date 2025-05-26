import sqlite3


#Singleton Desing Pattern
class OrderManagement:
    """
    'OrderManager' sınıfı, tüm sistemde yalnızca bir örneğinin (instance) olmasını sağlayan
    bir **Singleton Tasarım Deseni** uygular. Bu sınıf, siparişleri SQLite veritabanı üzerinden
    yönetmek için kullanılır: siparişleri listeleme, duruma göre filtreleme ve sipariş durumunu güncelleme
    gibi işlevler sağlar. Veritabanı bağlantısını tek bir noktadan yöneterek tutarlılığı garanti eder.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Sınıfın yeni bir örneği oluşturulmadan önce çağrılan özel metod.
        Eğer sınıfın bir örneği (_instance) daha önce oluşturulmamışsa, yeni bir örnek oluşturur
        ve onu _instance'a atar. Böylece OrderManager'ın her zaman tek bir örneği olur.
        """
        if not cls._instance:
            cls._instance = super(OrderManagement, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name="databases/orders.db"):
        """
        OrderManager nesnesini başlatır ve SQLite veritabanı bağlantısını kurar.
        Singleton yapısı nedeniyle, 'conn' niteliği sadece ilk örnek oluşturulduğunda başlatılır.

        Args:
            db_name (str): Veritabanı dosyasının adı. Varsayılan olarak "databases/orders.db" olarak ayarlanmıştır.
        """
        if not hasattr(self, 'conn'):
            self.conn = sqlite3.connect(db_name)

    def show_orders(self):
        """
        Veritabanındaki tüm siparişleri çeker ve konsola okunaklı bir formatta yazdırır.
        Her siparişin ID'sini, ürünlerini, durumunu, nakliye yöntemini ve toplam maliyetini gösterir.
        """
        try:
            cursor = self.conn.execute("SELECT id, products, status, shipping_method, total FROM orders")
            orders = cursor.fetchall()
            for i, (oid, products, status, shipping, total) in enumerate(orders, 1):
                print(f"{i}. Order ID: {oid} | Products: {products} | Status: {status} | Shipping: {shipping} | Total: {total}")
        except Exception as e:
                print(f"Error: {e}")

    def filter_by_order_status(self, status):
        """
        Belirtilen sipariş durumuna ('status') göre siparişleri filtreler ve konsola yazdırır.
        Yalnızca eşleşen duruma sahip siparişleri gösterir.

        Args:
            status (str): Filtrelemek istenen sipariş durumu (örn. "Preparing", "Shipped", "Delivered").
                          Bu, 'OrderStatus' Enum'undaki değerlerden biriyle eşleşmelidir.
        """
        try:
            cursor = self.conn.execute("Select id, products, status, shipping_method, total FROM orders WHERE status = ?", (status,))
            orders = cursor.fetchall()
            for i, (oid, products, status, shipping, total) in enumerate(orders, 1):
                print(f"{i}. Order ID: {oid} | Products: {products} | Status: {status} | Shipping: {shipping} | Total: {total}")
        except Exception as e:
                print(f"Error: {e}")

    def update_by_order_status(self, order_id, status):
        """
        Belirtilen sipariş kimliğine ('order_id') sahip bir siparişin durumunu günceller.

        Args:
            order_id (int): Durumu güncellenecek siparişin kimliği.
            status (str): Siparişin ayarlanacağı yeni durum (örn. "Preparing", "Shipped", "Delivered").
        """

        try:
            self.conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
            self.conn.commit()
        except Exception as e:
                print(f"Error: {e}")
         
    
    