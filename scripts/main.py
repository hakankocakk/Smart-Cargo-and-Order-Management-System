import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.inventorymanager import ProductManager
from src.product import Product

if __name__ == "__main__":
    manager = ProductManager()

    product1 = Product(id=1, name="Laptop", category="Electronics", stock=10, price=1500.0)
    product2 = Product(id=1, name="Kettle", category="Home Appliances", stock=25, price=30.0)
    manager.add_product(product1)
    manager.add_product(product2)

    for p in manager.list_products():
        print(p)


    electronics = manager.filter_by_category("Electronics")
    print("Electronics:", electronics)

    manager.update_stock(product_id=1, new_stock=8)
    print("New stock for product 1:", manager.get_stock(1))

    for p in manager.list_products():
        print(p)