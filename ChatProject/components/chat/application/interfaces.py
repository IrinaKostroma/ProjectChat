from abc import ABC, abstractmethod
from typing import Optional, List

from .dataclasses import User, Message, Chat, Cart


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


class ChatsRepo(ABC):

    @abstractmethod
    def find_by_keywords(self, search: str = None,
                         limit: int = 10,
                         offset: int = 0) -> List[Chat]: ...

    @abstractmethod
    def get_by_title(self, sku: str) -> Optional[Chat]: ...

    @abstractmethod
    def add(self, product: Chat): ...

    @abstractmethod
    def remove(self, cart: Chat): ...


class CartsRepo(ABC):

    @abstractmethod
    def get_for_user(self, user_id: int) -> Optional[Cart]: ...

    @abstractmethod
    def add(self, cart: Cart): ...

    @abstractmethod
    def remove(self, cart: Cart): ...

    def get_or_create(self, user_id: int) -> Cart:
        cart = self.get_for_user(user_id)
        if cart is None:
            cart = Cart(user_id)
            self.add(cart)

        return cart


class MessagesRepo(ABC):

    @abstractmethod
    def add(self, message: Message): ...

    @abstractmethod
    def get_by_number(self, number: int) -> Optional[Message]: ...


class MailSender(ABC):

    @abstractmethod
    def send(self, mail: str, title: str, text: str): ...
