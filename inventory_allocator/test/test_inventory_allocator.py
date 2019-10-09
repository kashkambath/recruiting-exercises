import unittest
from inventory_allocator.src.inventory_allocator import InventoryAllocator

class TestSum(unittest.TestCase):

    def test_empty_order_should_err(self):
        order = {}
        inventory_dist = [{"name": "owd", "inventory": {"apple": 5, "orange": 10}},
                          {"name": "dm", "inventory": {"banana": 5, "orange": 10}}]
        i = InventoryAllocator(order, inventory_dist)
        self.assertRaises(AssertionError, lambda: i.complete_order())

    def test_empty_inventory_dist_should_err(self):
        order = {"apple": 5, "banana": 5, "orange": 5}
        inventory_dist = []
        i = InventoryAllocator(order, inventory_dist)
        self.assertRaises(AssertionError, lambda: i.complete_order())

    def test_example_from_spec(self):
        order = {"apple": 5, "banana": 5, "orange": 5}
        inventory_dist = [{"name": "owd", "inventory": {"apple": 5, "orange": 10}},
                          {"name": "dm", "inventory": {"banana": 5, "orange": 10}}]
        i = InventoryAllocator(order, inventory_dist)
        shipment = i.complete_order()
        expected_output = [{"owd": {"apple": 5, "orange": 5}}, {"dm": {"banana": 5}}]
        self.assertEqual(expected_output, shipment, "Example from spec failed")

    def test_exact_inventory_match(self):
        order = {"apple": 1}
        inventory_dist = [{"name": "owd", "inventory": {"apple": 1}}]
        i = InventoryAllocator(order, inventory_dist)
        shipment = i.complete_order()
        expected_output = [{"owd": {"apple": 1}}]
        self.assertEqual(expected_output, shipment, "Exact inventory match failed")

    def test_not_enough_inventory_for_single_item(self):
        order = {"apple": 1}
        inventory_dist = [{"name": "owd", "inventory": {"apple": 0}}]
        i = InventoryAllocator(order, inventory_dist)
        shipment = i.complete_order()
        expected_output = []
        self.assertEqual(expected_output, shipment, "Insufficient inventory failed")

    def test_split_item_across_warehouses(self):
        order = {"apple": 10}
        inventory_dist = [{"name": "owd", "inventory": {"apple": 5}}, {"name": "dm", "inventory": {"apple": 5}}]
        i = InventoryAllocator(order, inventory_dist)
        shipment = i.complete_order()
        expected_output = [{"owd": {"apple": 5}}, {"dm": {"apple": 5}}]
        self.assertEqual(expected_output, shipment, "Split item across warehouses failed")

    def test_split_items_across_warehouses(self):
        order = {"apple": 10, "banana": 15}
        inventory_dist = [{"name": "owd", "inventory": {"apple": 6, "banana": 3}},
                          {"name": "eq", "inventory": {"banana": 7}},
                          {"name": "dm", "inventory": {"apple": 4, "banana": 5}},
                          {"name": "dm", "inventory": {"apple": 8, "banana": 12}}]
        i = InventoryAllocator(order, inventory_dist)
        shipment = i.complete_order()
        expected_output = [{"owd": {"apple": 6, "banana": 3}}, {"eq": {"banana": 7}}, {"dm": {"apple": 4, "banana": 5}}]
        self.assertEqual(expected_output, shipment, "Split items across warehouses failed")

    def test_leave_items_in_warehouses(self):
        order = {"apple": 8, "banana": 7}
        inventory_dist = [{"name": "owd", "inventory": {"apple": 6, "banana": 3}},
                          {"name": "eq", "inventory": {"banana": 7}},
                          {"name": "dm", "inventory": {"apple": 4, "banana": 5}},
                          {"name": "dm", "inventory": {"apple": 8, "banana": 2}}]
        i = InventoryAllocator(order, inventory_dist)
        shipment = i.complete_order()
        expected_output = [{"owd": {"apple": 6, "banana": 3}}, {"eq": {"banana": 4}}, {"dm": {"apple": 2}}]
        self.assertEqual(expected_output, shipment, "Leave items in warehouses failed")

    def test_insufficient_inventory_for_an_item(self):
        order = {"apple": 8, "banana": 20}
        inventory_dist = [{"name": "owd", "inventory": {"apple": 6, "banana": 3}},
                          {"name": "eq", "inventory": {"banana": 7}},
                          {"name": "dm", "inventory": {"apple": 4, "banana": 5}},
                          {"name": "dm", "inventory": {"apple": 8, "banana": 2}}]
        i = InventoryAllocator(order, inventory_dist)
        shipment = i.complete_order()
        expected_output = []
        self.assertEqual(expected_output, shipment, "Leave items in warehouses failed")

    def test_insufficient_inventory_for_multiple_items(self):
        order = {"apple": 8, "banana": 20, "orange": 12}
        inventory_dist = [{"name": "owd", "inventory": {"apple": 6, "banana": 3}},
                          {"name": "eq", "inventory": {"banana": 7, "orange": 10}},
                          {"name": "dm", "inventory": {"apple": 4, "banana": 5}},
                          {"name": "dm", "inventory": {"apple": 8, "banana": 2, "orange": 4}}]
        i = InventoryAllocator(order, inventory_dist)
        shipment = i.complete_order()
        expected_output = []
        self.assertEqual(expected_output, shipment, "Leave items in warehouses failed")


if __name__ == "__main__":
    unittest.main()
