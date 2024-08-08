from system import directory


class File:
    def __init__(self, dir: directory.Dir) -> None:
        self._directory: directory.Dir = dir
