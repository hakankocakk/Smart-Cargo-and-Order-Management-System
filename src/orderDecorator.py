       
def logOrderCreation(func):
    def wrapper(self, *args, **kwargs):
        print(" Order is being created....")
        result = func(self, *args, **kwargs)
        print(f"Order created with ID: {self.id}")
        return result
    return wrapper
#argüman sayısı sabitse args kwargs yazmayız parametreleri yazarız ama böylesi daha güvenli
#orderı yazan kişi classı tanımladıktan hemen sonra @loOrderCreation yazacak.