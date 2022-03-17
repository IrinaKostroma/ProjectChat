from typing import Optional, List

from classic.components import component
from classic.sql_storage import BaseRepository
from sqlalchemy import select

from chat.application import interfaces
from chat.application.dataclasses import User, Chat, Message, Cart


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):

    def get_by_id(self, id_: int) -> Optional[User]:
        query = select(User).where(User.id == id_)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, user: User):
        self.session.add(user)
        self.session.flush()


@component
class ChatsRepo(BaseRepository, interfaces.ChatsRepo):

    def find_by_keywords(self, search: str = '',
                         limit: int = 10,
                         offset: int = 0) -> List[Chat]:

        query = (select(Chat).order_by(Chat.sku)
                                .limit(limit)
                                .offset(offset))

        if search is not None:
            query = query.where(
                Chat.title.ilike(f'%{search}%') |
                Chat.description.ilike(f'%{search}%')
            )

        return self.session.execute(query).scalars()

    def get_by_title(self, title: str) -> Optional[Chat]:
        query = select(Chat).where(Chat.title == title)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, chat: Chat):
        self.session.add(chat)
        self.session.flush()


@component
class CartsRepo(BaseRepository, interfaces.CartsRepo):

    def get_for_user(self, user_id: int) -> Optional[Cart]:
        query = select(Cart).where(Cart.user_id == user_id)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, cart: Cart):
        self.session.add(cart)
        self.session.flush()

    def remove(self, cart: Cart):
        self.session.delete(cart)


@component
class MessagesRepo(BaseRepository, interfaces.MessagesRepo):

    def get_by_number(self, number: int) -> Optional[Message]:
        query = select(Message).where(Message.number == number)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, order: Message):
        self.session.add(order)
        self.session.flush()
