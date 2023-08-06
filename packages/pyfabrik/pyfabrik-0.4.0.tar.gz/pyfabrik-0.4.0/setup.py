# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfabrik']

package_data = \
{'': ['*']}

install_requires = \
['vectormath>=0.2.2,<0.3.0']

setup_kwargs = {
    'name': 'pyfabrik',
    'version': '0.4.0',
    'description': 'Python 3 implementation of FABRIK (Forward And Backward Reaching Inverse Kinematics) algorithm.',
    'long_description': '# pyfabrik\n\n![Badge showing number of total downloads from PyPI.](https://pepy.tech/badge/pyfabrik)\n\n![Badge showing number of monthly downloads from PyPI.](https://pepy.tech/badge/pyfabrik/month)\n\n![Badge showing that code has been formated with Black formatter.](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nPython 3 implementation of\n[FABRIK](http://www.andreasaristidou.com/FABRIK.html) (Forward And\nBackward Reaching Inverse Kinematics).\n## Installation\n\n    pip install pyfabrik\n\n## Usage\n\n**NOTE: API is still very unstable (until the 1.0 release). Suggestions are welcome.**\n\n```python\n\nimport pyfabrik\nfrom vectormath import Vector3\n\ninitial_joint_positions = [Vector3(0, 0, 0), Vector3(10, 0, 0), Vector3(20, 0, 0)]\ntolerance = 0.01\n\n# Initialize the Fabrik class (Fabrik, Fabrik2D or Fabrik3D)\nfab = pyfabrik.Fabrik3D(initial_joint_positions, tolerance)\n\nfab.move_to(Vector3(20, 0, 0))\nfab.angles_deg # Holds [0.0, 0.0, 0.0]\n\nfab.move_to(Vector3(60, 60, 0)) # Return 249 as number of iterations executed\nfab.angles_deg # Holds [43.187653094161064, 3.622882738369357, 0.0]\n```\n\n\n## Goal\n![Inverse kinematics example with human skeleton.](http://www.andreasaristidou.com/publications/images/FABRIC_gif_1.gif)\n\n## Roadmap\n\n- [x] Basic 2D (flat chain)\n- [x] Basic 3D (flat chain)\n- [ ] 3D testing sandbox\n- [ ] Basic 2D joint movement restrictions\n- [ ] Basic 3D joint movement restrictions\n- [ ] Complex chain support 2D\n- [ ] Complex chain support 3D\n\n## Contributing\n\n__All contributions are appreciated.__\n\nRead the paper [paper](http://www.andreasaristidou.com/publications/papers/FABRIK.pdf).\n\nFABRIKs [homepage](http://www.andreasaristidou.com/FABRIK.html) has links to other implementations.\n\n## [License](./LICENSE)\n\nMIT License\n\nCopyright (c) 2020 Saša Savić\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'Saša Savić',
    'author_email': 'sasa@savic.one',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/saleone/pyfabrik',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
