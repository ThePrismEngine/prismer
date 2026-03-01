from pathlib import Path

from prismer.db import db
from prismer.utils import dirs

def init():
    if (Path(dirs.user_data_dir) / Path("init")).is_file():
        return
    Path(dirs.user_data_dir).mkdir(parents=True, exist_ok=True)
    (Path(dirs.user_data_dir) / Path("init")).touch()
    db.create_all()
