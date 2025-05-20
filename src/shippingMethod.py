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