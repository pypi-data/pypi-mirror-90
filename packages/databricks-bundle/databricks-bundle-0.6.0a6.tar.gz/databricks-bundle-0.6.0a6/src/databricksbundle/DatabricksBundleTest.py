import unittest
from injecta.testing.servicesTester import testServices
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.package.pathResolver import resolvePath
from pyfony.Kernel import Kernel
from pyfonybundles.loader import pyfonyBundlesLoader
from databricksbundle.DatabricksBundle import DatabricksBundle

class DatabricksBundleTest(unittest.TestCase):

    def test_azure(self):
        container = self.__createContainer('test_azure')

        testServices(container)

    def test_aws(self):
        container = self.__createContainer('test_aws')

        testServices(container)

    def test_test(self):
        container = self.__createContainer('test_test')

        testServices(container)

    def __createContainer(self, appEnv: str):
        bundles = [*pyfonyBundlesLoader.loadBundles(), DatabricksBundle.createForConsoleTesting()]

        kernel = Kernel(
            appEnv,
            resolvePath('databricksbundle') + '/_config',
            bundles,
            YamlConfigReader()
        )
        kernel.setAllowedEnvironments(['test_aws', 'test_azure', 'test_test'])

        return kernel.initContainer()

if __name__ == '__main__':
    unittest.main()
