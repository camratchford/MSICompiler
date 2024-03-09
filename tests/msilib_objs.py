import msilib
import msilib.schema
from contextlib import contextmanager
from pathlib import Path



@contextmanager
def msilib_db(path: str):
    path_path = Path(path)
    db = msilib.init_database(
        str(path_path),
        msilib.schema,
        path_path.name,
        msilib.gen_uuid(),
        "0.0.1",
        "TestCompany"
    )
    try:
        yield db
    finally:
        db.Commit()
        db.Close()
