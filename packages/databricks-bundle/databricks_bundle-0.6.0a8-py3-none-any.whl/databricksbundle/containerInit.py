from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.package.pathResolver import resolvePath
from pyfonycore.Kernel import Kernel
from pyfonybundles.loader import pyfonyBundlesLoader
from databricksbundle.DatabricksBundle import DatabricksBundle

def initContainer(appEnv: str):
    bundles = [*pyfonyBundlesLoader.loadBundles(), DatabricksBundle.createForConsoleTesting()]

    kernel = Kernel(
        appEnv,
        resolvePath('databricksbundle') + '/_config',
        YamlConfigReader(),
        bundles,
    )
    kernel.setAllowedEnvironments(['test_aws', 'test_azure', 'test_test'])

    return kernel.initContainer()
