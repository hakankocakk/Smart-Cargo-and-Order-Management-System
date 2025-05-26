# Observer Pattern for order status notifications
class Observer:
    """
    Observer (Gözlemci) arayüzünü temsil eder.
    Bir Subject (Konu) nesnesinden güncellemeler almak isteyen tüm somut gözlemcilerin
    bu arayüzü uygulaması beklenir.
    """
    def update(self, message):
        """
        Subject'ten (Konu) bir bildirim alindiğinda çağrilan soyut metod.
        Somut gözlemciler bu metodu kendi bildirim işleme mantiklarini uygulamak için override etmelidir.

        Args:
            message (any): Subject'ten gelen bildirim mesaji veya veri.
        """
        pass

class Subject:
    """
    Subject (Konu) classini temsil eder.
    Bu class, gözlemcilerin kendisine kaydolmasina (attach) veya kaydini silmesine (detach) izin verir.
    Durumu değiştiğinde, kayitli tüm gözlemcilerine bir bildirim (notify) gönderir.
    """
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """
        Bir gözlemci nesnesini bu Subject'e ekler.
        Artik bu gözlemci, Subject'ten bildirimler alacaktir.

        Args:
            observer (Observer): Eklenecek gözlemci nesnesi.
        """
        self._observers.append(observer)

    def detach(self, observer):
        """
        Bir gözlemci nesnesini bu Subject'ten çıkarır.
        Bu gözlemci artik Subject'ten bildirim almayacaktır.

        Args:
            observer (Observer): Çikarilacak gözlemci nesnesi.
        """
        self._observers.remove(observer)

    def notify(self, message):
        """
        Tüm kayitli gözlemcilere bir bildirim mesaji gönderir.
        Genellikle Subject'in durumunda bir değişiklik olduğunda çağrilir.

        Args:
            message (str): Gözlemcilere gönderilecek bildirim mesaji.
        """
        for observer in self._observers:
            observer.update(message)