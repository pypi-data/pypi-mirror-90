from pathlib import Path


def find_asset(name, basepath=Path.cwd()):
    for p in basepath.glob(f"**/{name}"):
        if p.is_file():
            return p
    return None
