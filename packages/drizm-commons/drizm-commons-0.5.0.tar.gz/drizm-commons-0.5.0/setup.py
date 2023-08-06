# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drizm_commons',
 'drizm_commons.google',
 'drizm_commons.sqla',
 'drizm_commons.testing',
 'drizm_commons.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0']

extras_require = \
{'all': ['sqlalchemy==1.3.20',
         'google-auth==1.23.0',
         'requests>=2.25.0,<3.0.0',
         'google-cloud-storage==1.35.0'],
 'google': ['google-auth==1.23.0',
            'requests>=2.25.0,<3.0.0',
            'google-cloud-storage==1.35.0'],
 'sqla': ['sqlalchemy==1.3.20']}

setup_kwargs = {
    'name': 'drizm-commons',
    'version': '0.5.0',
    'description': 'Python3 commons for the Drizm organization',
    'long_description': '# Drizm Python Commons\n\n<p align="center">\n    <a href="https://badge.fury.io/py/drizm-commons">\n        <img \n        src="https://badge.fury.io/py/drizm-commons.svg" \n        alt="PyPI version" height="18"\n        >\n    </a>\n    <a href="https://github.com/psf/black">\n        <img\n        src="https://img.shields.io/badge/code%20style-black-000000.svg"\n        alt="Code Style" height="18"\n        >\n    </a>\n</p>\n\n---\nDocumentation:  \nhttps://commons.python.drizm.com/\n---\n\nThis package contains shared code used by\nthe Drizm organizations development team.  \n\nIt is not intended for public usage,\nbut you may still download,\nredistribute or modify it to your liking.\n\n**Author:**  \n[Ben "ThaRising" Koch](https://github.com/ThaRising)\n\n**Maintainers:**  \n[Dominik Lewandowski](https://github.com/dominik-lewandowski)\n\n## Requirements\n\nPython **^3.8.X** supported.\n\n**Debian 9+** and **Ubuntu 18.04+** for Linux,\nas well as **Windows 10 1909+**,\nare tested and supported.\n\nOther OS are still most likely supported,\nbut were not explicitly tested.\n',
    'author': 'ThaRising',
    'author_email': 'kochbe.ber@gmail.com',
    'maintainer': 'Dominik Lewandowski',
    'maintainer_email': 'dominik.lewandow@gmail.com',
    'url': 'https://github.com/drizm-team/python-commons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
