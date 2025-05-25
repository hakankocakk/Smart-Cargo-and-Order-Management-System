import sys
import os
import sqlite3
import threading
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.inventorymanager import ProductManager
from src.product import Product
from src.order import Order
from src.orderstatus import OrderStatus
from src.customer import Customer
from src.orderfactory import OrderFactory
from src.shippingMethod import ShippingSelector
from src.cart import Cart
from src.ordermanagement import OrderManager
from src.product_factory import ProductFactory
from src.electronics_product import ElectronicsProduct
from src.book_product import BookProduct


CUSTOMER_OBJECTS = {}
current_order_statuses = {}


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
    products = inventory_manager.list_products() # Bu, artık doğru alt sınıf nesnelerini döndürecek

    if not products:
        print("No products available.")
        return

    for product in products:
        product_info = f"ID: {product.id} | Name: {product.name} | Category: {product.category} | Stock: {product.stock} | Price: ${product.price:.2f}"

        if isinstance(product, ElectronicsProduct):
            product_info += f" | Warranty: {product.warranty_years} years"
        elif isinstance(product, BookProduct):
            product_info += f" | Author: {product.author} | Publisher: {product.publisher}"
            
        print(product_info)


def manager_menu(inventory_manager, order_manager, product_factory):
    
    while True:
        print("\n--- Manager Menu ---")
        print("1. List Product")
        print("2. Add Product")
        print("3. Reduce Stock")
        print("4. Update Stock")
        print("5. Show Order")
        print("6. Filter by Order Status")
        print("7. Update Order Status")
        print("8. Exit")
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
                #product_category = input("Enter a product category: ")
                product_type = input("Enter product type (Electronics, Book, Standard): ").lower()
                product_stock = int(input("Enter a product stock: "))
                product_price = input("Enter a product price: ")

                if product_type == "electronics":
                    warranty_years = int(input("Enter warranty years: "))
                    product = product_factory.create_product(
                        product_type, id=product_id, name=product_name,
                        stock=product_stock, price=product_price, warranty_years=warranty_years
                    )
                elif product_type == "book":
                    author = input("Enter author: ")
                    publisher = input("Enter publisher: ")
                    product = product_factory.create_product(
                        product_type, id=product_id, name=product_name,
                        stock=product_stock, price=product_price, author=author, publisher=publisher
                    )
                else: # Varsayılan veya bilinmeyen tip için
                    product_category = input("Enter product category (e.g., General): ") # Varsayılan kategori
                    product = product_factory.create_product(
                        "standard", id=product_id, name=product_name,
                        category=product_category, stock=product_stock, price=product_price # category'yi Product'a ilet
                    )

                #product = Product(id=product_id, name=product_name, category=product_category, stock=product_stock, price=product_price)
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
            try:
                order_manager.show_orders()
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "6":
            try:
                status = input("Order Status ('Preparing', 'Shipped', 'Delivered'): ")
                order_manager.filter_by_order_status(status)
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "7":
            try:
                order_manager.show_orders()
                order_id = int(input("Order ID: "))
                status = input("Order Status ('Preparing', 'Shipped', 'Delivered'): ")
                order_manager.update_by_order_status(order_id, status)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "8":
            print("Good By Admin!")
            break

        else:
            print("Please enter a valid value.")



def pool_for_order_status(customer):
    global current_order_statuses
    while True:
        conn = sqlite3.connect("databases/orders.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM orders WHERE customer_name = ?", (customer.name,))
            my_orders = cursor.fetchall()
            for i in my_orders:
                order = Order(i[0], i[1], [i[3]], i[4], i[5])
                if order.id not in current_order_statuses or current_order_statuses[order.id] != order.status:
                    if order.id in current_order_statuses:
                        order.attach(customer)
                        order.notify(f"Order {order.id} status has been updated: {order.status}")
                        print_customer_menu()
                    current_order_statuses[order.id] = order.status
        except Exception as e:
                print(f"Error: {e}")
        time.sleep(10)


def print_customer_menu():
    print("\n1. List the Products")
    print("2. Filter by Category")
    print("3. Create Order")
    print("4. Show Order History")
    print("5. Exit")
    print("Your choice: ")

def customer_menu(inventory_manager, username, mail):
    print(f"\n--- Hoşgeldiniz, {username}! ---")
    if username not in CUSTOMER_OBJECTS:
        CUSTOMER_OBJECTS[username] = Customer(customer_id=1, name=username, surname="", phone_number="", email=mail, order_history=[], address="adres")
    customer = CUSTOMER_OBJECTS[username]
    order_factory = OrderFactory()


    polling_thread = threading.Thread(target=pool_for_order_status, args=(customer,))
    polling_thread.daemon = True
    polling_thread.start()


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
            cart = Cart()
            while True:
                display_products(inventory_manager)     
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
                cart.add(selected[0], adet)
                print(f"Added {adet} of {selected[0].name} to your cart.")
                kategori = selected[0].category
                print(f"\nSee other products from '{kategori}' category:")
                kategori_urunler = [p for p in urunler if p.category == kategori and p.id != selected[0].id]
                if kategori_urunler:
                    for product in kategori_urunler:
                        print(f"ID: {product.id} | Name: {product.name} | Stock: {product.stock} | Price: ${product.price:.2f}")
                else:
                    print("No other products found in this category.")
                    
                while True:
                    devam = input("Do you want to add more products? (y/n): ").strip().lower()
                    if devam == "y":
                        break
                    elif devam == "n":
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                        
                if devam == "n":
                    break

            if cart.is_empty():
                print("No products selected.")
                continue

            urgency = input("Is it urgent? (high/low): ")
            total_items = sum(adet for _, adet in cart)
            shipping_method = ShippingSelector.select_best_method(order_weight=total_items, urgency=urgency)
            product_list = []
            for product, adet in cart:
                product_list.extend([product] * adet)
                inventory_manager.reduce_stock(product.name, adet)

            order_id = order_factory.get_next_order_id()
            order = order_factory.create_order(order_id=order_id, customer=customer, products=product_list, status=OrderStatus.PREPARING, shipping_method=shipping_method)
            order.attach(customer)
            order.update_status(OrderStatus.PREPARING)
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
            inventory_manager = ProductManager()

            if not username:
                return
            
            if role == "manager":
                order_manager = OrderManager()
                product_factory = ProductFactory()
                manager_menu(inventory_manager, order_manager, product_factory)
            
            elif role == "customer":
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