import json
import os

DATA_FILE = "stock.json"


def load_inventory():
    """Loads inventory from JSON file if it exists, otherwise returns empty dict."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Data file corrupted. Starting with empty inventory.")
    return {}


def save_inventory(inventory):
    """Saves current inventory to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(inventory, f, indent=4)


def add_or_update_item(inventory):
    """Adds a new item or updates an existing item's metadata."""
    item_id = input("Enter Item ID/SKU: ").strip().upper()
    if not item_id:
        print("Item ID cannot be empty.")
        return

    name = input("Enter Item Name: ").strip()
    try:
        quantity = int(input("Enter Initial Quantity: "))
        min_threshold = int(input("Enter Minimum Safety Stock Threshold: "))
        unit_price = float(input("Enter Unit Price ($): "))
    except ValueError:
        print("Invalid numerical input. Operation cancelled.")
        return

    inventory[item_id] = {
        "name": name,
        "quantity": quantity,
        "min_threshold": min_threshold,
        "unit_price": unit_price,
    }
    save_inventory(inventory)
    print(f"Success: '{name}' (SKU: {item_id}) saved.")


def update_stock_quantity(inventory, mode="add"):
    """Adjusts stock levels (adding restock or removing sales)."""
    item_id = input("Enter Item ID/SKU: ").strip().upper()
    if item_id not in inventory:
        print("Item not found in inventory.")
        return

    item = inventory[item_id]
    try:
        qty = int(input(f"Enter quantity to {'add' if mode == 'add' else 'remove'}: "))
        if qty <= 0:
            print("Quantity must be greater than 0.")
            return
    except ValueError:
        print("Invalid quantity. Operation cancelled.")
        return

    if mode == "add":
        item["quantity"] += qty
        print(f"Added {qty} units. New total for '{item['name']}': {item['quantity']}")
    else:
        if qty > item["quantity"]:
            print(f"Insufficient stock! Current quantity: {item['quantity']}")
            return
        item["quantity"] -= qty
        print(f"Removed {qty} units. Remaining total for '{item['name']}': {item['quantity']}")

    save_inventory(inventory)


def display_inventory(inventory):
    """Displays formatted view of inventory and flags low-stock items."""
    if not inventory:
        print("\nInventory is currently empty.")
        return

    print("\n" + "=" * 70)
    print(f"{'SKU':<10} | {'Name':<20} | {'Qty':<8} | {'Min Limit':<10} | {'Price':<8} | {'Status'}")
    print("-" * 70)

    total_value = 0.0
    for item_id, details in inventory.items():
        qty = details["quantity"]
        min_lim = details["min_threshold"]
        price = details["unit_price"]
        status = "LOW STOCK!" if qty <= min_lim else "OK"
        total_value += qty * price

        print(
            f"{item_id:<10} | {details['name']:<20} | {qty:<8} | {min_lim:<10} | ${price:<7.2f} | {status}"
        )

    print("=" * 70)
    print(f"Total Inventory Value: ${total_value:,.2f}\n")


def search_item(inventory):
    """Search for a specific item by SKU or name keyword."""
    query = input("Enter Item SKU or Name keyword to search: ").strip().lower()
    found = False

    for item_id, details in inventory.items():
        if query in item_id.lower() or query in details["name"].lower():
            print(f"\n[SKU: {item_id}]")
            print(f"  Name:       {details['name']}")
            print(f"  Quantity:   {details['quantity']}")
            print(f"  Min Limit:  {details['min_threshold']}")
            print(f"  Unit Price: ${details['unit_price']:.2f}")
            found = True

    if not found:
        print("No matching items found.")


def main():
    inventory = load_inventory()

    while True:
        print("\n--- WAREHOUSE STOCK TRACKER ---")
        print("1. View All Stock & Status")
        print("2. Add New Item")
        print("3. Receive Stock (Restock)")
        print("4. Remove Stock (Ship/Sell)")
        print("5. Search Item")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            display_inventory(inventory)
        elif choice == "2":
            add_or_update_item(inventory)
        elif choice == "3":
            update_stock_quantity(inventory, mode="add")
        elif choice == "4":
            update_stock_quantity(inventory, mode="remove")
        elif choice == "5":
            search_item(inventory)
        elif choice == "6":
            print("Exiting Stock Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 through 6.")


if __name__ == "__main__":
    main()