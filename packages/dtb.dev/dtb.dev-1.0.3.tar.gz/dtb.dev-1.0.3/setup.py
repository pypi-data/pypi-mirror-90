# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dtb_dev']
install_requires = \
['black>=20.8b1,<21.0',
 'flake8-bandit>=2.1.2,<3.0.0',
 'flake8-bugbear>=20.1.4,<21.0.0',
 'flake8-builtins>=1.5.3,<2.0.0',
 'flake8-comprehensions>=3.2.3,<4.0.0',
 'flake8-debugger>=3.2.1,<4.0.0',
 'flake8-eradicate>=0.4.0,<0.5.0',
 'flake8-isort>=4.0.0,<5.0.0',
 'flake8-print>=3.1.4,<4.0.0',
 'flake8-quotes>=3.2.0,<4.0.0',
 'flake8-string-format>=0.3.0,<0.4.0',
 'flake8>=3.8.4,<4.0.0',
 'mccabe>=0.6.1,<0.7.0',
 'mypy',
 'pep8-naming>=0.11.1,<0.12.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'pytest>=6.1.1,<7.0.0']

extras_require = \
{'devtools': ['isort>=5.6.1,<6.0.0',
              'ptipython>=1.0.1,<2.0.0',
              'pre-commit>=2.7.1,<3.0.0',
              'autoflake>=1.4,<2.0',
              'jedi>=0.17.2,<0.18.0']}

setup_kwargs = {
    'name': 'dtb.dev',
    'version': '1.0.3',
    'description': 'DTB: Base dev tools',
    'long_description': None,
    'author': 'Dima Doroshev',
    'author_email': 'dima@doroshev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
