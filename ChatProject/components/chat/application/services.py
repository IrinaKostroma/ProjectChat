from typing import Optional, List, Tuple

from classic.components import component
from classic.aspects import PointCut
from classic.app import DTO, validate_with_dto
from classic.messaging import Publisher, Message
from pydantic import validate_arguments

from .dataclasses import User, Chat, Cart, Message
from .errors import NoChat, NoMessage, EmptyCart
from . import interfaces


join_points = PointCut()
join_point = join_points.join_point


class ProductInfo(DTO):
    sku: str
    title: str
    description: str
    price: float


class ProductInfoForChange(DTO):
    sku: str
    title: str = None
    description: str = None
    price: float = None


@component
class CatalogChats:
    chats_repo: interfaces.ChatsRepo
    # products_repo: interfaces.ProductsRepo

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
    def add_chat(self, product_info: ChatInfo):
        chat = product_info.create_obj(Chat)
        self.chats_repo.add(chat)

    @join_point
    @validate_with_dto
    def change_chat(self, chat_info: ChatInfoForChange):
        chat = self.chats_repo.get_by_title(chat_info.title)
        if chat is None:
            raise NoChat(title=product_info.title)

        chat_info.populate_obj(chat)


@component
class Checkout:
    chats_repo: interfaces.ChatsRepo
    users_repo: interfaces.UsersRepo
    carts_repo: interfaces.CartsRepo
    orders_repo: interfaces.OrdersRepo
    publisher: Publisher

    def _get_user_and_cart(
        self, user_id: Optional[int],
    ) -> Tuple[User, Cart]:

        user = self.users_repo.get_or_create(user_id)
        cart = self.carts_repo.get_or_create(user.id)
        return user, cart

    @join_point
    @validate_arguments
    def get_cart(self, user_id: int = None) -> Cart:
        __, cart = self._get_user_and_cart(user_id)
        return cart

    @join_point
    @validate_arguments
    # подписаться на чат
    def add_chat_to_cart(self, title: str,
                            id_chat: int = 1,
                            user_id: int = None):
        chat = self.chats_repo.get_by_title(title)
        if chat is None:
            raise NoChat(title=title)

        __, cart = self._get_user_and_cart(user_id)
        cart.add_chat(chat)

    @join_point
    @validate_arguments
    # покинуть чат
    def remove_chat_from_cart(self, title: str, user_id: int = None):
        chat = self.chats_repo.get_by_title(title)
        if chat is None:
            raise NoChat(title=title)

        __, cart = self._get_user_and_cart(user_id)
        cart.remove_product(chat)

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
class Messages:
    messages_repo: interfaces.MessagesRepo

    @join_point
    @validate_arguments
    def get_message(self, number: int,
                  user_id: Optional[int] = None) -> Message:

        message = self.messages_repo.get_by_number(number)
        if message is None:
            raise NoMessage(number=number)

        if user_id and message.user.id != user_id:
            raise NoMessage(number=number)

        return message
