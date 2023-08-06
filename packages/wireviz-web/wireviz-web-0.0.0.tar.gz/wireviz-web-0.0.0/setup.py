# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wireviz_web']

package_data = \
{'': ['*']}

install_requires = \
['flask-restplus==0.13.0',
 'flask>=1.1.2,<2.0.0',
 'werkzeug==0.16.1',
 'wireviz>=0.2,<0.3']

entry_points = \
{'console_scripts': ['wireviz-web = wireviz_web.cli:run']}

setup_kwargs = {
    'name': 'wireviz-web',
    'version': '0.0.0',
    'description': 'A wrapper around WireViz for bringing it to the web. Easily document cables and wiring harnesses.',
    'long_description': '###########\nWireViz-Web\n###########\n\n\n*****\nAbout\n*****\nWireViz-Web is a wrapper around the excellent WireViz_ by `Daniel Rojas`_\nfor bringing it to the web.\n\nOriginally, it has been conceived within a `WireViz fork`_ by `Jürgen Key`_.\n\nFor compatibility with PlantUML_, it includes an URL query parameter decoder\nby `Dyno Fu`_ and `Rudi Yardley`_.\n\nThanks!\n\n\n*******\nDetails\n*******\nWireViz is a tool for easily documenting cables, wiring harnesses and connector pinouts.\nIt takes plain text, YAML-formatted files as input and produces beautiful graphical output\n(SVG, PNG, ...) thanks to GraphViz_.\nIt handles automatic BOM (Bill of Materials) creation and has a lot of extra features.\n\n\n********\nSynopsis\n********\n::\n\n    # Render a plain YAML file.\n    echo "Bob -> Alice : hello" > test.yml\n    http --form http://127.0.0.1:3005/render yml_file@test.yml Accept:image/svg+xml\n    http --form http://127.0.0.1:3005/render yml_file@test.yml Accept:image/png\n\n    # Render a PlantUML request.\n    http http://127.0.0.1:3005/svg/SyfFKj2rKt3CoKnELR1Io4ZDoSa700==\n    http http://127.0.0.1:3005/png/SyfFKj2rKt3CoKnELR1Io4ZDoSa700==\n\n\n***********\nDevelopment\n***********\nAs this is still in its infancy, we humbly ask for support from the community.\nLook around, give it a test drive and submit patches.\n\n\n.. _WireViz: https://github.com/formatc1702/WireViz\n.. _WireViz fork: https://github.com/elbosso/WireViz\n.. _Daniel Rojas: https://github.com/formatc1702\n.. _Jürgen Key: https://github.com/elbosso\n.. _GraphViz: https://www.graphviz.org/\n.. _PlantUML: https://plantuml.com/\n.. _Dyno Fu: https://github.com/dyno\n.. _Rudi Yardley: https://github.com/ryardley\n',
    'author': 'Jürgen Key',
    'author_email': 'jkey@arcor.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daq-tools/wireviz-web',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
