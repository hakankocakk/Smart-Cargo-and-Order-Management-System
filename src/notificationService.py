class NotificationService:
    """
    Bu class, farkli türde bildirimler (e-posta, SMS) göndermek için kullanilir.
    Kullanicinin tercihine göre belirli bir bildirim türünü kullanarak mesaj iletimini sağlar.

    Attributes:
        notification_type (str): Servis tarafindan kullanilacak varsayilan bildirim tipi
                                 ("email", "sms" veya diğer özel tipler olabilir).
    """
    def __init__(self, notification_type: str):
        self.notification_type = notification_type

    def sendEmail(self, customer_email: str, message: str):
        """
        Belirtilen e-posta adresine bir e-posta bildirimi gönderir.

        Args:
            customer_email (str): Bildirimin gönderileceği müşterinin e-posta adresi.
            message (str): Gönderilecek e-posta mesajinin içeriği.
        """
        print(f"Email to {customer_email}: {message}")

    def sendSMS(self, customer_phone: str, message: str):
        """
        Belirtilen telefon numarasina bir SMS bildirimi gönderir.

        Args:
            customer_phone (str): Bildirimin gönderileceği müşterinin telefon numarası.
            message (str): Gönderilecek SMS mesajinin içeriği.
        """
        print(f"SMS to {customer_phone}: {message}")

    def send_notification(self, customer_contact: str, message: str):
        """
        'notification_type' özelliğine göre uygun bildirim metodunu çağirarak
        bir bildirim gönderir. Eğer bilinen bir tip değilse, genel bir mesaj yazdirir.

        Args:
            customer_contact (str): Müşterinin iletişim bilgisi (e-posta adresi veya telefon numarasi).
            message (str): Gönderilecek bildirim mesajinin içeriği.
        """
        if self.notification_type == "email":
            self.sendEmail(customer_contact, message)
        elif self.notification_type == "sms":
            self.sendSMS(customer_contact, message)
        else:
            print(f"Notification to {customer_contact} ({self.notification_type}): {message}")

