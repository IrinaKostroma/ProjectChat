from classic.http_api import App

from application import services

from . import controllers


def create_app(users: services.UserService,
               chats: services.ChatService,
               messages: services.MessageService) -> App:

    app = App(prefix='/api')

    # app.register(controllers.Chats(chats=chats))
    # app.register(controllers.Users(users=users))
    # app.register(controllers.Messages(messages=messages))

    app.add_route('/users/', controllers.Chats(chats=chats))
    app.add_route('/chats/', controllers.Users(users=users))
    app.add_route('/messages/', controllers.Messages(messages=messages))

    return app

