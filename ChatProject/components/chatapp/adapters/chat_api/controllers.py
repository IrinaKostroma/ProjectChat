from classic.components import component

from application import services

from .join_points import join_point


@component
class Chats:
    chats: services.ChatService

    @join_point
    def on_get_show_chat(self, request, response):
        product = self.catalog_chat.get_chat(**request.params)
        response.media = {
            'sku': product.sku,
            'title': product.title,
            'description': product.description,
            'price': product.price,
        }

    @join_point
    def on_get_search_chat(self, request, response):
        chats = self.catalog_chats.search_chats(**request.params)
        response.media = [
            {
                'sku': chat.sku,
                'title': chat.title,
                'description': chat.description,
                'price': chat.price,
            } for chat in chats
        ]


@component
class Users:
    users: services.UserService

    @join_point
    def on_get_show_cart(self, request, response):
        cart = self.checkout.get_cart(request.context.client_id)
        response.media = {
            'positions': [
                {
                    'product_sku': position.product.sku,
                    'product_price': position.product.price,
                    'quantity': position.quantity,
                }
                for position in cart.positions
            ]
        }

    @join_point
    def on_post_add_chatt_to_cart(self, request, response):
        self.checkout.add_chat_to_cart(
            customer_id=request.context.client_id,
            **request.media,
        )

    @join_point
    def on_post_remove_chat_from_cart(self, request, response):
        self.checkout.remove_chat_from_cart(
            user_id=request.context.client_id,
            **request.media,
        )

    @join_point
    def on_post_register_message(self, request, response):
        message_number = self.checkout.create_message(
            user_id=request.context.client_id,
        )
        response.media = {'message_number': message_number}


@component
class Messages:
    messages: services.MessageService

    @join_point
    def on_get_show_message(self, request, response):
        message = self.messages.get_message(
            user_id=request.context.client_id,
            **request.params,
        )
        response.media = {
            'number': message.number,
            'text': message.text
        }
