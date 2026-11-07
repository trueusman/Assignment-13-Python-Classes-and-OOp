"""Task 15: Integrated order fulfillment system with rollback and unit tests."""

import json
import os
import tempfile
import unittest
import uuid

class Product:
    def __init__(self, product_id, name, price, stock):
        if price < 0 or stock < 0:
            raise ValueError("Price and stock cannot be negative")
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

class Inventory:
    def __init__(self, products):
        self.products = {p.product_id: p for p in products}

    def validate(self, items):
        for product_id, quantity in items.items():
            if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
                raise ValueError("Quantities must be positive integers")
            if product_id not in self.products:
                raise ValueError(f"Unknown product: {product_id}")
            if self.products[product_id].stock < quantity:
                raise ValueError(f"Out of stock: {product_id}")

    def reduce_stock(self, items):
        self.validate(items)
        for product_id, quantity in items.items():
            self.products[product_id].stock -= quantity

class Cart:
    def __init__(self):
        self.items = {}

    def add(self, product_id, quantity):
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        self.items[product_id] = self.items.get(product_id, 0) + quantity

    def total(self, inventory, discount_percent=0):
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        subtotal = 0
        for product_id, quantity in self.items.items():
            if product_id not in inventory.products:
                raise ValueError(f"Unknown product: {product_id}")
            subtotal += inventory.products[product_id].price * quantity
        return subtotal * (1 - discount_percent / 100)

class Order:
    def __init__(self, items, total):
        self.order_id = str(uuid.uuid4())
        self.items = dict(items)
        self.total = round(total, 2)

    def to_dict(self):
        return {"order_id": self.order_id, "items": self.items, "total": self.total}

def load_catalog(path):
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
    return Inventory([
        Product(row["product_id"], row["name"], row["price"], row["stock"])
        for row in data
    ])

def place_order(cart, inventory, discount_percent, orders_path="orders.json"):
    # Validate all items before mutating stock.
    inventory.validate(cart.items)
    total = cart.total(inventory, discount_percent)
    order = Order(cart.items, total)

    old_stock = {pid: inventory.products[pid].stock for pid in cart.items}
    old_bytes = None
    if os.path.exists(orders_path):
        with open(orders_path, "rb") as file:
            old_bytes = file.read()

    try:
        inventory.reduce_stock(cart.items)
        existing = []
        if old_bytes:
            existing = json.loads(old_bytes.decode("utf-8"))
        existing.append(order.to_dict())

        directory = os.path.dirname(os.path.abspath(orders_path))
        fd, temp_path = tempfile.mkstemp(dir=directory, text=True)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                json.dump(existing, file, indent=4)
            os.replace(temp_path, orders_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    except Exception:
        for pid, stock in old_stock.items():
            inventory.products[pid].stock = stock
        raise

    return order

class OrderSystemTests(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory([Product("P1", "Pen", 100, 5)])
        self.cart = Cart()
        self.cart.add("P1", 2)
        self.temp_dir = tempfile.TemporaryDirectory()
        self.orders_path = os.path.join(self.temp_dir.name, "orders.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_discounted_total(self):
        self.assertEqual(self.cart.total(self.inventory, 10), 180)

    def test_stock_reduced_after_order(self):
        place_order(self.cart, self.inventory, 10, self.orders_path)
        self.assertEqual(self.inventory.products["P1"].stock, 3)

    def test_out_of_stock_rejected_without_stock_change(self):
        self.cart.items["P1"] = 99
        with self.assertRaises(ValueError):
            place_order(self.cart, self.inventory, 0, self.orders_path)
        self.assertEqual(self.inventory.products["P1"].stock, 5)

if __name__ == "__main__":
    # Run: python3 task_15.py
    unittest.main()
