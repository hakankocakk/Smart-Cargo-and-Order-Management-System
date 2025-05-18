import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.inventorymanager import ProductManager
from src.product import Product
from src.customer import Customer
from src.orderstatus import OrderStatus
from src.shippingMethod import CheapShipping
from src.orderfactory import OrderFactory

# Example products
products = [Product(id=1, name = "Laptop",category="Electronics",stock=200, price=1500), Product(id=1, name = "Mouse",category="Accesories",stock=100, price=50)]

# Customer
customer = Customer(customer_id=123, name="Alice",surname="Smith", phone_number="0903940394", email="mksdlfmsdfa",order_history=[], address="123 Main Street")

# Shipping method
shipping_method = CheapShipping()

# Create factory and order
factory = OrderFactory()
order = factory.create_order(
    order_id=1,
    customer=customer,
    products=products,
    status=OrderStatus.PENDING,
    shipping_method=shipping_method
)

print(f"Order {order.id} created and saved with total: ${order.calculate_total():.2f}")
