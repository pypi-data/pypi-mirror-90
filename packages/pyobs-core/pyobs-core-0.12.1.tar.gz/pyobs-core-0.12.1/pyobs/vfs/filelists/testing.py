import logging

from .filelist import FileList


log = logging.getLogger(__name__)


class TestingFileList(FileList):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, filename: str) -> list:
        return [
            __file__
        ]


__all__ = ['TestingFileList']
