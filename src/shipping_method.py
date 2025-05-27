from abc import ABC, abstractmethod
class ShippingMethod(ABC):
    """
    Nakliye yöntemleri için soyut temel class.
    Tüm somut nakliye yöntemlerinin uygulaması gereken 'calculateCost' metodunu tanımlar.
    Bu, farklı nakliye seçenekleri arasında tutarlı bir arayüz sağlar ve **Strateji Deseni**'nin
    arayüzünü (Strategy Interface) temsil eder.
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
    Hizli nakliye yöntemini temsil eder.
    Bu yöntem, daha yüksek bir maliyetle hizli teslimat sağlar ve **Strateji Deseni**'nin
    somut bir stratejisini (Concrete Strategy) oluşturur.
    """
    def calculateCost(self):
        """
        Hızlı nakliye maliyetini hesaplar.

        Returns:
            float: Sabit hizli nakliye maliyeti (20.0).
        """
        return 20.0
class CheapShipping(ShippingMethod):
    """
    Ucuz nakliye yöntemini temsil eder.
    Bu yöntem, düşük bir maliyetle standart teslimat sağlar ve **Strateji Deseni**'nin
    somut bir stratejisini (Concrete Strategy) oluşturur.
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
    Bu yöntem, belirli durumlar için yüksek maliyetli ancak hizli bir teslimat sağlar ve
    **Strateji Deseni**'nin somut bir stratejisini (Concrete Strategy) oluşturur.
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
    Uygun nakliye yöntemini seçmek için kullanilan yardimci class.
    Bu class, verilen siparişin ağirliği ve aciliyetine göre en iyi nakliye yöntemini belirler.
    
    Bu class'in `select_best_method` statik metodu, koşullara göre farkli 'ShippingMethod'
    nesneleri oluşturarak **Basit Fabrika (Simple Factory) deseni**ni uygular.
    Bu sayede, istemci kodunun hangi somut nakliye classinin kullanacağini bilmesine gerek kalmaz.
    """
    @staticmethod
    def select_best_method(order_weight, urgency):
        """
        Verilen sipariş ağirliği ve aciliyetine göre en uygun nakliye yöntemini seçer.
        Bu, bir fabrika (factory) desenine benzer şekilde, belirli koşullara göre farklı
        nakliye stratejilerini döndürür.

        Args:
            order_weight (float): Siparişin ağirliği.
            urgency (str): Siparişin aciliyet seviyesi ('high' veya diğer).

        Returns:
            ShippingMethod: Seçilen nakliye yöntemini temsil eden bir ShippingMethod nesnesi.
        """
        if urgency == 'high':
            return FastShipping()
        elif order_weight < 2:
            return DroneShipping()
        else:
            return CheapShipping()    