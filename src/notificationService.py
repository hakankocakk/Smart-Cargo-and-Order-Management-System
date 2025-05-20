class NotificationService: #Ayrı class olarak yazmadım böyle daha açık geldi
    def __init__(self, notification_type: str):
        self.notification_type = notification_type

    def sendEmail(self, customer_email: str, message: str):
        """Sends an email notification."""
        print(f"Email to {customer_email}: {message}")

    def sendSMS(self, customer_phone: str, message: str):
        """Sends an SMS notification."""
        print(f"SMS to {customer_phone}: {message}")

    def send_notification(self, customer_contact: str, message: str):
        """Sends a notification based on the notification_type."""
        if self.notification_type == "email":
            self.sendEmail(customer_contact, message)
        elif self.notification_type == "sms":
            self.sendSMS(customer_contact, message)
        else:
            print(f"Notification to {customer_contact} ({self.notification_type}): {message}")

