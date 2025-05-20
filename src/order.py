from typing import List
from customer import Customer
from product import Product
from orderstatus import OrderStatus
from shippingMethod import ShippingMethod
from notificationService import NotificationService 

class Order:
    def __init__(self, order_id: int, customer: Customer,
                 products: List[Product],
                 status: OrderStatus,
                 shipping_method: ShippingMethod,
                 notification_service: NotificationService):
        self.__id = order_id
        self.__customer = customer
        self.__products = products
        self.__status = status
        self.__shipping_method = shipping_method
        self.__notification_service = notification_service 

    def calculate_total(self) -> float:
        """Calculate total price of products plus shipping cost."""
        product_total = sum(product.price for product in self.__products)
        shipping_cost = self.__shipping_method.calculateCoat()
        return product_total + shipping_cost

    def update_status(self, new_status: OrderStatus):
        """Update the order status and send a notification.""" 
        self.__status = new_status
        message = f"Your order {self.id} status has been updated to {new_status.value}."        # Status_degistiginde gidecek
        if hasattr(self.__customer, 'email') and self.__notification_service.notification_type == "email":
            contact_info = self.__customer.email
            self.__notification_service.send_notification(contact_info, message)
        elif hasattr(self.__customer, 'phone_number') and self.__notification_service.notification_type == "sms": 
            contact_info = self.__customer.phone_number
            self.__notification_service.send_notification(contact_info, message)
        else:
            print(f"Could not send notification for order {self.id}: Contact info or type mismatch.")

    @property
    def id(self):
        return self.__id

    @property
    def status(self):
        return self.__status

    @property
    def customer(self):
        return self.__customer

