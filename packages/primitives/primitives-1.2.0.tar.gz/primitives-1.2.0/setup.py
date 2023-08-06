# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_primitives', 'primitives']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'primitives',
    'version': '1.2.0',
    'description': 'Fake objects designed with OOP in mind.',
    'long_description': '# Primitives\n\n[![azure-devops-builds](https://img.shields.io/azure-devops/build/proofit404/primitives/5?style=flat-square)](https://dev.azure.com/proofit404/primitives/_build/latest?definitionId=5&branchName=master)\n[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/proofit404/primitives/5?style=flat-square)](https://dev.azure.com/proofit404/primitives/_build/latest?definitionId=5&branchName=master)\n[![pypi](https://img.shields.io/pypi/v/primitives?style=flat-square)](https://pypi.org/project/primitives)\n[![python](https://img.shields.io/pypi/pyversions/primitives?style=flat-square)](https://pypi.org/project/primitives)\n\nFake objects designed with OOP in mind.\n\n**[Documentation](https://proofit404.github.io/primitives) |\n[Source Code](https://github.com/proofit404/primitives) |\n[Task Tracker](https://github.com/proofit404/primitives/issues)**\n\nA paragraph of text explaining the goal of the library…\n\n## Pros\n\n- A feature\n- B feature\n- etc\n\n## Example\n\nA line of text explaining snippet below…\n\n```pycon\n\n>>> from primitives import Callable\n\n>>> func = Callable()\n\n>>> func()\n\n```\n\n## Questions\n\nIf you have any questions, feel free to create an issue in our\n[Task Tracker](https://github.com/proofit404/primitives/issues). We have the\n[question label](https://github.com/proofit404/primitives/issues?q=is%3Aopen+is%3Aissue+label%3Aquestion)\nexactly for this purpose.\n\n## Enterprise support\n\nIf you have an issue with any version of the library, you can apply for a paid\nenterprise support contract. This will guarantee you that no breaking changes\nwill happen to you. No matter how old version you\'re using at the moment. All\nnecessary features and bug fixes will be backported in a way that serves your\nneeds.\n\nPlease contact [proofit404@gmail.com](mailto:proofit404@gmail.com) if you\'re\ninterested in it.\n\n## License\n\n`primitives` library is offered under the two clause BSD license.\n\n<p align="center">&mdash; ⭐️ &mdash;</p>\n<p align="center"><i>The `primitives` library is part of the SOLID python family.</i></p>\n',
    'author': 'Artem Malyshev',
    'author_email': 'proofit404@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/primitives',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
