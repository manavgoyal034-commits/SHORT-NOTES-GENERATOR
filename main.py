from src.storage import InventoryStorage
from src.tracker import WarehouseTracker


def main():
    storage = InventoryStorage("stock.json")
    tracker = WarehouseTracker(storage)

    while True:
        print("\n=== WAREHOUSE STOCK TRACKER ===")
        print("1. View Inventory")
        print("2. Add / Update Item")
        print("3. Receive Stock (Restock)")
        print("4. Ship/Sell Stock")
        print("5. View Low Stock Alerts")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            print("\n" + "=" * 70)
            print(
                f"{'SKU':<10} | {'Name':<20} | {'Qty':<8} | {'Min Limit':<10} | {'Price':<8} | {'Status'}"
            )
            print("-" * 70)
            for sku, details in tracker.inventory.items():
                status = (
                    "LOW STOCK!"
                    if details["quantity"] <= details["min_threshold"]
                    else "OK"
                )
                print(
                    f"{sku:<10} | {details['name']:<20} | {details['quantity']:<8} | {details['min_threshold']:<10} | ${details['unit_price']:<7.2f} | {status}"
                )
            print("=" * 70)
            print(
                f"Total Inventory Value: ${tracker.get_total_value():,.2f}\n"
            )

        elif choice == "2":
            try:
                sku = input("Enter SKU: ")
                name = input("Enter Item Name: ")
                qty = int(input("Enter Initial Quantity: "))
                min_t = int(input("Enter Minimum Safety Threshold: "))
                price = float(input("Enter Unit Price ($): "))
                tracker.add_item(sku, name, qty, min_t, price)
                print(f"Success: Item '{name}' saved.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            try:
                sku = input("Enter SKU: ")
                qty = int(input("Quantity received: "))
                new_qty = tracker.adjust_stock(sku, qty, operation="add")
                print(f"Restocked successfully. New balance: {new_qty}")
            except (KeyError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "4":
            try:
                sku = input("Enter SKU: ")
                qty = int(input("Quantity removed: "))
                new_qty = tracker.adjust_stock(sku, qty, operation="remove")
                print(f"Removed successfully. Remaining balance: {new_qty}")
            except (KeyError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "5":
            low_stock = tracker.get_low_stock_items()
            if not low_stock:
                print("\nAll items are at healthy stock levels!")
            else:
                print("\n--- LOW STOCK ALERTS ---")
                for sku, details in low_stock.items():
                    print(
                        f"SKU: {sku} | Name: {details['name']} | Current: {details['quantity']} | Min Threshold: {details['min_threshold']}"
                    )

        elif choice == "6":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()