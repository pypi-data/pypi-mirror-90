# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mathx',
 'mathx.matseq',
 'mathx.ode',
 'mathx.ode.test_ode',
 'mathx.phase',
 'mathx.qdht',
 'mathx.sft',
 'mathx.test']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.4,<2.0.0', 'scipy>=1.4.1,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.9"': ['numba>=0.52.0,<0.53.0']}

setup_kwargs = {
    'name': 'mathx',
    'version': '0.2.1',
    'description': 'Array handling and mathematics built on top of numpy and scipy.',
    'long_description': '# mathx\nA mathematics toolbox built on top of `Numpy` and `Scipy`.\n\nMuch of this package was developed in support of optical physics calculations and experimental tools. The contents\nare expressed in mathematical rather than physical terms.\n\n## Installation\n\nDevelopment version: `pip install git+https://github.com/draustin/mathx`\n\nRelease version: `pip install mathx`\n\n## Testing\n\nUses `tox` (with [Poetry](https://python-poetry.org/)) and `pytest`.\n\n\n\n\n\n',
    'author': 'Dane Austin',
    'author_email': 'dane_austin@fastmail.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/draustin/mathx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
