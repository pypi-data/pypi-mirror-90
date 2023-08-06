# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vetting']

package_data = \
{'': ['*']}

install_requires = \
['corner>=2.1.0,<3.0.0', 'lightkurve>=1.11.3,<2.0.0']

setup_kwargs = {
    'name': 'vetting',
    'version': '0.1.0',
    'description': 'Simple, stand-alone vetting tools for transiting signals in Keper, K2 and TESS data',
    'long_description': None,
    'author': 'Christina Hedges',
    'author_email': 'christina.l.hedges@nasa.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
