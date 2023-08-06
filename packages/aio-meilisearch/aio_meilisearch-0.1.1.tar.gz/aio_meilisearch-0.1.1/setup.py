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
    'version': '0.1.1',
    'description': 'Async library for MeiliSearch',
    'long_description': '[![Tests](https://github.com/devtud/aio_meilisearch/workflows/Tests/badge.svg)](https://github.com/devtud/aio_meilisearch/actions?workflow=Tests)\n![pypi](https://img.shields.io/pypi/v/aio_meilisearch.svg)\n![versions](https://img.shields.io/pypi/pyversions/aio_meilisearch.svg)\n[![](https://pypip.in/license/aio_meilisearch/badge.svg)](https://pypi.python.org/pypi/aio_meilisearch)\n\n# AIO_MEILISEARCH\n## Async Wrapper over Meilisearch REST API with type hints\n\n```bash\npip install aio_meilisearch\n```\n\n## Usage\n\n```python\nfrom typing import TypedDict, List, Optional\nimport httpx\nfrom aio_meilisearch import (\n    MeiliSearch,\n    MeiliConfig,\n    Index,\n    SearchResponse,\n)\n\n\nclass MovieDict(TypedDict):\n    id: str\n    name: str\n    genres: List[str]\n    url: str\n    year: int\n\n\nhttp = httpx.AsyncClient()\n\nmeilisearch = MeiliSearch(\n    meili_config=MeiliConfig(\n        base_url=\'http://localhost:7700\',\n        private_key=\'PRIVATE_KEY\',\n        public_key=\'PUBLIC_KEY\',\n    ),\n    http_client=http,\n)\n\n\nindex: Index[MovieDict] = await meilisearch.create_index(name="movies", pk="id")\n\nawait index.update_settings(\n    {\n        "searchableAttributes": ["name", "genres"],\n        "displayedAttributes": [\n            "name",\n            "genres",\n            "id",\n            "url",\n            "year",\n        ],\n        "attributesForFaceting": ["genres", "year"],\n    }\n)\n\nmovie_list: List[MovieDict] = [\n    {\n        "name": "Oblivion",\n        "genres": ["action", "adventure", "sci-fi"],\n        "id": "tt1483013",\n        "url": "https://www.imdb.com/title/tt1483013/",\n        "year": 2013,\n    }\n]\n\nawait index.documents.add_many(movie_list)\n\nresponse: SearchResponse[MovieDict] = await index.documents.search(query="action")\n```\n\n## Contributing\n\n**Prerequisites:**\n - **poetry**\n - **nox**\n - **nox-poetry**\n\nInstall them on your system:\n```bash\npip install poetry nox nox-poetry\n```\n\nRun tests:\n```bash\nnox\n```',
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
