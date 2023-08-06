# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databricksbundle',
 'databricksbundle.dbutils',
 'databricksbundle.jdbc',
 'databricksbundle.notebook',
 'databricksbundle.notebook.decorator',
 'databricksbundle.notebook.decorator.executor',
 'databricksbundle.notebook.function',
 'databricksbundle.notebook.logger',
 'databricksbundle.notebook.path',
 'databricksbundle.spark',
 'databricksbundle.spark.config']

package_data = \
{'': ['*'],
 'databricksbundle': ['_config/*', '_config/databricks/*', '_config/scope/*']}

install_requires = \
['console-bundle==0.3.0a3',
 'injecta==0.8.13b1',
 'logger-bundle==0.6.0a3',
 'pyfony-bundles==0.2.5a2']

entry_points = \
{'pyfony.bundle': ['autodetect = '
                   'databricksbundle.DatabricksBundle:DatabricksBundle.autodetect'],
 'pyfony.testing_scope': ['console = '
                          'databricksbundle.DatabricksBundle:DatabricksBundle.createForConsoleTesting',
                          'notebook = '
                          'databricksbundle.DatabricksBundle:DatabricksBundle.createForNotebookTesting']}

setup_kwargs = {
    'name': 'databricks-bundle',
    'version': '0.6.0a9',
    'description': 'Databricks bundle for the Pyfony framework',
    'long_description': '# Databricks bundle\n\nThis bundle helps you to create simple function-based Databricks notebooks, which can be easily auto-documented and unit-tested. It is part of the [Bricksflow framework](https://github.com/bricksflow/bricksflow).\n\n![alt text](docs/function-based-notebook.png "Databricks function-based notebook example")\n\n## Installation\n\nInstall the bundle via Poetry:\n\n```\n$ poetry add databricks-bundle && poetry add databricks-connect --dev\n```\n\n## Usage\n\n1. [Writing function-based notebooks](docs/function-based-notebooks.md)\n1. [Recommended notebooks structure](docs/structure.md)\n1. [Configuring notebook functions](docs/configuration.md)\n1. [Using dependencies](docs/dependencies.md)\n1. [Databricks Connect setup](docs/databricks-connect.md)\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricksflow/databricks-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
