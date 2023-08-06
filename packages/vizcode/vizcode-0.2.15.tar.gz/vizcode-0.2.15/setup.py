# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vizcode']

package_data = \
{'': ['*'],
 'vizcode': ['frontend/build/*',
             'frontend/build/code/python/main/*',
             'frontend/build/code/python/main/edge-code/*',
             'frontend/build/code/python/main/node-code/*',
             'frontend/build/code/react/contactus-graph/*',
             'frontend/build/code/react/dashboard-graph/*',
             'frontend/build/code/react/main/*',
             'frontend/build/code/react/main/edge-code/*',
             'frontend/build/static/css/*',
             'frontend/build/static/js/*']}

install_requires = \
['jedi>=0.17.2,<0.18.0', 'parso>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['vizcode = vizcode.main:start']}

setup_kwargs = {
    'name': 'vizcode',
    'version': '0.2.15',
    'description': 'Visualize your codebase as a graph',
    'long_description': '# VizCode\n\nVizCode is a command line tool for visualizing codebases as directed graphs. It utilizes static analysis to parse through your code to detect any definitions and references, which are then represented as nodes and edges respectively in a graph. Furthermore, the graph will be visualized on a web browser once the code files have been parsed.\n\n![](https://i.ibb.co/28S6ZFx/vizcode-screenshot.png)\n\nPlease note that VizCode is only supported for Python at the moment. For more information about VizCode visit our [website](https://vizcode.dev).\n\n## Installation\n\nYou can install VizCode from [PyPI](https://pypi.org/project/vizcode/):\n\n    pip install vizcode\n\nVizCode is supported on Python 3.7 and above.\n\n## How to use\n\nTo run VizCode on a codebase, simply call the program:\n\n    $ vizcode -p [ENTER A DIRECTORY PATH]\n\nSince VizCode only works on Python code, it will ignore any files without the .py file extension. If your code uses any dependencies that are not installed in your default environment, then you can specify an environment path:\n\n    $ vizcode -p [ENTER A DIRECTORY PATH] -e [ENTER AN ENVIRONMENT PATH]\n\nIf you would like VizCode to ignore test files, then you can add an additional argument:\n\n    $ vizcode -p [ENTER A DIRECTORY PATH] -t [ENTER PATH OF TEST FILES]\n',
    'author': 'Alex Rubin, Maciej Holubiec, Karthik Rao',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://vizcode.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
