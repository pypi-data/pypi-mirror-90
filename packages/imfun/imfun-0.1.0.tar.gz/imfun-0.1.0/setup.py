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
    'version': '0.1.0',
    'description': 'Convert an image to cartoon',
    'long_description': '![ImFun](https://github.com/matyama/imfun/workflows/ImFun/badge.svg)\n\n# ImFun\nConvert an image to cartoon!\n\n## Setup\nCurently both the installation and development setup require [Poetry](https://python-poetry.org/)\nto be installed. Once the repository is cloned, one can setup everything with\n```bash\nmake setup\n```\n\n## Usage\nIn an active environment, one can run the `imfun` app to convert an image to a cartoon like this\n```\n$ imfun -i examples/prague-castle.png -o examples/prague-castle-cartoon.png\nConverting image \'examples/prague-castle.png\'\nCartoon image saved as \'examples/prague-castle-cartoon.png\'\n```\n\n## Examples\n<img src="./examples/prague.jpg" alt="Prague castle (original)" title="Original Image" width="300">\n<img src="./examples/prague-cartoon.jpg" alt="Prague castle (cartoon)" title="Cartoon Image" width="300">\n',
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
