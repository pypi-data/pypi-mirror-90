import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata # pylint: disable = no-name-in-module
else:
    import importlib_metadata

def readContainerInit():
    entryPoints = importlib_metadata.entry_points().get('bricksflow.app', ())

    if not entryPoints:
        raise Exception('bricksflow.app entry_point not defined in project\'s pyproject.toml')

    results = [entryPoint.value.split(':') for entryPoint in entryPoints if entryPoint.name == "container-init"]

    if not results:
        raise Exception('Missing container-init definition for the bricksflow.app entry_point in project\'s pyproject.toml')

    if len(results) > 1:
        raise Exception('Multiple container-init definitions found for the bricksflow.app entry_point')

    return results[0]

def entryPointExists():
    return 'bricksflow.app' in importlib_metadata.entry_points()
