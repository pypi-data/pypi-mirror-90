# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_sensors', 'my_sensors.sensors']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'my-sensors',
    'version': '0.1.0rc13',
    'description': 'A collection of sensors that I use with a standardized interface.',
    'long_description': '# my-sensors\nA collection of sensors that I use with a standardized interface.\n',
    'author': 'janjagusch',
    'author_email': 'jan.jagusch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
