from sqlalchemy import create_engine

from classic.sql_storage import TransactionContext
from classic.messaging_kombu import KombuPublisher
from kombu import Connection

from chat.application import services
from chat.adapters import database, message_bus, shop_api, mail_sending


class DB:
    db = database

    settings = db.Settings()

    engine = create_engine(settings.DB_URL)
    db.metadata.create_all(engine)

    context = TransactionContext(bind=engine, expire_on_commit=False)

    customers_repo = db.repositories.CustomersRepo(context=context)
    products_repo = db.repositories.ProductsRepo(context=context)
    carts_repo = db.repositories.CartsRepo(context=context)
    orders_repo = db.repositories.OrdersRepo(context=context)


# class MessageBus:
#     settings = message_bus.Settings()
#     connection = Connection(settings.BROKER_URL)
#     message_bus.broker_scheme.declare(connection)
#
#     publisher = KombuPublisher(
#         connection=connection,
#         scheme=message_bus.broker_scheme,
#     )
#
#
# class MailSending:
#     sender = mail_sending.FileMailSender()


class Application:
    catalog_chats = services.CatalogChats(chats_repo=DB.chats_repo)
    checkout = services.Checkout(
        users_repo=DB.users_repo,
        chats_repo=DB.chats_repo,
        carts_repo=DB.carts_repo,
        messages_repo=DB.messages_repo  #       publisher=MessageBus.publisher,
    )
    messages = services.Messages(
        messages_repo=DB.messages_repo,
    )

# class Aspects:
#     services.join_points.join(DB.context)
#     shop_api.join_points.join(MessageBus.publisher, DB.context)


app = chat_api.create_app(
    catalog_chats=Application.catalog_chats,
    checkout=Application.checkout,
    messages=Application.messages,
)