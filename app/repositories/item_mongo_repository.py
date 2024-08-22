from typing import Optional
from models.item import Item 
from repositories.mongo.base_mongo_repository import BaseMongoRepository

DATABASE_NAME = "python_seed_db"
COLLECTION_NAME = "item"

class ItemMongoRepository(BaseMongoRepository[Item]):
    def __init__(self):
        super().__init__(database_name=DATABASE_NAME, collection_name=COLLECTION_NAME, model=Item)