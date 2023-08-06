import re
from consolebundle.detector import isRunningInConsole
from injecta.container.ContainerInterface import ContainerInterface
from pyfonybundles.Bundle import Bundle
from databricksbundle.notebook.NotebookErrorHandler import setNotebookErrorHandler
from databricksbundle.detector import isDatabricks
from databricksbundle.notebook.helpers import getNotebookPath, isNotebookEnvironment

class DatabricksBundle(Bundle):

    DATABRICKS_NOTEBOOK = 'databricks_notebook.yaml'
    DATABRICKS_SCRIPT = 'databricks_script.yaml'
    DATABRICKS_CONNECT = 'databricks_connect.yaml'
    DATABRICKS_TEST = 'databricks_test.yaml'

    SCOPE_CONSOLE = 'console_scope.yaml'
    SCOPE_NOTEBOOK = 'notebook_scope.yaml'

    @classmethod
    def autodetect(cls):
        if isDatabricks():
            if isNotebookEnvironment():
                return DatabricksBundle(DatabricksBundle.DATABRICKS_NOTEBOOK, DatabricksBundle.SCOPE_NOTEBOOK)

            return DatabricksBundle(DatabricksBundle.DATABRICKS_SCRIPT, DatabricksBundle.SCOPE_NOTEBOOK)

        if isRunningInConsole():
            return DatabricksBundle(DatabricksBundle.DATABRICKS_CONNECT, DatabricksBundle.SCOPE_CONSOLE)

        return DatabricksBundle(DatabricksBundle.DATABRICKS_CONNECT, DatabricksBundle.SCOPE_NOTEBOOK)

    @staticmethod
    def createForConsoleTesting():
        return DatabricksBundle(DatabricksBundle.DATABRICKS_TEST, DatabricksBundle.SCOPE_CONSOLE)

    @staticmethod
    def createForNotebookTesting():
        return DatabricksBundle(DatabricksBundle.DATABRICKS_TEST, DatabricksBundle.SCOPE_NOTEBOOK)

    def __init__(self, databricksConfig: str, scopeConfig: str):
        self.__databricksConfig = databricksConfig
        self.__scopeConfig = scopeConfig

    def getConfigFiles(self):
        return ['config.yaml', 'databricks/' + self.__databricksConfig, 'scope/' + self.__scopeConfig]

    def boot(self, container: ContainerInterface):
        parameters = container.getParameters()

        if (
            isDatabricks()
            and isNotebookEnvironment()
            and parameters.databricksbundle.enableNotebookErrorHandler is True
            and not re.match('^/Users/', getNotebookPath())
        ):
            setNotebookErrorHandler()
