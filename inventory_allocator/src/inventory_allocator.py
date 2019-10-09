class InventoryAllocator:
    """This class is used to determine the most cost-effective shipment
     given an order and an inventory distribution"""

    def __init__(self, order, warehouse_to_inventory):
        assert isinstance(order, dict), "Order must be a dictionary"
        assert isinstance(warehouse_to_inventory, list), "Inventory distribution must be a list"
        self.order = order
        self.warehouse_to_inventory = warehouse_to_inventory
        self.cheapest_shipment = list()

    def get_order(self):
        """Returns the order being placed"""
        return self.order

    def get_inventory_distribution(self):
        """Returns the current inventory distribution"""
        return self.warehouse_to_inventory

    def get_cheapest_shipment(self):
        """Returns the most cost-effective shipment"""
        return self.cheapest_shipment

    def complete_order(self):
        """Calculates the most cost-effective shipment"""
        # Sanity checks
        assert self.get_order() is not None and self.get_order() != {}, "Missing order"
        assert self.get_inventory_distribution() is not None \
               and self.get_inventory_distribution() != [], "Missing inventory distribution"

        # Examine each warehouse, and try to fulfill as much of the order as you can
        for warehouse in self.warehouse_to_inventory:
            warehouse_ship_info = dict()
            items_to_ship = dict()
            for item in self.order.keys():
                if item in warehouse["inventory"].keys() and self.order[item] > 0 \
                        and warehouse["inventory"][item] > 0:
                    amount_to_order = self.order[item]
                    amount_in_stock = warehouse["inventory"][item]
                    if amount_to_order <= amount_in_stock:
                        items_to_ship[item] = amount_to_order
                        warehouse["inventory"][item] -= amount_to_order
                        self.order[item] -= amount_to_order
                    else:
                        items_to_ship[item] = amount_in_stock
                        warehouse["inventory"][item] = 0
                        self.order[item] -= amount_in_stock
            if items_to_ship != {}:
                warehouse_ship_info[warehouse["name"]] = items_to_ship
                self.cheapest_shipment.append(warehouse_ship_info)

        # See if any items in the order were not completely allocated for
        array_zeroes = [0] * len(self.get_order().values())
        if list(self.get_order().values()) != array_zeroes:
            self.cheapest_shipment = list()
        return self.cheapest_shipment
