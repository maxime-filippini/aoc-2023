import pathlib


def read_file(path: pathlib.Path) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()
