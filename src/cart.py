class Cart:
    def __init__(self):
        self.items = []  # Each item: (Product, quantity)

    def add(self, product, quantity):
        # If product already in cart, increase quantity
        for i, (p, q) in enumerate(self.items):
            if p.id == product.id:
                self.items[i] = (p, q + quantity)
                return
        self.items.append((product, quantity))

    def is_empty(self):
        return len(self.items) == 0

    def clear(self):
        self.items = []

    def total_items(self):
        return sum(q for _, q in self.items)

    def get_products(self):
        result = []
        for product, quantity in self.items:
            result.extend([product] * quantity)
        return result

    def __iter__(self):
        return iter(self.items)