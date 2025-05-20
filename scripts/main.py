import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.inventorymanager import ProductManager
from src.product import Product
from src.customer import Customer
from src.orderfactory import OrderFactory
from src.orderstatus import OrderStatus
from src.shippingMethod import ShippingSelector


USERS = {
    "Nilgun": {"password": "admin123", "role": "manager"},
    "Hakan": {"password": "hakosahilde33", "role": "customer", "email": "hakan@example.com"},
    "Nur": {"password": "nuruyuyo00", "role": "customer", "email": "nur@example.com"},
    "Leyla": {"password": "leylasahilde33", "role": "customer", "email": "leyla@example.com"},
}


def login():
    print("=======Giriş=======")
    username = input("Lütfen kullanıcı adınızı girin: ")
    password = input("Lütfen şifrenizi girin: ")

    user = USERS.get(username)

    if user and user["password"]==password:
        print(f"Giriş yapıldı. {username}, hoşgeldiniz!")
        return username, user["role"], user.get("email")
    else:
        print("Kullanıcı adı veya şifre hatalı.")
        return None, None, None


def display_products(inventory_manager):
    print("\n======= Ürünler =======")
    products = inventory_manager.list_products()
    for product in products:
        print(f"ID: {product.id} | Ürün İsmi: {product.name} | Kategori: {product.category} | Stok durumu: {product.stock} | Fiyat: ${product.price:.2f}")


def manager_menu(inventory_manager):
    while True:
        print("\n--- Yönetici Menü ---")
        print("1. Ürünleri Listele")
        print("2. Ürün Ekle")
        print("3. Ürün Sil")
        print("4. Ürün Güncelle")
        print("5. Çıkış")
        choice = input("Seçim: ")

        if choice == "1":
            display_products(inventory_manager)

        elif choice == "2":
            try:
                product_id = int(input("Ürün ID girin: "))
                product_name = input("Ürün ismi girin: ")
                product_category = input("Ürün kategorisi girin: ")
                product_stock = int(input("Ürün stok miktarı girin: "))
                product_price = float(input("Ürün fiyatı girin: "))
                product = Product(id=product_id, name=product_name, category=product_category, stock=product_stock, price=product_price)
                inventory_manager.add_product(product)
                print("Ürün başarıyla eklendi.")
            except Exception as e:
                print(f"Hata: {e}")

        elif choice == "3":
            try:
                product_id = int(input("Silmek istediğiniz ürünün ID'sini girin: "))
                inventory_manager.conn.execute("DELETE FROM Product WHERE id = ?", (product_id,))
                inventory_manager.conn.commit()
                print("Ürün başarıyla silindi.")
            except Exception as e:
                print(f"Hata: {e}")

        elif choice == "4":
            try:
                product_id = int(input("Güncellemek istediğiniz ürünün ID'sini girin: "))
                new_name = input("Yeni ürün ismi (boş bırakılırsa değişmez): ")
                new_category = input("Yeni kategori (boş bırakılırsa değişmez): ")
                new_stock = input("Yeni stok (boş bırakılırsa değişmez): ")
                new_price = input("Yeni fiyat (boş bırakılırsa değişmez): ")
                # Mevcut ürünü çek
                cursor = inventory_manager.conn.execute("SELECT name, category, stock, price FROM Product WHERE id = ?", (product_id,))
                row = cursor.fetchone()
                if not row:
                    print("Ürün bulunamadı.")
                    continue
                name = new_name if new_name else row[0]
                category = new_category if new_category else row[1]
                stock = int(new_stock) if new_stock else row[2]
                price = float(new_price) if new_price else row[3]
                inventory_manager.conn.execute("UPDATE Product SET name = ?, category = ?, stock = ?, price = ? WHERE id = ?", (name, category, stock, price, product_id))
                inventory_manager.conn.commit()
                print("Ürün başarıyla güncellendi.")
            except Exception as e:
                print(f"Hata: {e}")

        elif choice == "5":
            print("Yönetici menüsünden çıkılıyor...")
            break
        else:
            print("Geçersiz seçim.")


# Kullanıcıya özel müşteri nesnelerini saklamak için bir sözlük
CUSTOMER_OBJECTS = {}

def customer_menu(inventory_manager, username, email):
    print(f"\n--- Hoşgeldiniz, {username}! ---")
    if username not in CUSTOMER_OBJECTS:
        CUSTOMER_OBJECTS[username] = Customer(customer_id=1, name=username, surname="", phone_number="", email=email, order_history=[], address="adres")
    customer = CUSTOMER_OBJECTS[username]
    order_factory = OrderFactory()
    while True:
        print("\n1. Ürünleri Listele")
        print("2. Kategoriye Göre Filtrele")
        print("3. Sipariş Oluştur")
        print("4. Sipariş Geçmişi Göster")
        print("5. Çıkış")
        secim = input("Seçiminiz: ")
        if secim == "1":
            display_products(inventory_manager)
        elif secim == "2":
            kategori = input("Kategori adı: ")
            urunler = inventory_manager.filter_by_category(kategori)
            for product in urunler:
                print(f"ID: {product.id} | Name: {product.name} | Stock: {product.stock} | Price: ${product.price:.2f}")
        elif secim == "3":
            product_id = int(input("Sipariş vermek istediğiniz ürün ID: "))
            urunler = inventory_manager.list_products()
            selected = [p for p in urunler if p.id == product_id]
            if not selected:
                print("Ürün bulunamadı.")
                continue
            adet = int(input("Kaç adet?: "))
            if selected[0].stock < adet:
                print("Yeterli stok yok!")
                continue
            urgency = input("Aciliyet (high/low): ")
            shipping_method = ShippingSelector.select_best_method(order_weight=adet, urgency=urgency)
            product_list = [selected[0]] * adet
            order = order_factory.create_order(order_id=product_id, customer=customer, products=product_list, status=OrderStatus.PENDING, shipping_method=shipping_method)
            order.attach(customer)
            order.update_status(OrderStatus.SHIPPED)
            print("Sipariş oluşturuldu ve kargo seçildi.")
        elif secim == "4":
            # Sipariş geçmişini veritabanından çek ve göster
            orders = order_factory.get_orders_by_customer(username)
            if not orders:
                print("Sipariş geçmişiniz yok.")
            else:
                print("Sipariş Geçmişiniz:")
                for i, (oid, products, status, shipping, total) in enumerate(orders, 1):
                    print(f"{i}. Sipariş ID: {oid} | Ürünler: {products} | Durum: {status} | Kargo: {shipping} | Toplam: {total}")
        elif secim == "5":
            break
        else:
            print("Geçersiz seçim.")


def main():

    inventory_manager = ProductManager()
    username, role, mail = login()

    if not username:
        return
    
    if role == "manager":
        manager_menu(inventory_manager)
    elif role == "customer":
        customer_menu(inventory_manager, username, mail)


if __name__ == "__main__":

    main()