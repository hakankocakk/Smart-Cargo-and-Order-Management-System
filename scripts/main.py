import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.inventorymanager import ProductManager
from src.product import Product


USERS = {
    "Nilgun": {"password": "admin123", "role": "manager"},
    "Hakan": {"password": "hakosahilde33", "role": "customer", "email": "hakan@example.com"},
    "Nur": {"password": "nuruyuyo00", "role": "customer", "email": "nur@example.com"},
    "Leyla": {"password": "leylasahilde33", "role": "customer", "email": "leyla@example.com"},
}


def login():
    
    print("=======Login=======")
    username = input("Please enter a username: ")
    password = input("Please enter a password: ")

    user = USERS.get(username)

    if user and user["password"]==password:
        print(f"Login successful. Welcome {username}!")
        return username, user["role"], user.get("email")
    else:
        print("Wrong username or password.")
        return None, None, None


def display_products(inventory_manager):

    print("\n======= Available Products =======")
    products = inventory_manager.list_products()
    for product in products:
        print(f"ID: {product.id} | Name: {product.name} | Category: {product.category} | Stock: {product.stock} | Price: ${product.price:.2f}")


def manager_menu(inventory_manager):

    while True:
        print("\n--- Manager Menu ---")
        print("1. List Product")
        print("2. Add Product")
        print("3. Reduce Stock")
        print("4. Update Stock")
        print("5. Exit")
        choice = input("Choice: ")

        if choice == "1":
            display_products(inventory_manager)

        elif choice == "2":
            try:
                product_id = int(input("Enter a product id: "))
                product_name = input("Enter a product name: ")
                product_category = input("Enter a product category: ")
                product_stock = int(input("Enter a product stock: "))
                product_price = input("Enter a product price: ")

                product = Product(id=product_id, name=product_name, category=product_category, stock=product_stock, price=product_price)
                inventory_manager.add_product(product)
                print("Product added successfully.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            break
             

def main():

    inventory_manager = ProductManager()
    username, role, mail = login()

    if not username:
        return
    
    if role == "manager":
        manager_menu(inventory_manager)


if __name__ == "__main__":

    main()