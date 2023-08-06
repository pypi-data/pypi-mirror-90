# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyqtgraph_extended',
 'pyqtgraph_extended.opengl',
 'pyqtgraph_extensions',
 'pyqtgraph_extensions.examples',
 'pyqtgraph_extensions.opengl',
 'pyqtgraph_extensions.opengl.test',
 'pyqtgraph_extensions.test',
 'pyqtgraph_recipes',
 'pyqtgraph_recipes.test']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.14.2,<6.0.0',
 'mathx>=0.2.1,<0.3.0',
 'pyopengl>=3.1.5,<4.0.0',
 'pyqtgraph==0.11.0']

setup_kwargs = {
    'name': 'pyqtgraph-extensions',
    'version': '0.5.2',
    'description': 'Various extensions for pyqtgraph.',
    'long_description': "# README\n\nVarious extensions for [pyqtgraph](https://github.com/pyqtgraph/pyqtgraph).\n\nInstalling `pyqtgraph_extensions` creates two namespaces:\n\n* `pyqtgraph_extensions` - various classes and functions providing some of extra functionality for pyqtgraph\n* `pyqtgraph_extended` - a namespace merging pyqtgraph_extensions with the original pyqtgraph\n\nIn principle, it should be possible to import `pyqtgraph_extended` instead of `pyqtgraph` and have the same behaviour but with new functionality available. So the two options for using this repository are:\n\n    import pyqtgraph as pg\n    import pyqtgraph_extensions as pgx\n\nor\n\n    import pyqtgraph_extended as pg\n\n## Installation\n\nTo get latest release from PyPi: `pip install pyqtgraph_extensions`.\n\nOr install from GitHub: `pip install git+https://github.com/draustin/pyqtgraph_extensions`.\n\npyqtgraph_extensions is packaged using [Poetry](https://python-poetry.org/).\n\nPython 3.6 or later is required.\n\n## Features\n\nSee [`pyqtgraph_extensions/examples`](pyqtgraph_extensions/examples) for some examples.\n\n### Axis alignment across multiple plot items\n\nThe `AlignedPlotItem` is so-called because it uses its parent's graphics layout object for holding its constituent items (view box, axis items and title) rather than creating one internally. Its constituents can therefore be aligned with those of other items in the parent's graphics layout, including the constituent items of other `AlignedPlotItem` objects. Here's an [example](pyqtgraph_extensions/examples/demo_axis_alignment.py).\n![](screenshots/axis_alignment.png)\n\n### More axis controls\n\n`AxisItem` is reimplemented with its own buttons for autoranging at the upper and lower limits.\n![](screenshots/axis_buttons_labelled.png)\n\n### Traditional interactive color bar\n\n`pyqtgraph_extensions` adds a MATLAB-style `ColorBarItem` which can be linked to multiple ImageItems.\n\n![](screenshots/live_colorbaritem.gif)\n\n### Other\n\n* Simplified exporting with the `export` function\n* Easy adding of a second vertical axis on the right hand side (with linked x axis), likewise for a second horizontal axis on the top. See [example](pyqtgraph_extensions/examples/demo_right_top_axes.py).\n* More [GLGraphicsItems](http://www.pyqtgraph.org/documentation/3dgraphics/glgraphicsitem.html) - see the [unit tests](pyqtgraph_extensions/opengl/test/test_pyqtgraph_extensions_opengl.py).\n\n## Testing\n\nI use `pytest` with `pytest-qt` during development work and `tox` to test installation & dependencies.\n\n## Plan / outlook\n\nI developed the various features as needed and will continue on the same basis. When I began writing `pyqtgraph_extensions` I was just starting out with Python, Git/GitHub, and open source tools in general (I'm a convert from MATLAB).\n\nI'd be happy for any/all features to be moved into `pyqtgraph` proper. Feel free to [reach out](mailto:dane_austin@fastmail.com.au).\n\n### TODO\n\n* Add switch for user interactivity on color bar example.\n* Documentation\n",
    'author': 'Dane Austin',
    'author_email': 'dane_austin@fastmail.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/draustin/pyqtgraph_extensions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
