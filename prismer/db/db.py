from pathlib import Path
from platformdirs import user_data_dir
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import event
from sqlalchemy.engine import Engine

from prismer.utils.dirs import app_dir


class DatabaseManager:
    _engine = None
    _db_path = None

    @classmethod
    def get_db_path(cls) -> Path:
        if cls._db_path is None:
            data_dir = app_dir
            data_dir.mkdir(parents=True, exist_ok=True)
            cls._db_path = data_dir / "storage.db"
        return cls._db_path

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls._engine = create_engine(
                f"sqlite:///{cls.get_db_path()}",
                echo=False,
                pool_pre_ping=True
            )
            @event.listens_for(Engine, "connect")
            def _set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        return cls._engine

    @classmethod
    def init_db(cls):
        from prismer.db.models import EngineVersion, Project
        SQLModel.metadata.create_all(cls.get_engine())

    @classmethod
    def get_session(cls) -> Session:
        return Session(cls.get_engine())