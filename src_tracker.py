class WarehouseTracker:

    def __init__(self, storage):
        self.storage = storage
        self.inventory = self.storage.load()

    def add_item(self, sku, name, quantity, min_threshold, unit_price):
        """Adds or updates an item in the inventory."""
        sku = sku.strip().upper()
        if not sku:
            raise ValueError("SKU cannot be empty.")

        self.inventory[sku] = {
            "name": name,
            "quantity": int(quantity),
            "min_threshold": int(min_threshold),
            "unit_price": float(unit_price),
        }
        self.storage.save(self.inventory)
        return self.inventory[sku]

    def adjust_stock(self, sku, quantity, operation="add"):
        """Increments or decrements stock for a given SKU."""
        sku = sku.strip().upper()
        if sku not in self.inventory:
            raise KeyError(f"SKU '{sku}' not found in inventory.")

        qty = int(quantity)
        if qty <= 0:
            raise ValueError("Adjustment quantity must be greater than zero.")

        item = self.inventory[sku]
        if operation == "add":
            item["quantity"] += qty
        elif operation == "remove":
            if qty > item["quantity"]:
                raise ValueError(
                    f"Insufficient stock! Available: {item['quantity']}"
                )
            item["quantity"] -= qty

        self.storage.save(self.inventory)
        return item["quantity"]

    def get_low_stock_items(self):
        """Returns items that are at or below their safety threshold."""
        return {
            sku: details
            for sku, details in self.inventory.items()
            if details["quantity"] <= details["min_threshold"]
        }

    def get_total_value(self):
        """Calculates total dollar value of current inventory."""
        return sum(
            item["quantity"] * item["unit_price"]
            for item in self.inventory.values()
        )