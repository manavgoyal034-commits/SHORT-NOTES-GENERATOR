import os
import pytest
from src.storage import InventoryStorage
from src.tracker import WarehouseTracker

TEST_DB = "test_stock.json"


@pytest.fixture
def tracker():
    storage = InventoryStorage(TEST_DB)
    tracker_instance = WarehouseTracker(storage)
    yield tracker_instance
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_add_item(tracker):
    item = tracker.add_item("SKU100", "Widget", 50, 10, 12.50)
    assert item["name"] == "Widget"
    assert "SKU100" in tracker.inventory


def test_adjust_stock_add(tracker):
    tracker.add_item("SKU100", "Widget", 50, 10, 12.50)
    new_qty = tracker.adjust_stock("SKU100", 20, operation="add")
    assert new_qty == 70


def test_adjust_stock_remove_insufficient(tracker):
    tracker.add_item("SKU100", "Widget", 10, 5, 12.50)
    with pytest.raises(ValueError):
        tracker.adjust_stock("SKU100", 20, operation="remove")


def test_low_stock_detection(tracker):
    tracker.add_item("SKU100", "Widget", 3, 10, 12.50)
    low_stock = tracker.get_low_stock_items()
    assert "SKU100" in low_stock


def test_total_inventory_value(tracker):
    tracker.add_item("SKU1", "Item 1", 10, 2, 5.00)
    tracker.add_item("SKU2", "Item 2", 5, 1, 10.00)
    assert tracker.get_total_value() == 100.00