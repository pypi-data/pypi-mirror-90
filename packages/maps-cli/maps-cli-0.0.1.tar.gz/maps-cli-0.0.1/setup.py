# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maps']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'geopy>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['maps = maps.commands:maps']}

setup_kwargs = {
    'name': 'maps-cli',
    'version': '0.0.1',
    'description': 'A CLI for maps services.',
    'long_description': '# Maps CLI \n\n[comment]: <> ([![Main Actions Status]&#40;https://github.com/sackh/maps-cli/workflows/main/badge.svg&#41;]&#40;https://github.com/sackh/maps-cli/actions&#41;)\nA simple command line tool to access services of various map services providers.\n\n## Usage\n# ![demo](https://github.com/sackh/maps-cli/raw/main/gifs/demo.gif)\n\n## Installation\n```bash\n    pip install maps-cli\n```\n\n## Test Suite\n```bash\n    poetry install\n    python -m poetry run python -m pytest -v --durations=10 --cov=maps tests\n```\n\n### Commands\n\n```bash\n    maps -h\n    maps show\n```\n\n## Maps Service Providers\nCurrently, this library is supporting following providers.\n\n- [OSM](https://www.openstreetmap.org/)\n- [HERE](https://www.here.com/)\n- [MapBox](https://www.mapbox.com/)\n- [TomTom](https://www.tomtom.com/)\n\n## Services\nCurrently, all providers support forward and reverse geocoding services.\n',
    'author': 'Sachin Kharude',
    'author_email': 'sachinkharude10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sackh/maps-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
