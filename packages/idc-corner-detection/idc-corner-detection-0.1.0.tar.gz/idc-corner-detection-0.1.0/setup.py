# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idc_corner_detection']

package_data = \
{'': ['*'],
 'idc_corner_detection': ['models/*',
                          'models/ssd_mobilenet_v2/*',
                          'models/ssd_mobilenet_v2/ckpt/*',
                          'models/ssd_mobilenet_v2/saved_model/*',
                          'models/ssd_mobilenet_v2/saved_model/variables/*']}

setup_kwargs = {
    'name': 'idc-corner-detection',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'nguyen minh',
    'author_email': 'nguyenminh180798@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
