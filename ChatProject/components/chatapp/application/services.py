from typing import Optional, List, Tuple

from classic.components import component
from classic.aspects import PointCut
from classic.app import DTO, validate_with_dto
from classic.messaging import Publisher, Message
from pydantic import validate_arguments

from .dataclasses import User, Chat, Message, ChatUsers
from .errors import NoChat, NoMessage, EmptyCart
from . import interfaces


join_points = PointCut()
join_point = join_points.join_point


class ChatInfo(DTO):
    id: str
    title: str
    description: str
    price: float


class ChatInfoForChange(DTO):
    id: str
    title: str = None
    description: str = None
    price: float = None


@component
class ChatService:
    chats_repo: interfaces.ChatsRepo
    users_repo: interfaces.UsersRepo


    @join_point
    @validate_arguments
    def search_chats(self, search: str = None,
                        limit: int = 10, offset: int = 0) -> List[Chat]:
        return self.chats_repo.find_by_keywords(search, limit, offset)

    @join_point
    @validate_arguments
    def get_chat(self, title: str) -> Chat:
        chat = self.chats_repo.get_by_title(title)
        if chat is None:
            raise NoChat(title=title)

        return chat

    @join_point
    @validate_with_dto
    def add_chat(self, chat_info: ChatInfo):
        chat = chat_info.create_obj(Chat)
        self.chats_repo.add(chat)

    @join_point
    @validate_with_dto
    def change_chat(self, chat_info: ChatInfoForChange):
        chat = self.chats_repo.get_by_title(chat_info.title)
        if chat is None:
            raise NoChat(title=chat_info.title)

        chat_info.populate_obj(chat)


@component
class UserService:
    users_repo: interfaces.UsersRepo


    @join_point
    @validate_arguments
    def _get_user( self, user_id: Optional[int]):
        user = self.users_repo.get_or_create(user_id)
        return user

    @join_point
    @validate_arguments
    def join_to_chat(self):
        pass

    @join_point
    @validate_arguments
    def leave_chat(self, chat_id: int = None):
        pass

    @join_point
    @validate_arguments
    def create_message(self, user_id: int, text: str = '') -> int:
        user, cart = self._get_user_and_cart(user_id)
        if cart is None or not cart.positions:
            raise EmptyCart()

        message = Message(user)

        message.text = text

        self.messages_repo.add(message)
        # self.carts_repo.remove(cart)

        self.publisher.plan(
            Message('Message Placed', {'message_number': message.number})
        )

        return message.number


@component
class MessageService:
    messages_repo: interfaces.MessagesRepo

    @join_point
    @validate_arguments
    def get_message(self, mess_id: int,
                  user_id: Optional[int] = None) -> Message:

        message = self.messages_repo.get_by_number(mess_id)
        if message is None:
            raise NoMessage(number=mess_id)

        if user_id and message.user.id != user_id:
            raise NoMessage(number=mess_id)

        return message
