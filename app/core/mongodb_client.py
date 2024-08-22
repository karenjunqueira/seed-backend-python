from pymongo import MongoClient
from typing import Optional

DEFAULT_CONNECTION_STRING = "mongodb://admin:pass@localhost:27017/"

class MongoDBClient:
    _instance: Optional[MongoClient] = None
 
    @classmethod
    def get_client(cls, connection_string: str = DEFAULT_CONNECTION_STRING) -> MongoClient:
        if cls._instance is None:
            cls._instance = MongoClient(connection_string)
        print(cls._instance)
        return cls._instance

    @classmethod
    def get_database(cls, database_name: str):
        client = cls.get_client()
        return client[database_name]

    @classmethod
    def get_collection(cls, database_name: str, collection_name: str):
        database = cls.get_database(database_name)
        return database[collection_name]