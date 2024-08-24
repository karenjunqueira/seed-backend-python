from repositories.item_mongo_repository import ItemMongoRepository
from models.item import Item

class ItemService():
    def __init__(self):
        self.repository = ItemMongoRepository()

    def create_item(self, item):
        return self.repository.create(item)

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def get_all(self):
        return self.repository.get_all()

    def update_item(self, id, item):
        return self.repository.update(id, item)

    def delete_item(self, id):
        return self.repository.delete(id)