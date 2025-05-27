from __future__ import annotations 
from typing import List
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from src.order import Order
from src.customer import Customer
from src.product import Product
from src.order_status import OrderStatus
from src.shipping_method import ShippingMethod
from src.observer import Subject
from src.notification_service import NotificationService


class Order(Subject):
    """
    Bu class, bir müşteri siparişini yönetir; ürünleri, durumu, toplam maliyeti, notlari ve takip numarasini içerir.
    Observer (Gözlemci) tasarim deseninde bir 'Subject' (Konu) olarak görev yaparak,
    siparişin durumu değiştiğinde **kayitli gözlemcileri bilgilendirir** ve
    ilgili `NotificationService` araciliğiyla **müşteriye bildirim gönderir**.

    Attributes:
        __id (int): Siparişin benzersiz kimliği.
        __customer (Customer): Siparişi veren müşteri nesnesi.
        __products (List[Product]): Siparişteki ürünlerin listesi.
        __status (OrderStatus): Siparişin mevcut durumu (örn: Hazirlaniyor, Kargolandi, Teslim edildi).
        __shipping_method (ShippingMethod): Sipariş için kullanilan kargo metodu.
        __notification_service (NotificationService): Bildirim göndermek için kullanilan servis örneği.
        __note (str): Siparişle ilgili ek notlar.
        __tracking_number (int): Siparişin kargo takip numarasi.
        __total (float): Siparişin toplam maliyeti.
    """
    def __init__(self, order_id: int, customer: Customer,
                 products: List[Product],
                 status: OrderStatus,
                 shipping_method: ShippingMethod,
                 notification_service: NotificationService,
                 note: str,
                 tracking_number: int,
                 total: float = None):
        super().__init__()
        self.__id = order_id
        self.__customer = customer
        self.__products = products
        self.__status = status
        self.__shipping_method = shipping_method
        self.__notification_service = notification_service
        self.__note  = note
        self.__tracking_number = tracking_number

        if total is not None:
            self.__total = total
        else:
            self.__total = self.calculate_total()

    def calculate_total(self) -> float:
        """
        Siparişin toplam fiyatini (ürünlerin toplami + kargo maliyeti) hesaplar.

        Returns:
            float: Siparişin toplam maliyeti.
        """
        product_total = sum(product.price for product in self.__products)
        shipping_cost = self.__shipping_method.calculateCost()
        return product_total + shipping_cost
    
    
    def update_status(self, new_status: OrderStatus):
        """
        Siparişin durumunu günceller ve değişiklik hakkinda gözlemcilere bildirim gönderir.
        Ayrica, yapilandirilmiş `NotificationService`'i kullanarak müşteriye de bildirim sağlar.
        Kargolandi ve teslim edildi durumu için takip numarasini da bildirime ekler.

        Args:
            new_status (OrderStatus): Siparişin ayarlanacağı yeni durum.
        """
        self.__status = new_status.value

        message = f"Your order {self.id} status has been updated to {new_status.value}. Shipping tracking number: {self.tracking_number}"

        if self.__status == "Preparing":
            self.notify(f"Order {self.__id} status has been updated: {new_status.value}")
            message = f"Your order {self.id} status has been updated to {new_status.value}."

        if hasattr(self.__customer, '_Customer__email') and self.__notification_service.notification_type == "email":
            contact_info = self.__customer.get_email()
            self.__notification_service.send_notification(contact_info, message)
        elif hasattr(self.__customer, '_Customer__phone_number') and self.__notification_service.notification_type == "sms": 
            contact_info = self.__customer.get_phone_number()
            self.__notification_service.send_notification(contact_info, message)
        else:
            print(f"Could not send notification for order {self.id}: Contact info or type mismatch.")

    def __str__(self):
        product_names = ', '.join([product.name for product in self.__products])
        return f"Order ID: {self.__id}, Customer: {self.__customer.name}, Products: {product_names}, Status: {self.__status.value}, Shipping Method: {self.__shipping_method.__class__.__name__}"

    @property
    def id(self):
        """
        Siparişin benzersiz kimliğini döndürür.

        Returns:
            int: Sipariş ID'si.
        """
        return self.__id

    @property
    def status(self):
        """
        Siparişin mevcut durumunu döndürür.

        Returns:
            OrderStatus: Siparişin mevcut durumu.
        """
        return self.__status

    @property
    def customer(self):
        """
        Siparişi veren müşteri nesnesini döndürür.

        Returns:
            Customer: Müşteri nesnesi.
        """
        return self.__customer
    
    @property
    def products(self):
        """
        Sipariş edilen ürünlerin kopyasini döndürür.
        Listenin doğrudan dışarıdan değiştirilmesini önlemek için bir kopya döndürülür.

        Returns:
            List[Product]: Siparişteki ürünlerin listesi.
        """
        return list(self.__products)

    @property
    def shipping_method(self):
        """
        Sipariş için kullanilan kargo metodunu döndürür.

        Returns:
            ShippingMethod: Kargo metodu nesnesi.
        """
        return self.__shipping_method
    
    @property
    def total(self):
        """
        Siparişin toplam maliyetini döndürür.

        Returns:
            float: Siparişin toplam maliyeti.
        """
        return self.__total
    
    @property
    def note(self):
        """
        Siparişle ilgili ek notlari döndürür.

        Returns:
            str: Sipariş notu.
        """
        return self.__note
    
    @property
    def tracking_number(self):
        """
        Siparişin kargo takip numarasini döndürür.

        Returns:
            int: Kargo takip numarasi.
        """
        return self.__tracking_number
    
    def add_tracking_number(self, tracking_number):
        """
        Siparişin kargo takip numarasini günceller.
        Bu metod, sipariş kargolandiğinda takip numarasini atamak için kullanilir.

        Args:
            tracking_number (int): Siparişe atanacak yeni takip numarası.
        """
        self.__tracking_number = tracking_number