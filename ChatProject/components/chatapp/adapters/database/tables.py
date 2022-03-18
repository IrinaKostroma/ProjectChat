from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Float, ForeignKey,
)


metadata = MetaData()


customers = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('password', String),
)

products = Table(
    'chats', metadata,
    Column('id', String, primary_key=True),
    Column('title', String),
    Column('description', String),
    Column('admin_name', String),
)

carts = Table(
    'chat_users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('chat_id', ForeignKey('customers.id')),
)

# cart_positions = Table(
#     'cart_positions', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('product_sku', ForeignKey('products.sku')),
#     Column('cart_id', ForeignKey('carts.id')),
#     Column('quantity', Integer),
# )

messages = Table(
    'messages', metadata,
    Column('number', Integer, primary_key=True),
    Column('text', Integer, primary_key=True),
    Column('user_name', ForeignKey('users.name')),
    Column('chat_title', ForeignKey('chats.title')),
)

# order_lines = Table(
#     'order_lines', metadata,
#     Column('order_number', ForeignKey('orders.number'), primary_key=True),
#     Column('product_sku', String),
#     Column('product_title', String),
#     Column('price', Float),
#     Column('quantity', Integer),
# )
