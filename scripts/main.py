import sys
import os
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.inventorymanager import ProductManager
from src.product import Product
from src.orderstatus import OrderStatus
from src.customer import Customer
from src.orderfactory import OrderFactory
from src.shippingMethod import ShippingSelector



def sign_up():
    conn = sqlite3.connect("databases/users.db")

    while True:
        print("=======Sign Up=======")
        username = input("Please enter a username: ")
        password = input("Please enter a password: ")
        email = input("\nPlease enter a email: ")

        try:
                user = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
                user = user.fetchone()

                if  user:
                    print("This username is already in use. Please choose a different one.")

                else:
                    query = "INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)"
                    conn.execute(query, (username, password, 'customer', email))
                    conn.commit()
                    print("Your account has been created successfully.")
                    break

        except Exception as e:
            print(f"Error: {e}")


def sign_in():
    conn = sqlite3.connect("databases/users.db")

    print("=======Sign In=======")
    username = input("Please enter a username: ")
    password = input("Please enter a password: ")

    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = user.fetchone()
    password_db = conn.execute("SELECT password FROM users WHERE username = ?", (username,))
    password_db = password_db.fetchone()

    if user and password_db[0]==password:
        print(f"Login successful. Welcome {username}!")
        return username, user[3], user[4]
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
            try:
                display_products(inventory_manager)
            except Exception as e:
                print(f"Error: {e}")

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

        elif choice == "3":
            try:
                display_products(inventory_manager)
                product_name = input("Enter product name: ")
                product_quantity = int(input("Enter product quantity: "))
                status = inventory_manager.reduce_stock(product_name, product_quantity)
                print(status,"\n")
                display_products(inventory_manager)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            try:
                display_products(inventory_manager)
                product_name = input("Enter product id: ")
                new_stock = int(input("Enter new stock: "))
                inventory_manager.update_stock(product_name, new_stock)
                display_products(inventory_manager)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            print("Good By Admin!")
            break

        else:
            print("Please enter a valid value.")

CUSTOMER_OBJECTS = {}

def customer_menu(inventory_manager, username, mail):
    print(f"\n--- Hoşgeldiniz, {username}! ---")
    if username not in CUSTOMER_OBJECTS:
        CUSTOMER_OBJECTS[username] = Customer(customer_id=1, name=username, surname="", phone_number="", email=mail, order_history=[], address="adres")
    customer = CUSTOMER_OBJECTS[username]
    order_factory = OrderFactory()
    while True:
        print("\n1. List the Products")
        print("2. Filter by Category")
        print("3. Create Order")
        print("4. Show Order History")
        print("5. Exit")
        secim = input("Your choice: ")
        if secim == "1":
            display_products(inventory_manager)
        elif secim == "2":
            kategori = input("Category Name: ")
            urunler = inventory_manager.filter_by_category(kategori)
            for product in urunler:
                print(f"ID: {product.id} | Name: {product.name} | Stock: {product.stock} | Price: ${product.price:.2f}")
        elif secim == "3":
            product_id = int(input("Product ID of your choice: "))
            urunler = inventory_manager.list_products()
            selected = [p for p in urunler if p.id == product_id]
            if not selected:
                print("Could not find the product.")
                continue
            adet = int(input("How many?: "))
            if selected[0].stock < adet:
                print("Product is out of stock!")
                continue
            urgency = input("Is it urgent? (high/low): ")
            shipping_method = ShippingSelector.select_best_method(order_weight=adet, urgency=urgency)
            product_list = [selected[0]] * adet
            order_id = order_factory.get_next_order_id()
            order = order_factory.create_order(order_id=order_id, customer=customer, products=product_list, status=OrderStatus.PREPARING, shipping_method=shipping_method)
            order.attach(customer)
            order.update_status(OrderStatus.SHIPPED)
            print("Order has been created and saved.")
        elif secim == "4":
            # Sipariş geçmişini veritabanından çek ve göster
            orders = order_factory.get_orders_by_customer(username)
            if not orders:
                print("No order history found.")
            else:
                print("Your Order History:")
                for i, (oid, products, status, shipping, total) in enumerate(orders, 1):
                    print(f"{i}. Order ID: {oid} | Products: {products} | Status: {status} | Shipping: {shipping} | Total: {total}")
        elif secim == "5":
            break
        else:
            print("Unvalid choice. Please try again.")
             

def main():

    while True:
        print("\n--- Welcome to OOP Store ---")
        print("1. Sign Up: ")
        print("2. Sign In: ")
        print("3. Exit: ")
        choice = input("Choice: ")

        if choice == "1":
            sign_up()

        elif choice == "2":
            username, role, mail = sign_in()

            if not username:
                return
            
            if role == "manager":
                inventory_manager = ProductManager()
                manager_menu(inventory_manager)
            
            elif role == "customer":
                inventory_manager = ProductManager()
                customer_menu(inventory_manager, username, mail)
            
            else:
                print("Unauthorized access")

        elif choice == "3":
            print("Good Bye!")
            break
        else:
            print("Please enter a valid value.")


if __name__ == "__main__":

    main()