from abc import ABC, abstractmethod
class ShippingMethod(ABC):
    @abstractmethod
    def calculateCoat(self):
        pass

class FastShipping(ShippingMethod):
    def calculateCoat(self):
        return 20.0
class CheapShipping(ShippingMethod):
    def calculateCoat(self):
        return 5.0
class DroneShipping(ShippingMethod):
    def calculateCoat(self):
        return 50.0

class ShippingSelector:
    @staticmethod
    def select_best_method(order_weight, urgency):
        # Basit örnek: ağırlık ve aciliyet ile seçim
        if urgency == 'high':
            return FastShipping()
        elif order_weight < 2:
            return DroneShipping()
        else:
            return CheapShipping()    