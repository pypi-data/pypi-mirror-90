import os
from pathlib import Path
import tomlkit

def _loadEntryPoint(pyprojectPath: Path) -> list:
    with pyprojectPath.open('r') as t:
        config = tomlkit.parse(t.read())

        if (
            'tool' not in config
            or 'poetry' not in config['tool']
            or 'plugins' not in config['tool']['poetry']
            or 'bricksflow' not in config['tool']['poetry']['plugins']
        ):
            raise Exception('[tool.poetry.plugins.bricksflow] section is missing in pyproject.toml')

        return config['tool']['poetry']['plugins']['bricksflow']

def getContainerInit():
    workingDir = Path(os.getcwd())

    entryPointConfig = _loadEntryPoint(workingDir.joinpath('pyproject.toml'))
    return entryPointConfig['container-init'].split(':')
