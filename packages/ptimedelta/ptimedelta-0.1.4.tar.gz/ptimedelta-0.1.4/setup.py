# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptimedelta']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ptimedelta',
    'version': '0.1.4',
    'description': 'Pretty Timedelta. Convert your timedelta objects to pretty strings and vice versa.',
    'long_description': '# ptimedelta\n\nConvert time periods represented by strings to timedelta objects and vice versa. \n\n## Features\n1. Supports Python2.7, Python3+.\n2. Supports time periods with days, hours, minutes, seconds, milliseconds.\n\n## Installation\n```shell script\n$ pip install ptimedelta\n```\n\n## Examples\n```pydocstring\n>>> import ptimedelta as ptd\n>>> ptd.to_timedelta("12m34s")\ndatetime.timedelta(seconds=754)\n>>> ptd.to_seconds("3h23m4s", as_int=True)\n12184\n>>> ptd.to_seconds("3.96ms")\n0.00396\n```\n',
    'author': 'Anton Goy',
    'author_email': 'antongoy@internet.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/antongoy/ptimedelta',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
