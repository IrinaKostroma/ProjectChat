from typing import Optional, List

import attr


@attr.dataclass
class User:
    id: Optional[int] = None
    email: Optional[str] = None


@attr.dataclass
class Message:
    id: Optional[int] = None
    user_id: Optional[int] = None
    chat_id: Optional[int] = None
    text: str
    time_created: str
    # title: str
    # description: str
    # price: float


@attr.dataclass
class Chat:
    id: int
    title: str
    admin: User
    users: List[User]

    def find_position(self, user: User):
        for user_ in self.users:
            if user_ == user:
                return user_
        return None

    def add_user(self, user: User):
        self.users.append(user)

    def delete_user(self, user: User):
        position = self.find_position(user)
        if position is not None:
            self.users.remove(user)
