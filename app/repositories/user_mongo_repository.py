from typing import Optional
from models.user import User 
from repositories.mongo.base_mongo_repository import BaseMongoRepository

DATABASE_NAME = "python_seed_db"
COLLECTION_NAME = "user"

class UserMongoRepository(BaseMongoRepository[User]):
    def __init__(self):
        super().__init__(database_name=DATABASE_NAME, collection_name=COLLECTION_NAME, model=User)