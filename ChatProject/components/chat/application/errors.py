from classic.app.errors import AppError


class NoUser(AppError):
    msg_template = "No user with ID '{number}'"
    code = 'no_user'


class NoMessage(AppError):
    msg_template = "No message'{number}'"
    code = 'no_message'


class NoChat(AppError):
    msg_template = "No chat '{title}'"
    code = 'no_chat'


class EmptyCart(AppError):
    msg_template = "Cart is empty"
    code = 'cart_is_empty'