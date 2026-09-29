import json
import os


class InventoryStorage:

    def __init__(self, filepath="stock.json"):
        self.filepath = filepath

    def load(self):
        """Loads inventory data from local JSON file."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save(self, data):
        """Saves current inventory dictionary to local JSON file."""
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)