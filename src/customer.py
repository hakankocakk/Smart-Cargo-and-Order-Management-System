from src.observer import Observer

class Customer(Observer):
    def __init__(self, customer_id, name, surname,phone_number, email, order_history, address):
        self.__customer_id = customer_id
        self.name = name
        self.surname = surname
        self.__phone_number = phone_number
        self.__email = email
        self.__order_history= order_history
        self.__address = address

    def get_customer_id(self):
        return self.__customer_id
    
    def get_phone_number(self):
        return self.__phone_number
    
    def get_email(self):
        return self.__email
    
    def get_order_history(self):
        return self.__order_history
    
    def get_address(self):
        return self.__address
    
    def update(self, message):
        print(f"\nNotification for {self.name} {self.surname}: {message}")

    def update_address(self, new_address):
        self.__address = new_address
        print(f"Address has been updated: {new_address}")

    def add_order(self, order):
        self.__order_history.append(order)
        print(f"New order has been added: {order}")

    def print_order_history(self):
        print("Order History: ")
        for i, order in enumerate(self.__order_history, 1):
            print(f"{i} . {order}")

    def print_summary(self):
        print(f"Customer ID: {self.__customer_id}")
        print(f"Full Name: {self.name} {self.surname}")
        print(f"Telephone: {self.__phone_number}")
        print(f"Email: {self.__email}")
        print(f"Addres: {self.__address}")
        print(f"Order Count: {len(self.__order_history)}")
