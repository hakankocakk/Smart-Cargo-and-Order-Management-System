import sqlite3
from typing import List
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.order import Order
from src.customer import Customer
from src.product import Product
from src.order_status import OrderStatus
from src.shipping_method import ShippingMethod
from src.order_decorator import logOrderCreation
from src.notification_service import NotificationService

class OrderFactory:
    """
    'OrderFactory' sınıfı, sipariş nesneleri oluşturmaktan ve bu siparişleri bir veritabanında yönetmekten sorumludur.
    Bu sınıf, bir fabrika deseni (Factory Pattern) uygulayarak sipariş oluşturma sürecini soyutlar ve
    veritabanı etkileşimlerini kapsüller. Siparişlerin oluşturulması, kaydedilmesi, takip numarası atanması
    ve müşteri sipariş geçmişi ile ürün stok güncellemeleri gibi işlemleri yönetir.
    """
    def __init__(self, db_path: str = "databases/orders.db"):
        """
        OrderFactory nesnesini başlatır ve SQLite veritabanı bağlantısını kurar.
        Gerekirse 'orders' tablosunu oluşturur.

        Args:
            db_path (str): Veritabanı dosyasının yolu. Varsayılan olarak "databases/orders.db" olarak ayarlanmıştır.
        """
        self.conn = sqlite3.connect(db_path)
        self.create_orders_table()

    def create_orders_table(self):
        """
        Veritabanında 'orders' tablosunu oluşturur eğer zaten yoksa.
        Bu tablo, siparişlerin temel bilgilerini depolamak için kullanılır.
        Sipariş ID'si, müşteri adı ve adresi, ürünler (metin olarak), not,
        durum, kargo metodu, toplam tutar ve takip numarası gibi alanları içerir.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_name TEXT,
                customer_address TEXT,
                products TEXT,
                note TEXT,
                status TEXT,
                shipping_method TEXT,
                total REAL,
                tracking_number INT
            )
        ''')
        self.conn.commit()
    
    def get_next_order_id(self):
        """
        Veritabanındaki son sipariş kimliğini (ID) sorgulayarak bir sonraki uygun sipariş kimliğini döndürür.
        Bu, sipariş kimliklerinin benzersiz olmasını sağlar.

        Returns:
            int: Bir sonraki kullanılabilir sipariş kimliği. Eğer hiç sipariş yoksa 1 döndürür.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT MAX(id) FROM orders')
        result = cursor.fetchone()
        return (result[0] + 1) if result[0] is not None else 1


    def create_tracking_number(self, order_id):
        """
        Belirtilen sipariş ID'si için benzersiz bir kargo takip numarası oluşturur
        ve bu numarayi veritabanindaki ilgili sipariş kaydina günceller.
        Takip numarasi, sipariş ID'si ve rastgele bir sayi kombinasyonundan oluşur.

        Args:
            order_id (int): Takip numarasi oluşturulacak siparişin kimliği.
        """
        try:
            # Sipariş ID'si ve 5 haneli rastgele bir sayıyı birleştirerek takip numarası oluştur
            tracking_number = int(str(order_id) + str(random.randint(10000, 99999)))
            self.conn.execute("UPDATE orders SET tracking_number  = ? WHERE id = ?", (tracking_number, order_id))
            self.conn.commit()
        except Exception as e:
                print(f"Error: {e}")

    def get_tracking_number(self, order_id):
        """
        Belirtilen sipariş ID'sine ait kargo takip numarasını veritabanından getirir.

        Args:
            order_id (int): Takip numarasi sorgulanacak siparişin kimliği.

        Returns:
            int | None: Siparişin takip numarasi (int) veya bulunamazsa None.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT tracking_number FROM orders WHERE id = ?', (order_id,))
        return cursor.fetchone()[0]

    
    def save_order_to_db(self, order: Order):
        """
        Verilen Order nesnesini veritabanına kaydeder.
        Siparişin ID'si, müşteri bilgileri, ürünleri, notu, durumu, nakliye yöntemi ve toplam maliyeti gibi
        detayları 'orders' tablosuna ekler.

        Args:
            order (Order): Veritabanına kaydedilecek olan Order nesnesi.
        """
        cursor = self.conn.cursor()
        product_names = ', '.join([p.name for p in order._Order__products])  
        shipping_method_name = type(order._Order__shipping_method).__name__
        cursor.execute('''
           INSERT INTO orders (id, customer_name, customer_address, products, note, status, shipping_method, total)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order.id,
            order.customer.name,
            order.customer.get_address(),  
            product_names,
            order.note,
            order.status.value,
            shipping_method_name,
            order.total
       ))
        self.conn.commit() 
    @logOrderCreation
    def create_order(self, order_id: int, customer: Customer, products: List[Product],
                     status: OrderStatus, shipping_method: ShippingMethod,  notification_type: NotificationService,
                     note: str) -> Order:
        """
        Yeni bir sipariş nesnesi oluşturur, veritabanına kaydeder, müşteri sipariş geçmişine ekler
        ve sipariş edilen ürünlerin stoğunu günceller.
        Bu metod, 'logOrderCreation' dekoratörü ile sarmalanmıştır; bu da sipariş oluşturma sürecinin
        başlangıcını ve bitişini otomatik olarak loglamasını sağlar.

        Args:
            order_id (int): Oluşturulacak siparişin benzersiz kimliği.
            customer (Customer): Siparişi veren müşteri nesnesi.
            products (List[Product]): Siparişteki Product nesnelerinin listesi.
            status (OrderStatus): Siparişin başlangıç durumu (örn. PENDING).
            shipping_method (ShippingMethod): Sipariş için seçilen nakliye yöntemi.
            notification_service (NotificationService): Sipariş bildirimleri için kullanılacak servis.
            note (str): Siparişle ilgili ek notlar.

        Returns:
            Order: Başarılı bir şekilde oluşturulan Order nesnesi.

        Raises:
            Exception: Eğer sipariş edilen ürünlerden herhangi biri stokta yoksa.
        """
        for product in products:
            if product.stock <= 0:
                raise Exception(f"{product.name} is out of stock.")
            
        order = Order(order_id, customer, products, status, shipping_method, notification_type, note, "")
        self.save_order_to_db(order)
        customer.add_order(order)
        for product in products:
            product.stock -= 1
        return order

    def get_orders_by_customer(self, customer_name):
        """
        Belirtilen müşteri adına ait tüm siparişleri veritabanından getirir.

        Args:
            customer_name (str): Siparişleri getirilecek müşterinin adı.

        Returns:
            List[tuple]: Müşteriye ait siparişlerin listesi. Her bir sipariş,
                          (id, customer_address, products, note, status, shipping_method, total, tracking_number) bilgilerini içeren bir tuple olarak döndürülür.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, customer_address, products, note, status, shipping_method, total, tracking_number FROM orders WHERE customer_name = ?', (customer_name,))
        return cursor.fetchall()