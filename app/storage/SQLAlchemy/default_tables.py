from app.deps.sqlalchemy_manager import SQLAlchemyBind
from app.models import Address, User
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


def init_tables(bind: SQLAlchemyBind):
    address = Table(
        "address",
        bind.registry_mapper.metadata,
        Column("address_id", Integer, primary_key=True),
        Column("user_id", Integer),
        Column("name", String(50)),
        Column("name2", String(50)),
        Column("name3", String(50)),
    )
    bind.registry_mapper.map_imperatively(Address, address)
    user = Table(
        "user",
        bind.registry_mapper.metadata,
        Column("user_id", Integer, primary_key=True),
        Column("name", String(50)),
        Column("fullname", String(50)),
        Column("nickname", String(12)),
    )
    bind.registry_mapper.map_imperatively(User, user)
