from tornado.ioloop import IOLoop
from sqlalchemy import create_engine
from tornado.web import Application
from models.user import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from handlers.auth import *
from handlers.chat import *
import os
from config import *
import uuid

sync_engine = create_engine(SYNC_DATABASE_URL)
Base.metadata.create_all(bind=sync_engine)

async_engine = create_async_engine(ASYNC_DATABASE_URL)
SessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession)


def make_app():
    return Application([(r'/login', LoginHandler, dict(session=SessionLocal)),
                        (r'/register', RegisterHandler, dict(session=SessionLocal)), (r'/profile', ProfileHandler),
                        (r'/chat', ChatPageHandler), (r"/chat/ws", ChatWebSocket)],
                       template_path=os.path.join(os.getcwd(), 'templates'),
                       static_path=os.path.join(os.getcwd(), 'static'), cookie_secret=str(uuid.uuid4()))


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    IOLoop.current().start()
