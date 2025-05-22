import sqlite3


class OrderManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OrderManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name="databases/orders.db"):
        if not hasattr(self, 'conn'):
            self.conn = sqlite3.connect(db_name)

    def show_orders(self):
        try:
            cursor = self.conn.execute("SELECT id, products, status, shipping_method, total FROM orders")
            orders = cursor.fetchall()
            for i, (oid, products, status, shipping, total) in enumerate(orders, 1):
                print(f"{i}. Order ID: {oid} | Products: {products} | Status: {status} | Shipping: {shipping} | Total: {total}")
        except Exception as e:
                print(f"Error: {e}")

    def filter_by_order_status(self, status):
        try:
            cursor = self.conn.execute("Select id, products, status, shipping_method, total FROM orders WHERE status = ?", (status,))
            orders = cursor.fetchall()
            for i, (oid, products, status, shipping, total) in enumerate(orders, 1):
                print(f"{i}. Order ID: {oid} | Products: {products} | Status: {status} | Shipping: {shipping} | Total: {total}")
        except Exception as e:
                print(f"Error: {e}")

    def update_by_order_status(self, order_id, status):
        try:
            self.conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
            self.conn.commit()
        except Exception as e:
                print(f"Error: {e}")
         
    
    