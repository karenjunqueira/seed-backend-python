from http import HTTPStatus
from fastapi import HTTPException
from repositories.user_mongo_repository import UserMongoRepository
from models.user import User
from utils.password_util import PasswordUtil

class UserService():
    def __init__(self):
        self.repository = UserMongoRepository()

    def get_by_attributes(self,user):
        list_filters = [{"email": user.email}]
        users_found = self.repository.get_by_attribute(list_filters)
        return users_found

    def validate_user_exist(self, user):
        list_filters = [{"email": user.email}, {"username":user.username}]
        users_found = self.repository.get_by_attribute(list_filters)

        if len(users_found) > 0:
            if users_found[0].username == user.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Username already exists',
                )
            elif users_found[0].email == user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Email already exists',
                )

        return False
    
    def create_user(self, user):
        self.validate_user_exist(user)
        hashed_password = PasswordUtil.get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            password=hashed_password,
        )
        return self.repository.create(db_user)

    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def get_all(self):
        return self.repository.get_all()

    def update_user(self, id, user):
        hashed_password =PasswordUtil.get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            password=hashed_password,
        )
        return self.repository.update(id, db_user)

    def delete_user(self, id):
        return self.repository.delete(id)