import msilib
from msi_compiler.msilib_util import new_msilib_db
from cleanup import cleanup


def test_new_msilib_db():
    path = "test.msi"
    product_name = "test.msi"
    product_version = "0.0.1"
    manufacturer = "TestCompany"
    with new_msilib_db(path, product_name, product_version, manufacturer) as db:
        assert db.GetSummaryInformation(1).GetProperty(msilib.PID_SUBJECT) == b"test.msi"
    cleanup()
