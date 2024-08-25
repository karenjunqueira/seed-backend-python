from repositories.user_mongo_repository import UserMongoRepository
from models.user import User

class UserService():
    def __init__(self):
        self.repository = UserMongoRepository()

    def create_user(self, user):
        return self.repository.create(user)

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def get_all(self):
        return self.repository.get_all()

    def update_user(self, id, user):
        return self.repository.update(id, user)

    def delete_user(self, id):
        return self.repository.delete(id)