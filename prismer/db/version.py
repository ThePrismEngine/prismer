import datetime

from prismer.db.db import session_scope
from prismer.db.models import Version


def get_list():
    with (session_scope() as s):
        versions = s.query(Version).all()
    return versions

def add(version: Version):
    with (session_scope() as s):
        s.add(version)

def remove(name: str):
    with (session_scope() as s):
        version = s.query(Version).filter_by(name=name).one()
        s.delete(version)
        s.delete()