from pathlib import Path
from databricksbundle.notebook.path.NotebookPathResolverInterface import NotebookPathResolverInterface

class TestingPathResolver(NotebookPathResolverInterface):

    def __init__(
        self,
        testingPath: str,
    ):
        self.__testingPath = testingPath

    def resolve(self) -> Path:
        return Path(self.__testingPath)
