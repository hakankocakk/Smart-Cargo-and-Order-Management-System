from abc import ABC, abstractmethod
class ShippingMethod(ABC):
    """
    Nakliye yöntemleri için soyut temel sınıf.
    Tüm somut nakliye yöntemlerinin uygulaması gereken 'calculateCost' metodunu tanımlar.
    Bu, farklı nakliye seçenekleri arasında tutarlı bir arayüz sağlar.
    """
    @abstractmethod
    def calculateCost(self):
        """
        abstractmethod: Nakliye maliyetini hesaplar.
        Bu metodun her somut alt sınıf tarafından uygulanması zorunludur.

        Returns:
            float: Nakliye maliyeti.
        """
        pass

class FastShipping(ShippingMethod):
    """
    Hızlı nakliye yöntemini temsil eder.
    Bu yöntem, daha yüksek bir maliyetle hızlı teslimat sağlar.
    """
    def calculateCost(self):
        """
        Hızlı nakliye maliyetini hesaplar.

        Returns:
            float: Sabit hızlı nakliye maliyeti (20.0).
        """
        return 20.0
class CheapShipping(ShippingMethod):
    """
    Ucuz nakliye yöntemini temsil eder.
    Bu yöntem, düşük bir maliyetle standart teslimat sağlar.
    """
    def calculateCost(self):
        """
        Ucuz nakliye maliyetini hesaplar.

        Returns:
            float: Sabit ucuz nakliye maliyeti (5.0).
        """
        return 5.0
class DroneShipping(ShippingMethod):
    """
    Drone ile nakliye yöntemini temsil eder.
    Bu yöntem, belirli durumlar için yüksek maliyetli ancak hızlı bir teslimat sağlar.
    """
    def calculateCost(self):
        """
        Drone ile nakliye maliyetini hesaplar.

        Returns:
            float: Sabit drone nakliye maliyeti (50.0).
        """
        return 50.0

class ShippingSelector:
    """
    Uygun nakliye yöntemini seçmek için kullanılan yardımcı sınıf.
    Bu sınıf, verilen siparişin ağırlığı ve aciliyetine göre en iyi nakliye yöntemini belirler.
    """
    @staticmethod
    def select_best_method(order_weight, urgency):
        """
        Verilen sipariş ağırlığı ve aciliyetine göre en uygun nakliye yöntemini seçer.
        Bu, bir fabrika (factory) desenine benzer şekilde, belirli koşullara göre farklı
        nakliye stratejilerini döndürür.

        Args:
            order_weight (float): Siparişin ağırlığı.
            urgency (str): Siparişin aciliyet seviyesi ('high' veya diğer).

        Returns:
            ShippingMethod: Seçilen nakliye yöntemini temsil eden bir ShippingMethod nesnesi.
        """
        # Basit örnek: ağırlık ve aciliyet ile seçim
        if urgency == 'high':
            return FastShipping()
        elif order_weight < 2:
            return DroneShipping()
        else:
            return CheapShipping()    