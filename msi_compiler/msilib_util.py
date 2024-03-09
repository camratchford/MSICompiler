import msilib
import msilib.schema
from contextlib import contextmanager


@contextmanager
def new_msilib_db(path: str, product_name: str, product_version: str, manufacturer: str):
    db = msilib.init_database(
        path,
        msilib.schema,
        product_name,
        msilib.gen_uuid(),
        product_version,
        manufacturer
    )
    try:
        yield db
    finally:
        db.Commit()
        db.Close()


def get_feature(db: msilib.OpenDatabase, feature_id: str):
    sql = r"SELECT * from Feature"
    view = db.OpenView(sql)
    view.Execute(None)
    result_dict = {}
    while True:
        result = view.Fetch()
        if result is None:
            break
        result_dict[feature_id] = {
            'feature_parent': result.GetString(2),
            'title': result.GetString(3),
            'description': result.GetString(4),
            'display': result.GetString(5),
            'level': result.GetString(6),
            'directory': result.GetString(7),
            'attributes': result.GetString(8)
        }

    print(result_dict)
    return result_dict.get(feature_id, "")


def get_custom_action(db: msilib.OpenDatabase, action_id: str):
    sql = r"SELECT * from CustomAction"
    view = db.OpenView(sql)
    view.Execute(None)
    result_dict = {}
    while True:
        result = view.Fetch()
        if result is None:
            break
        result_dict[action_id] = {
            'type': result.GetString(2),
            'source': result.GetString(3),
            'target': result.GetString(4)
        }

    print(result_dict)
    return result_dict.get(action_id, "")


def get_directory(db: msilib.OpenDatabase, directory_id: str):
    sql = r"SELECT * from Directory"
    view = db.OpenView(sql)
    view.Execute(None)
    result_dict = {}
    while True:
        result = view.Fetch()
        if result is None:
            break
        result_dict[directory_id] = {
            'directory_parent': result.GetString(2),
            'default_dir': result.GetString(3),
        }

    print(result_dict)
    return result_dict.get(directory_id, "")


def get_property(db: msilib.OpenDatabase, property: str):
    sql = r"SELECT * from Property"
    view = db.OpenView(sql)
    view.Execute(None)
    result_dict = {}
    while True:
        result = view.Fetch()
        if result is None:
            break
        result_dict[result.GetString(1)] = result.GetString(2)
    print(result_dict)
    return result_dict.get(property, "")