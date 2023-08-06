import os
from injecta.dtype.classLoader import loadClass
from databricksbundle.container.containerInitResolver import readContainerInit

container = loadClass(*readContainerInit())(os.environ['APP_ENV'])
