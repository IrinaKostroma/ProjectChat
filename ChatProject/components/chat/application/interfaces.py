from abc import ABC, abstractmethod
from typing import Optional, List

from .dataclasses import User, Message, Chat


class UsersRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[User]: ...

    @abstractmethod
    def add(self, customer: User): ...

    def get_or_create(self, id_: Optional[int]) -> User:
        if id_ is None:
            user = User()
            self.add(user)
        else:
            user = self.get_by_id(id_)
            if user is None:
                user = User()
                self.add(user)

        return user


class MessagesRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[Message]: ...

    @abstractmethod
    def get_by_user_id(self, user_id: int,
                         limit: int = 10,
                         offset: int = 0) -> List[Message]: ...

    @abstractmethod
    def get_by_chat_id(self, chat_id: int, time_created: str,
                         limit: int = 10,
                         offset: int = 0) -> List[Message]: ...

    @abstractmethod
    def add(self, product: Message): ...


class ChatsRepo(ABC):

    @abstractmethod
    def add(self, cart: Chat): ...

    @abstractmethod
    def remove(self, cart: Chat): ...

    def get_or_create(self, user_id: int) -> Chat:
        chat = self.get_for_user(user_id)
        if chat is None:
            chat = Chat(user_id)
            self.add(chat)

        return chat


class MailSender(ABC):

    @abstractmethod
    def send(self, mail: str, title: str, text: str): ...
