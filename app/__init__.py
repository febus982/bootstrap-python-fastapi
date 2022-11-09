from attrs import asdict
from fastapi import FastAPI

from app.config import AppConfig
from app.containers import Container
from app.deps.sqlalchemy_manager import SQLAlchemyManager
from app.models import User, Address
from app.routes import init_routes
from app.storage import init_storage


def create_app(test_config: dict | None = None) -> FastAPI:
    if test_config:
        app = FastAPI(debug=True)
    else:
        app = FastAPI(debug=False)

    # Initialise and wire DI container
    c = Container()

    init_storage()
    init_routes(app)

    @app.get('/new')
    def new():
        user = User(name="pippo")
        a = Address(name="aaa", user_id=user.user_id)

        with c.SQLAlchemyManager().get_session() as session:
            session.add(user)
            session.add(a)
            session.commit()
            user_id = user.user_id
            address_id = a.address_id
            print(user_id, address_id)
            user_from_db = session.query(User).get(user_id)
            a_db = session.query(Address).get(address_id)
        return {"user": asdict(user_from_db), "address": asdict(a_db)}

    @app.get('/get/{id}')
    def get(id: int):
        with c.SQLAlchemyManager().get_session() as session:
            user_from_db = session.get(User, id)
            print(str(type(user_from_db)))
        return {"user_type": str(type(user_from_db))}

    return app
