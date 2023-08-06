# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdfa_learning',
 'pdfa_learning.helpers',
 'pdfa_learning.learn_pdfa',
 'pdfa_learning.learn_pdfa.balle',
 'pdfa_learning.learn_pdfa.palmer',
 'pdfa_learning.learn_pdfa.utils',
 'pdfa_learning.learn_pdfa.utils.multiset',
 'pdfa_learning.pdfa']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.16,<0.17',
 'hypothesis>=5.43.5,<6.0.0',
 'mknotebooks==0.5.0',
 'numpy>=1.19.4,<2.0.0']

setup_kwargs = {
    'name': 'pdfa-learning',
    'version': '0.1.0',
    'description': 'A Python project template.',
    'long_description': None,
    'author': 'MarcoFavorito',
    'author_email': 'marco.favorito@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
