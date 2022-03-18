from sqlalchemy import create_engine
from wsgiref.simple_server import make_server

from classic.sql_storage import TransactionContext

from application.services import UserService, ChatService, MessageService
from adapters import database, chat_api


class Settings:
    db = database.Settings()
    chat_api = chat_api.Settings()


class DB:
    db = database

    settings = db.Settings()

    engine = create_engine(settings.DB_URL)
    # db.metadata.create_all(engine)

    context = TransactionContext(bind=engine, expire_on_commit=False)

    users_repo = db.repositories.UsersRepo(context=context)
    chats_repo = db.repositories.ChatsRepo(context=context)
    messages_repo = db.repositories.MessagesRepo(context=context)
    chat_user_repo = db.repositories.ChatUsersRepo(context=context)


class Application:

    user_service = UserService(users_repo=DB.users_repo)
    chat_service = ChatService(chats_repo=DB.chats_repo, users_repo=DB.chat_user_repo)
    message_service = MessageService(messages_repo=DB.messages_repo)

    is_dev_mode = Settings.chat_api.IS_DEV_MODE
    allow_origins = Settings.chat_api.ALLOW_ORIGINS


# class Aspects:
#     services.join_points.join(DB.context)
#     chat_api.join_points.join(DB.context)


app = chat_api.create_app(
    users=Application.user_service,
    chats=Application.chat_service,
    messages=Application.message_service,
)

with make_server('', 8000, app) as httpd:
    print(f'Server running on http://localhost:{httpd.server_port} ...')
    httpd.serve_forever()