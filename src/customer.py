from src.observer import Observer

class Customer(Observer):
    """
    Customer class'ı, Observer arayüzünü uygulayarak bildirim alabilen bir gözlemci görevi görür.
    Müşterinin kimlik, isim, iletişim bilgileri, sipariş geçmişi ve adres gibi özelliklerini yönetir.
    """
    def __init__(self, customer_id, name, surname,phone_number, email, order_history, address):
        """
        Customer nesnesini başlatır.

        Args:
            customer_id (str): Müşterinin benzersiz kimliği.
            name (str): Müşterinin adı.
            surname (str): Müşterinin soyadı.
            phone_number (str): Müşterinin telefon numarası.
            email (str): Müşterinin e-posta adresi.
            order_history (list): Müşterinin sipariş geçmişini tutan liste.
            address (str): Müşterinin adresi.
        """
        self.__customer_id = customer_id
        self.name = name
        self.surname = surname
        self.__phone_number = phone_number
        self.__email = email
        self.__order_history = order_history
        self.__address = address

    def get_customer_id(self):
        """
        Müşterinin kimliğini döndürür.(Attribute private olduğu için)

        Returns:
            str: Müşterinin kimliği.
        """
        return self.__customer_id
    
    def get_phone_number(self):
        """
        Müşterinin telefon numarasını döndürür.(Attribute private olduğu için)

        Returns:
            str: Müşterinin telefon numarası.
        """
        return self.__phone_number
    
    def get_email(self):
        """
        Müşterinin e-posta adresini döndürür.(Attribute private olduğu için)

        Returns:
            str: Müşterinin e-posta adresi.
        """
        return self.__email
    
    def get_order_history(self):
        """
        Müşterinin sipariş geçmişini döndürür.(Attribute private olduğu için)

        Returns:
            list: Müşterinin sipariş geçmişini içeren liste.
        """
        return self.__order_history
    
    def get_address(self):
        """
        Müşterinin adresini döndürür.(Attribute private olduğu için)

        Returns:
            str: Müşterinin adresi.
        """
        return self.__address
    
    def update(self, message):
        """
        Observer arayüzünün bir parçasıdır. Subject (konu) tarafından bir bildirim geldiğinde çağrılır.
        Bu metot, müşteriye gelen mesajı ekrana yazdırır.

        Args:
            message (str): Gelen bildirim mesajı.
        """
        print(f"\nNotification for {self.name} {self.surname}: {message}")

    def update_address(self, new_address):
        """
        Müşterinin adresini günceller ve güncellenen adresi ekrana yazdırır.

        Args:
            new_address (str): Yeni adres bilgisi.
        """
        self.__address = new_address
        print(f"Address has been updated: {new_address}")

    def add_order(self, order):
        """
        Müşterinin sipariş geçmişine yeni bir sipariş ekler ve eklenen siparişi ekrana yazdırır.

        Args:
            order (str): Eklenecek sipariş bilgisi.
        """
        self.__order_history.append(order)
        print(f"New order has been added: {order}")

    def print_order_history(self):
        """
        Müşterinin tüm sipariş geçmişini numaralandırılmış bir liste halinde ekrana yazdırır.
        """
        print("Order History: ")
        for i, order in enumerate(self.__order_history, 1):
            print(f"{i} . {order}")

    def print_summary(self):
        """
        Müşterinin tüm bilgilerini (kimlik, ad, soyad, telefon, e-posta, adres ve sipariş sayısı)
        özet halinde ekrana yazdırır.
        """
        print(f"Customer ID: {self.__customer_id}")
        print(f"Full Name: {self.name} {self.surname}")
        print(f"Telephone: {self.__phone_number}")
        print(f"Email: {self.__email}")
        print(f"Addres: {self.__address}")
        print(f"Order Count: {len(self.__order_history)}")
