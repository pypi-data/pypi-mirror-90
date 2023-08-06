# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_meilisearch']

package_data = \
{'': ['*']}

install_requires = \
['httpx']

setup_kwargs = {
    'name': 'aio-meilisearch',
    'version': '0.1.0',
    'description': 'Async library for MeiliSearch',
    'long_description': '[![Tests](https://github.com/devtud/aio_meilisearch/workflows/Tests/badge.svg)](https://github.com/devtud/aio_meilisearch/actions?workflow=Tests)\n![pypi](https://img.shields.io/pypi/v/aio_meilisearch.svg)\n![versions](https://img.shields.io/pypi/pyversions/aio_meilisearch.svg)\n[![](https://pypip.in/license/aio_meilisearch/badge.svg)](https://pypi.python.org/pypi/aio_meilisearch)\n\n# AIO_MEILISEARCH\n## Async HTTPX Wrapper over Meilisearch REST API\n\n### Run tests with nox and poetry\n\n**Prerequisites:**\n - **poetry**\n - **nox**\n - **nox-poetry**\n\nInstall them on your system:\n```bash\npip install poetry nox nox-poetry\n```\n\nRun tests:\n```bash\nnox\n```\n\nThe tests will be run against:\n - Python 3.8\n - Python 3.9\n\nor whichever is present on your system.\n',
    'author': 'devtud',
    'author_email': 'devtud@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devtud/aio_meilisearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
