# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpl_tools']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0']

setup_kwargs = {
    'name': 'mpl-tools',
    'version': '0.2',
    'description': 'Tools for working with matplotlib',
    'long_description': '# mpl-tools\n\n[![Travis](https://travis-ci.org/patricknraanes/mpl-tools.svg?branch=master)](https://travis-ci.org/patricknraanes/mpl-tools)\n[![Coveralls](https://coveralls.io/repos/github/patricknraanes/mpl-tools/badge.svg?branch=master)](https://coveralls.io/github/patricknraanes/mpl-tools?branch=master)\n[![Hits.dwyl](http://hits.dwyl.com/patricknraanes/mpl-tools.svg)](http://hits.dwyl.com/patricknraanes/mpl-tools)\n[![PyPI](https://badge.fury.io/py/mpl-tools.svg)](https://badge.fury.io/py/mpl-tools)\n[![PyPI - Downloads](https://img.shields.io/pypi/dw/mpl-tools)](https://pypi.org/project/mpl-tools/0.1.5/)\n\nThis package provides some tools to work with [Matplotlib](https://matplotlib.org/).\n\n- `freshfig`\n- `anchor_axes`, with auxiliaries:\n  - `align_ax_with`\n  - `set_ax_size`\n  - `get_legend_bbox`\n  - `xFontsize`\n- `add_log_toggler`\n  - `toggle_scale`\n',
    'author': 'patricknraanes',
    'author_email': 'patrick.n.raanes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
