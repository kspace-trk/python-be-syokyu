"""SQLAlchemy用."""

from debug_toolbar.panels.sqlalchemy import SQLAlchemyPanel as BasePanel
from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app import const

DATABASE_URL = f"mysql+pymysql://{const.DB_USER}:{const.DB_PASS}@{const.DB_HOST}/{const.DB_NAME}?charset=utf8"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


class SQLAlchemyPanel(BasePanel):
    """FastAPI Debug BarにSQLAlchemyクエリ実行結果表示パネルを追加するための記述."""
    async def add_engines(self, _: Request) -> None:  # noqa: D102
        self.engines.add(engine)
