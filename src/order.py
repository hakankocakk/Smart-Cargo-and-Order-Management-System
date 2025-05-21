from __future__ import annotations 
from typing import List
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from src.order import Order
from src.customer import Customer
from src.product import Product
from src.orderstatus import OrderStatus
from src.shippingMethod import ShippingMethod
from src.observer import Subject

class Order(Subject):
    def __init__(self, order_id: int, customer: Customer,
                 products: List[Product],
                 status: OrderStatus,
                 shipping_method: ShippingMethod):
        super().__init__()
        self.__id = order_id
        self.__customer = customer
        self.__products = products
        self.__status = status
        self.__shipping_method = shipping_method

    def calculate_total(self) -> float:
        """Calculate total price of products plus shipping cost."""
        product_total = sum(product.price for product in self.__products)
        shipping_cost = self.__shipping_method.calculateCoat()
        return product_total + shipping_cost

    def update_status(self, new_status: OrderStatus):
        """Update the order status."""
        self.__status = new_status
        self.notify(f"Sipariş {self.__id} durumu güncellendi: {new_status.value}")

    @property
    def id(self):
        return self.__id

    @property
    def status(self):
        return self.__status

    @property
    def customer(self):
        return self.__customer
    
    @property
    def products(self):
        """Get a copy of the products list to prevent direct modification."""
        return list(self.__products)

    @property
    def shipping_method(self):
        """Get the shipping method."""
        return self.__shipping_method