# controllers/inventory_controller.py
from models.inventory import InventoryModel

class InventoryController:
    def search(self, name, category):
        return InventoryModel.search(name, category)

    def all(self):
        return InventoryModel.all()

    def add(self, name, category, quantity, status="available"):
        InventoryModel.add(name, category, quantity, status)

    def update(self, inv_id, name=None, category=None, quantity=None, status=None):
        InventoryModel.update(inv_id, name, category, quantity, status)

    def delete(self, inv_id):
        InventoryModel.delete(inv_id)
