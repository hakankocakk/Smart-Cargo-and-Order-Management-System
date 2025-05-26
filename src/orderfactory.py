import sqlite3
from typing import List
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.order import Order
from src.customer import Customer
from src.product import Product
from src.orderstatus import OrderStatus
from src.shippingMethod import ShippingMethod
from src.orderDecorator import logOrderCreation
from src.notificationService import NotificationService

class OrderFactory:
    """
    'OrderFactory' sınıfı, sipariş nesneleri oluşturmaktan ve bu siparişleri bir veritabanında yönetmekten sorumludur.
    Bu sınıf, bir fabrika deseni (Factory Pattern) uygulayarak sipariş oluşturma sürecini soyutlar ve
    veritabanı etkileşimlerini kapsüller.
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
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_name TEXT,
                customer_address TEXT,
                products TEXT,
                status TEXT,
                shipping_method TEXT,
                total REAL
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
    
    def save_order_to_db(self, order: Order):
        """
        Verilen Order nesnesini veritabanına kaydeder.
        Siparişin ID'si, müşteri bilgileri, ürünleri, durumu, nakliye yöntemi ve toplam maliyeti gibi
        detayları 'orders' tablosuna ekler.

        Args:
            order (Order): Veritabanına kaydedilecek olan Order nesnesi.
        """
        cursor = self.conn.cursor()
        product_names = ', '.join([p.name for p in order._Order__products])  
        total = order.calculate_total()
        shipping_method_name = type(order._Order__shipping_method).__name__
        cursor.execute('''
           INSERT INTO orders (id, customer_name, customer_address, products, status, shipping_method, total)
           VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            order.id,
            order.customer.name,
            order.customer.get_address(),  
            product_names,
            order.status.value,
            shipping_method_name,
            total
       ))
        self.conn.commit() 
    @logOrderCreation
    def create_order(self, order_id: int, customer: Customer, products: List[Product],
                     status: OrderStatus, shipping_method: ShippingMethod,  notification_type: NotificationService) -> Order:
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
            notification_type (NotificationService): Sipariş bildirimleri için kullanılacak servis tipi.

        Returns:
            Order: Başarılı bir şekilde oluşturulan Order nesnesi.

        Raises:
            Exception: Eğer sipariş edilen ürünlerden herhangi biri stokta yoksa.
        """
        for product in products:
            if product.stock <= 0:
                raise Exception(f"{product.name} is out of stock.")
            
        order = Order(order_id, customer, products, status, shipping_method, notification_type)
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
                          (id, products, status, shipping_method, total) bilgilerini içeren bir tuple olarak döndürülür.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, products, status, shipping_method, total FROM orders WHERE customer_name = ?', (customer_name,))
        return cursor.fetchall()