from enum import Enum

class OrderStatus(Enum):
    """
    Siparişin mevcut durumunu temsil eden sabit değerler (enum) kümesi.
    Bir siparişin yaşam döngüsü boyunca alabileceği farklı aşamaları tanımlar.
    """
    PREPARING = "Preparing"
    """
    Siparişin hazırlanmakta olduğunu gösteren durum.
    Bu aşamada ürünler toplanır ve paketlenir.
    """
    SHIPPED   = "Shipped"
    """
    Siparişin kargoya verildiğini ve yolda olduğunu gösteren durum.
    Bu aşamada sipariş lojistik firmasına teslim edilmiştir.
    """
    DELIVERED = "Delivered"
    """
    Siparişin müşteriye başarıyla teslim edildiğini gösteren durum.
    Bu, siparişin son aşamasıdır.
    """
