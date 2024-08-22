from typing import TypeVar, Generic, Optional, Type, List
from pydantic import BaseModel
from bson.objectid import ObjectId
from pymongo.collection import Collection
from core.mongodb_client import MongoDBClient

T = TypeVar('T', bound=BaseModel)

class BaseMongoRepository(Generic[T]):
    def __init__(self, database_name: str, collection_name: str, model: Type[T]):
        self._collection: Collection = MongoDBClient.get_collection(database_name, collection_name)
        self._model = model

    def create(self, document: T) -> T:
        document_dict = document.model_dump()
        self._collection.insert_one(document_dict)
        return document

    def get_by_id(self, id: str) -> Optional[T]:
        document = self._collection.find_one({"_id": ObjectId(id)})
        if document:
            return self._model(**document)
        return None

    def get_all(self) -> List[Optional[T]]:
        cursor = self._collection.find({})
        data = []
        for doc in cursor:
            doc['_id'] = str(doc['_id']) # validate later if there is a better solution
            data.append(doc)
        return data

    def update(self, id: str, document: T) -> Optional[T]:
        result = self._collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": document.model_dump(exclude_unset=True)}
        )
        if result.modified_count == 1:
            return self.get_by_id(id)
        return None

    def delete(self, id: str) -> bool:
        result = self._collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count == 1