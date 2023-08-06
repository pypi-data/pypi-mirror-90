import os
from pathlib import Path
import tomlkit
from pyfony import bootstrap

def readContainerInit():
    workingDir = Path(os.getcwd())
    config = _loadPyprojectToml(workingDir.joinpath('pyproject.toml'))

    if bootstrap.configExists(config):
        boostrapConfig = bootstrap.getBootstrapConfig(config)
        return bootstrap.getContainerInit(boostrapConfig)

    entryPointConfig = _getEntryPoint(config)
    return entryPointConfig['container-init'].split(':')

def _loadPyprojectToml(pyprojectPath: Path):
    with pyprojectPath.open('r', encoding='utf-8') as t:
        return tomlkit.parse(t.read())

def _getEntryPoint(config: dict) -> list:
    if (
        'tool' not in config
        or 'poetry' not in config['tool']
        or 'plugins' not in config['tool']['poetry']
        or 'bricksflow.app' not in config['tool']['poetry']['plugins']
    ):
        raise Exception('[tool.poetry.plugins."bricksflow.app"] section is missing in pyproject.toml')

    return config['tool']['poetry']['plugins']['bricksflow.app']
