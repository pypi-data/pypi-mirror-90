# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imfun']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'numpy>=1.19.4,<2.0.0', 'opencv-python>=4.5.1,<5.0.0']

entry_points = \
{'console_scripts': ['imfun = imfun.app:main']}

setup_kwargs = {
    'name': 'imfun',
    'version': '0.1.1',
    'description': 'Convert an image to cartoon',
    'long_description': '![ImFun](https://github.com/matyama/imfun/workflows/ImFun/badge.svg) [![PyPI version](https://badge.fury.io/py/imfun.svg)](https://badge.fury.io/py/imfun) [![PyPI status](https://img.shields.io/pypi/status/imfun.svg)](https://pypi.python.org/pypi/imfun/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/imfun.svg)](https://pypi.python.org/pypi/imfun/)\n\n# ImFun\nConvert an image to cartoon!\n\n## Installation\nThis application (package) is available on *PyPI*, so it can be installed using `pip` or `pipx`.\n```\n$ pipx install imfun\n  installed package imfun 0.1.0, Python 3.8.5\n  These apps are now globally available\n    - imfun\ndone! ✨ 🌟 ✨\n```\n\n## Usage\nOne can run the `imfun` app to convert an image to a cartoon like this\n```\n$ imfun -i examples/prague-castle.jpg -o examples/prague-castle-cartoon.jpg\nConverting image \'examples/prague-castle.jpg\'\nCartoon image saved as \'examples/prague-castle-cartoon.jpg\'\n```\nassuming that `examples/prague-castle.jpg` exists - or try it on any other image ;)\n\n## Examples\n<img src="./examples/prague.jpg" alt="Prague castle (original)" title="Original Image" width="250">\n<img src="./examples/prague-cartoon.jpg" alt="Prague castle (cartoon)" title="Cartoon Image" width="250">\n\n## Development\nDevelopment setup requires [Poetry](https://python-poetry.org/) to be installed.\nOnce the repository is cloned, one can setup everything with\n```bash\nmake setup\n```\n',
    'author': 'Martin Matyášek',
    'author_email': 'martin.matyasek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matyama/imfun',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
