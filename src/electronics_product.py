from src.product import Product

class ElectronicsProduct(Product):
    def __init__(self, id: int, name: str, stock: int, price: float, warranty_years: int):
        super().__init__(id, name, "Electronics", stock, price)
        self.warranty_years = warranty_years

    def __repr__(self):
        return f"<ElectronicsProduct id={self.id} name='{self.name}' stock={self.stock} warranty={self.warranty_years} years>"

    def get_warranty_info(self):
        return f"{self.warranty_years} yıl garanti."