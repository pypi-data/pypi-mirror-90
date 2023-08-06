import os

__version__ = "0.5.0"
from .dataframe import WEO
from .dates import all_releases, download


def get(year: int, release: int, path: str) -> WEO:
    if not os.path.exists(path):
        download(year, release, path)
    return WEO(path)
