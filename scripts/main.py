import sys
import os
import sqlite3
import threading
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.inventory_management import ProductManagement
from src.product import Product
from src.order import Order
from src.order_status import OrderStatus
from src.customer import Customer
from src.order_factory import OrderFactory
from src.shipping_method import ShippingSelector
from src.cart import Cart
from src.order_management import OrderManagement
from src.product_factory import ProductFactory
from src.electronics_product import ElectronicsProduct
from src.book_product import BookProduct
from src.notification_service import NotificationService

CUSTOMER_OBJECTS = {}
current_order_statuses = {}


def sign_up():
    """
    Kullanıcı kaydını yönetir.

    Kullanıcıdan adını, soyadını, kullanıcı adını, şifresini, e-posta adresini,
    telefon numarasını ve adresini girmesini ister. Seçilen kullanıcı adının
    'users.db' veritabanında zaten mevcut olup olmadığını kontrol eder.
    Kullanıcı adı veritabaninda mevcut değilse, yeni kullanıcının bilgilerini 'customer' rolüyle
    veritabanına ekler.
    """
    conn = sqlite3.connect("databases/users.db")

    while True:
        print("=======Sign Up=======")
        name = input("Please enter a name: ")
        surname = input("Please enter a surname: ")
        username = input("Please enter a username: ")
        password = input("Please enter a password: ")
        email = input("\nPlease enter a email: ")
        phone_number = input("\nPlease enter a phone number: ")
        address = input("\nPlease enter a address: ")


        try:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = user.fetchone()

            if  user:
                print("This username is already in use. Please choose a different one.")

            else:
                query = "INSERT INTO users (username, password, role, name, surname, phone_number, email, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                conn.execute(query, (username, password, 'customer', name, surname, phone_number, email, address))
                conn.commit()
                print("Your account has been created successfully.")
                break

        except Exception as e:
            print(f"Error: {e}")


def sign_in():
    """
    Kullanıcı girişini yönetir.

    Kullanıcıdan kullanıcı adını ve şifresini girmesini ister. Sağlanan
    kimlik bilgilerinin 'users.db' veritabanındaki mevcut bir kullanıcıyla
    eşleşip eşleşmediğini kontrol eder. Giriş başarılı olursa, bir hoş geldiniz
    mesajı yazdırır ve kullanıcının veritabanı kaydını döndürür. Aksi takdirde,
    bir hata mesajı yazdırır ve None döndürür.

    Returns:
        tuple or None: Giriş başarılı olursa kullanıcının veritabanındaki
                       verilerini içeren bir demet (tuple), aksi takdirde None.
    """
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
        return user
    else:
        print("Wrong username or password.")
        return None


def display_products(inventory_manager):
    """
    Tüm mevcut ürünlerin biçimlendirilmiş bir listesini görüntüler.

    `inventory_manager`dan ürün listesini alır. Her ürün için,
    kimliğini, adını, kategorisini, mevcut stokunu ve fiyatını görüntüler.
    Ürün bir `ElectronicsProduct` ise garanti yılını da gösterir.
    Bir `BookProduct` ise yazar ve yayıncıyı gösterir.
    Ürün yoksa, ilgili bir mesaj yazdırır.

    Args:
        inventory_manager (ProductManagement): Ürün verilerini almak için kullanılan ProductManagement sınıfının bir örneği.
    """
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
    """
    Yönetici menüsünü sunar ve yöneticiye özgü eylemleri yönetir.

    Yöneticilerin şunları yapmasına olanak tanır:
    1. Tüm ürünleri listelemek.
    2. Yeni ürünler (Elektronik, Kitap veya Standart) belirli özelliklerle eklemek.
    3. Mevcut bir ürünün stoğunu azaltmak.
    4. Mevcut bir ürünün stoğunu güncellemek.
    5. Tüm müşteri siparişlerini göstermek.
    6. Siparişleri duruma göre filtrelemek.
    7. Belirli bir siparişin durumunu güncellemek.
    8. Yönetici menüsünden çıkmak.

    Args:
        inventory_manager (ProductManagement): Ürünleri yönetmek için `ProductManagement` sınıfının bir örneği.
        order_manager (OrderManagement): Siparişleri yönetmek için `OrderManagement` sınıfının bir örneği.
        product_factory (ProductFactory): Ürün nesneleri oluşturmak için `ProductFactory` sınıfının bir örneği.
    """
    
    
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
                product_type = input("Enter product type (Electronics, Book, Standard): ").lower()
                product_stock = int(input("Enter a product stock: "))
                product_price = input("Enter a product price: ")

                #Kategoriye göre Product nesnesi oluşturur
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
                else: 
                    product_category = input("Enter product category (e.g., General): ") 
                    product = product_factory.create_product(
                        "standard", id=product_id, name=product_name,
                        category=product_category, stock=product_stock, price=product_price 
                    )

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
    """
    Belirli bir müşteri için sipariş durumunu sürekli olarak izler.

    Bu fonksiyon ayrı bir iş parçacığında (thread) çalışır ve periyodik olarak
    müşterinin siparişlerindeki güncellemeler için 'orders.db' veritabanını
    kontrol eder. Bir siparişin durumu değişirse, `Order` nesnesini günceller,
    müşteriyi bir gözlemci olarak ekler ve müşteriyi durum değişikliği hakkında
    bilgilendirir. Sipariş "Kargolandı" durumuna geçtiğinde, kargo takip numarası
    oluşturulur ve bu bilgi de müşteriye bildirilir. Durum güncellemelesi bildirimden
    sonra `print_customer_menu()` çağrılarak müşterinin yapmak istediği işlem ekranı
    tekrar CLI'ye bastırılır. 

    Args:
        customer (Customer): Siparişleri izlenen müşteri nesnesi.
    """
    global current_order_statuses
    while True:
        conn = sqlite3.connect("databases/orders.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM orders WHERE customer_name = ?", (customer.name,))
            my_orders = cursor.fetchall()
            order_factory = OrderFactory()
            for i in my_orders:
                order = Order(i[0], customer, [i[3]], i[5], i[6], NotificationService("sms"), i[4], i[8], i[7])
                if order.id not in current_order_statuses or current_order_statuses[order.id] != order.status:
                    if order.id in current_order_statuses:
                        order.attach(customer)
                        if order.status == "Preparing":
                            order.update_status(OrderStatus.PREPARING)
                        elif order.status == "Shipped":
                            order_factory.create_tracking_number(order.id)
                            tracking_number = order_factory.get_tracking_number(order.id)
                            order.add_tracking_number(tracking_number)
                            order.update_status(OrderStatus.SHIPPED)
                        elif order.status == "Delivered":
                            order.update_status(OrderStatus.DELIVERED)
                        print_customer_menu()
                    current_order_statuses[order.id] = order.status
        except Exception as e:
                print(f"Error: {e}")
        time.sleep(10)


def print_customer_menu():
    """
    Müşteri menüsünde bulunan seçenekleri yazdırır.
    """
    print("\n1. List the Products")
    print("2. Filter by Category")
    print("3. Create Order")
    print("4. Show Order History")
    print("5. Exit")
    print("Your choice: ")

def customer_menu(inventory_manager, user):
    """
    Müşteri menüsünü sunar ve müşteriye özgü eylemleri yönetir.

    Müşterilerin şunları yapmasına olanak tanır:
    1. Tüm mevcut ürünleri listelemek.
    2. Ürünleri kategoriye göre filtrelemek.
    3. Sepete ürün ekleyerek, siparişe not, aciliyet, bildirim tipi ve gönderim yöntemi seçerek yeni bir sipariş oluşturmak. Sipariş daha sonra veritabanına kaydedilir ve ürün stoğu azaltılır.
    4. Sipariş geçmişini görüntülemek.
    5. Müşteri menüsünden çıkmak.

    Ayrıca, mevcut müşteri için sipariş durumu değişikliklerini izlemek üzere
    bir arka plan iş parçacığı (`pool_for_order_status`) başlatır.

    Args:
        inventory_manager (ProductManagement): Ürünleri yönetmek için `ProductManagement` sınıfının bir örneği.
        user (tuple): Giriş yapmış müşterinin veritabanından alınan verilerini içeren bir demet (örn: (id, kullanıcı adı, şifre, rol, ad, vb.)).
    """
    print(f"\n--- Hoşgeldiniz, {user[1]}! ---")
    if user[1] not in CUSTOMER_OBJECTS:
        CUSTOMER_OBJECTS[user[1]] = Customer(customer_id=user[0], name=user[4], surname=user[5], phone_number=user[6], email=user[7], order_history=[], address=user[8])
    customer = CUSTOMER_OBJECTS[user[1]]
    order_factory = OrderFactory()

    username = user[1]

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
            products = inventory_manager.filter_by_category(kategori)
            for product in products:
                product_info = f"ID: {product.id} | Name: {product.name} | Category: {product.category} | Stock: {product.stock} | Price: ${product.price:.2f}"

                if isinstance(product, ElectronicsProduct):
                    product_info += f" | Warranty: {product.warranty_years} years"
                elif isinstance(product, BookProduct):
                    product_info += f" | Author: {product.author} | Publisher: {product.publisher}"
    
                print(product_info)

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

            note = " "
            choice = input("Do you want to add note? (y/n): ").strip().lower()
            if choice == "y":
                note = input("Note: ")

            urgency = input("Is it urgent? (high/low): ")
            notification = input("Notification service type (email/sms): ")
            total_items = sum(adet for _, adet in cart)
            shipping_method = ShippingSelector.select_best_method(order_weight=total_items, urgency=urgency)
            product_list = []
            for product, adet in cart:
                product_list.extend([product] * adet)
                inventory_manager.reduce_stock(product.name, adet)

            order_id = order_factory.get_next_order_id()
            order = order_factory.create_order(order_id=order_id, customer=customer, products=product_list, status=OrderStatus.PREPARING, shipping_method=shipping_method, notification_type=NotificationService(notification), note=note)
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
                for i, (oid, address, products, note, status, shipping, total, tracking_number) in enumerate(orders, 1):
                    print(f"{i}. Order ID: {oid} | Products: {products} | Status: {status} | Note: {note} | Shipping: {shipping} | Total: {total}"
                          f"| Address : {address} | Tracking Number: {tracking_number}")
        elif secim == "5":
            break
        else:
            print("Unvalid choice. Please try again.")
             

def main():
    """
    E-ticaret uygulamasının ana fonksiyonu.

    Kullanıcıya başlangıç menüsünü sunar, şunları yapmasına olanak tanır:
    1. Kaydol: Yeni bir kullanıcı hesabı oluşturmak.
    2. Giriş Yap: Mevcut bir hesaba giriş yapmak.
    3. Çıkış: Uygulamayı sonlandırmak.

    Başarılı girişin ardından, kullanıcıyı atanmış rolüne göre yönetici
    menüsüne veya müşteri menüsüne yönlendirir.
    """

    while True:
        print("\n--- Welcome to OOP Store ---")
        print("1. Sign Up: ")
        print("2. Sign In: ")
        print("3. Exit: ")
        choice = input("Choice: ")

        if choice == "1":
            sign_up()

        elif choice == "2":
            user = sign_in()
            inventory_manager = ProductManagement()

            if not user:
                continue
            
            if user[3] == "manager":
                order_manager = OrderManagement()
                product_factory = ProductFactory()
                manager_menu(inventory_manager, order_manager, product_factory)
            
            elif user[3] == "customer":
                customer_menu(inventory_manager, user)
            
            else:
                print("Unauthorized access")

        elif choice == "3":
            print("Good Bye!")
            break
        else:
            print("Please enter a valid value.")


if __name__ == "__main__":

    main()