from classic.http_api import App

from chat.application import services

from .auth import auth
from .join_points import join_points

from . import controllers


def create_app(catalog_chats: services.CatalogChats,
               checkout: services.Checkout,
               messages: services.Messages) -> App:

    app = App(prefix='/api')

    app.register(controllers.CatalogChats(catalog_chats=catalog_chats))
    app.register(controllers.Checkout(checkout=checkout))
    app.register(controllers.Messagess(messages=messages))

    join_points.join(auth)

    return app
