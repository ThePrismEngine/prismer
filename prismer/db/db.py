from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from prismer.utils import dirs

engine = sqlalchemy.create_engine(f"sqlite:///{dirs.user_data_dir}/db.db", echo=False)

DBSession = sessionmaker(bind=engine, expire_on_commit=False)

@contextmanager
def session_scope():
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def create_all():
    from prismer.db.models import Base, Version

    Base.metadata.create_all(engine)