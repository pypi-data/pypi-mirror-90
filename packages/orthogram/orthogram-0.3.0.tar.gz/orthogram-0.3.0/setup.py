# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orthogram']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'Shapely>=1.7.1,<2.0.0',
 'networkx>=2.5,<3.0',
 'svgwrite>=1.4,<2.0']

setup_kwargs = {
    'name': 'orthogram',
    'version': '0.3.0',
    'description': 'Draw diagrams of graphs.',
    'long_description': 'Orthogram\n=========\n\nOrthogram is a command line program and Python library that lets you\ndraw diagrams of graphs.  It reads the definition of a diagram from a\nYAML file and produces a SVG file like this one:\n\n.. image:: examples/powerplant.svg\n   :width: 100%\n   :alt: Diagram of a combined cycle power plant\n\nTarget audience\n---------------\n\nThis project might be of interest to you if:\n\n* You want to draw a network of boxes connected to each other with\n  arrows.\n* You do not want to use a GUI.  You prefer your diagrams defined in\n  plain text files.\n* You know where your boxes should be, but you would rather have the\n  computer maintain the connections for you.\n* You are not exploring the interconnections of thousands of nodes in\n  random networks.  You are rather trying to prepare a slide for your\n  little presentation or create a diagram for your software\n  documentation project. A grid layout is probably all you need.\n* You tried to force `Graphviz`_ to output the layout you want, but to\n  no avail.\n\n.. _Graphviz: https://graphviz.org/\n\nInstallation and usage\n----------------------\n\nInstall from PyPI:\n\n.. code::\n   \n   pip install orthogram\n\nAssuming there is a diagram definition file named ``diagram.yaml`` in\nyour current directory, run the following command to produce a SVG\nfile:\n\n.. code::\n   \n   python -m orthogram diagram.yaml\n\nPlease read the full online `documentation`_ for more.\n\n.. _documentation: https://readthedocs.org/projects/orthogram/\n',
    'author': 'Georgios Athanasiou',
    'author_email': 'yorgath@gmail.com',
    'maintainer': 'Georgios Athanasiou',
    'maintainer_email': 'yorgath@gmail.com',
    'url': 'https://github.com/yorgath/orthogram',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
