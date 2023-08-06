# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libpdf', 'libpdf.models']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5,<6',
 'chardet>=3,<4',
 'click>=7,<8',
 'pillow>=8.1.0,<9.0.0',
 'pycryptodome>=3.9.9,<4.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'sortedcontainers>=2.3.0,<3.0.0',
 'unicodecsv>=0.14.1,<0.15.0',
 'wand>=0.6.5,<0.7.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.8"': ['importlib-metadata>=1.6.0,<2.0.0'],
 'colorama': ['colorama>=0.4.4,<0.5.0'],
 'docs': ['sphinx',
          'sphinx_rtd_theme',
          'sphinxcontrib-needs',
          'sphinxcontrib-plantuml'],
 'tqdm': ['tqdm>=4.50.0,<5.0.0']}

entry_points = \
{'console_scripts': ['libpdf = libpdf.core:main_cli']}

setup_kwargs = {
    'name': 'libpdf',
    'version': '0.0.1',
    'description': 'Extract structured data from PDFs.',
    'long_description': '**Complete documentation** http://libpdf.readthedocs.io/en/latest/\n\nIntroduction\n============\n\n``libpdf`` allows the extraction of structured data from machine readable PDFs.\n\n',
    'author': 'Marco Heinemann',
    'author_email': 'marco.heinemann@useblocks.com',
    'maintainer': 'Jui-Wen Chen',
    'maintainer_email': 'jui-wen.chen@useblocks.com',
    'url': 'http://pypi.python.org/pypi/libpdf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
