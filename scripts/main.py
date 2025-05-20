import sys
import os
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.inventorymanager import ProductManager
from src.product import Product



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


def customer_menu():
    pass
             

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
                customer_menu()
            
            else:
                print("Unauthorized access")

        elif choice == "3":
            print("Good By!")
            break
        else:
            print("Please enter a valid value.")


if __name__ == "__main__":

    main()