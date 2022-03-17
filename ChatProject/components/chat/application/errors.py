from classic.app.errors import AppError


class NoUser(AppError):
    msg_template = "No user with ID '{number}'"
    code = 'no_user'


class NoMessage(AppError):
    msg_template = "No message'{}'"
    code = 'no_message'


class EmptyChat(AppError):
    msg_template = "Chat is empty"
    code = 'chat_is_empty'