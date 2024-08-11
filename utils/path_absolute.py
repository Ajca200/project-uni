import os

class PathLoader:
    @staticmethod
    def get_path(relative_path: str) -> str:
        base_path = os.path.dirname(__file__)
        return os.path.abspath(os.path.join(base_path, relative_path))