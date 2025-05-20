from enum import Enum

class OrderStatus(Enum):
    PREPARING = "Preparing"
    SHIPPED   = "Shipped"
    DELIVERED = "Delivered"