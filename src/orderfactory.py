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
    def __init__(self, db_path: str = "databases/orders.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_orders_table()

    def create_orders_table(self):
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

"""    def create_order(self, order_id: int, customer: Customer, products: List[Product],
                     status: OrderStatus, shipping_method: ShippingMethod) -> Order:
        order = Order(order_id, customer, products, status, shipping_method)
        self.save_order_to_db(order)
        return order"""
    
    def get_next_order_id(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT MAX(id) FROM orders')
        result = cursor.fetchone()
        return (result[0] + 1) if result[0] is not None else 1
    
    def save_order_to_db(self, order: Order):
        cursor = self.conn.cursor()
        product_names = ', '.join([p.name for p in order._Order__products])  # accessing private attribute
        total = order.calculate_total()
        shipping_method_name = type(order._Order__shipping_method).__name__
        cursor.execute('''
           INSERT INTO orders (id, customer_name, customer_address, products, status, shipping_method, total)
           VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            order.id,
            order.customer.name,
            order.customer.get_address(),  # Changed to use the getter method
            product_names,
            order.status.value,
            shipping_method_name,
            total
       ))
        self.conn.commit() 
    @logOrderCreation
    def create_order(self, order_id: int, customer: Customer, products: List[Product],
                     status: OrderStatus, shipping_method: ShippingMethod, notification_type: NotificationService) -> Order:
        # Stok kontrolü: stokta olmayan ürün sipariş edilemez
        for product in products:
            if product.stock <= 0:
                raise Exception(f"{product.name} is out of stock.")
        order = Order(order_id, customer, products, status, shipping_method, notification_type)
        self.save_order_to_db(order)
        # Sipariş müşteri geçmişine eklenir
        customer.add_order(order)
        # Sipariş edilen ürünlerin stoğu güncellenir
        for product in products:
            product.stock -= 1
        return order

    def get_orders_by_customer(self, customer_name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, products, status, shipping_method, total FROM orders WHERE customer_name = ?', (customer_name,))
        return cursor.fetchall()