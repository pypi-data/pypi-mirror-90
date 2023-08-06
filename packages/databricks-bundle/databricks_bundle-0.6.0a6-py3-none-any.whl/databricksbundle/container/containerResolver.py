import os
from injecta.container.ContainerInterface import ContainerInterface
from injecta.dtype.classLoader import loadClass
from databricksbundle.container.containerInitResolver import getContainerInit

def initAppContainer(appEnv: str) -> ContainerInterface:
    containerInitConfig = getContainerInit()

    initContainerFunction = loadClass(containerInitConfig[0], containerInitConfig[1])

    return initContainerFunction(appEnv)

container = initAppContainer(os.environ['APP_ENV'])
