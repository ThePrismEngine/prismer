from pathlib import Path

from prismer.db.db import DatabaseManager
from prismer.utils import dirs

def init():
    DatabaseManager.init_db()
