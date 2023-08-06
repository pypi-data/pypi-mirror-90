import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata # pylint: disable = no-name-in-module
else:
    import importlib_metadata

def getContainerInit():
    entryPoints = importlib_metadata.entry_points().get('bricksflow', ())

    for entryPoint in entryPoints:
        if entryPoint.name == "container-init":
            return entryPoint.value.split(':')

    raise Exception('bricksflow\'s container-init entry_point not defined')

def entryPointExists():
    return 'bricksflow' in importlib_metadata.entry_points()
