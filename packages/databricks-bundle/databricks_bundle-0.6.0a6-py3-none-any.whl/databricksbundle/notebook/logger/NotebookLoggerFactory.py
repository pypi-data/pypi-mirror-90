from logging import Logger
from pathlib import Path
from loggerbundle.LoggerFactory import LoggerFactory

class NotebookLoggerFactory:

    def __init__(
        self,
        loggerFactory: LoggerFactory,
    ):
        self.__loggerFactory = loggerFactory

    def create(self, notebookPath: Path) -> Logger:
        return self.__loggerFactory.create(notebookPath.parent.stem)
