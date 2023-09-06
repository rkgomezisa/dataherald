from bson import ObjectId

from config import USER_COL
from database.mongo import MongoDB
from modules.user.models.entities import User


class UserRepository:
    def get_users(self, filter: dict) -> list[User]:
        return [User(**user) for user in MongoDB.find(USER_COL, filter)]

    def get_user(self, user_id: str) -> User:
        user = MongoDB.find_by_id(USER_COL, user_id)
        return User(**user) if user else None

    def get_user_by_email(self, email: str) -> User:
        user = MongoDB.find_one(USER_COL, {"email": email})
        return User(**user) if user else None

    def delete_user(self, user_id: str) -> int:
        return MongoDB.delete_one(USER_COL, {"_id": ObjectId(user_id)})

    def update_user(self, user_id: str, new_user_data: dict) -> int:
        return MongoDB.update_one(USER_COL, {"_id": ObjectId(user_id)}, new_user_data)

    def add_user(self, new_user_data: dict) -> str:
        if MongoDB.find_one(USER_COL, {"email": new_user_data["email"]}):
            return None
        return str(MongoDB.insert_one(USER_COL, new_user_data))
