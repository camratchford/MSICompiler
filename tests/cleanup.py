from pathlib import Path


def cleanup():
    Path("test.msi").unlink(missing_ok=True)
