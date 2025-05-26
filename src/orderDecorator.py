       
def logOrderCreation(func):
    """
    Bu bir dekoratör fonksiyonudur. Bir siparişin oluşturulması sürecini loglamak (kaydetmek) için kullanılır.
    Dekore edilen fonksiyon çağrılmadan önce "Order is being created...." mesajını yazdırır
    ve fonksiyonun çalışması tamamlandıktan sonra oluşturulan siparişin ID'sini ekrana basar.
    Bu, sipariş oluşturma işlemlerinin izlenmesine yardımcı olur.

    Args:
        func (function): Dekore edilecek (genellikle bir sınıf metodu olan) fonksiyon.
                        Bu fonksiyonun bir sipariş nesnesi döndürmesi ve bu nesnenin 'id' niteliğine sahip olması beklenir.

    Returns:
        function: Dekore edilmiş fonksiyonun sarmalayıcı (wrapper) versiyonu.
    """

    def wrapper(self, *args, **kwargs):
        """
        Dekore edilen fonksiyonu sarmalayan iç fonksiyondur.
        Sipariş oluşturma öncesi ve sonrası log mesajlarını ekrana yazdırır.

        Args:
            self: Metodun ait olduğu sınıfın örneği (örneğin, OrderManager sınıfının bir örneği).
            *args: Dekore edilen fonksiyona geçirilen konumlu argümanlar.
            **kwargs: Dekore edilen fonksiyona geçirilen anahtar kelime argümanları.

        Returns:
            object: Dekore edilen fonksiyonun döndürdüğü sonuç (genellikle oluşturulan sipariş nesnesi).
        """
        print(" Order is being created....")
        result = func(self, *args, **kwargs)
        print(f"Order created with ID: {result.id}")
        return result
    return wrapper
