# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vfit']

package_data = \
{'': ['*']}

install_requires = \
['brotli>=1.0.7,<2.0.0', 'fonttools>=4.13.0,<5.0.0', 'tqdm>=4.48.0,<5.0.0']

entry_points = \
{'console_scripts': ['vfit = vfit.app:main']}

setup_kwargs = {
    'name': 'vfit',
    'version': '2.1.0',
    'description': 'Generate backwards-compatible, static instances of variable fonts',
    'long_description': '<div align="center">\n  <img src="https://raw.githubusercontent.com/jonpalmisc/vfit/master/vfit-logo.png">\n</div>\n\n## About\n\nVFIT (Variable Font Instancing Tool) allows you to generate custom, static\ninstances of a variable font defined in a configuration file.\n\n## Installation\n\nVFIT is now available on the Python Package Index. You can install VFIT with\nthe following command:\n\n```sh\n$ pip3 install vfit\n```\n\nAlternatively, you can install VFIT by downloading a pre-built wheel from the\nReleases section or by building it yourself.\n\n``` sh\n# Skip this step if you\'re downloading a prebuilt wheel.\n$ git clone https://github.com/jonpalmisc/vfit.git && cd vfit\n$ poetry build && cd dist\n\n# Install VFIT from the wheel.\n$ pip install vfit-version-py3-none-any.whl\n```\n\n## Usage\n\nTo begin, you will need a variable font file to work with. Your first step will\nbe creating a configuration file. See `sample.json` for an example.\n\nNext, run VFIT and pass your configuration and variable font file as arguments:\n\n``` sh\n$ vfit config.json variable.ttf\n```\n\nIf you would like to generate instances into a specific directory, you can use\nthe `-o` option. For more options, see `vift --help`.\n\n## Contributing\n\nAll contributions are welcome. If you find a bug or have a request for a\nfeature, feel free to create a new issue (or even better, a pull request).\n\n## Credits\n\nSpecial thanks to [Viktor Rubenko](https://github.com/ViktorRubenko) for\nhelping me get exported fonts to work on Windows!\n\nThe VFIT logo uses [NewGlyph](https://beta.newglyph.com/)\'s\n[Armada](https://beta.newglyph.com/discovery-collection/#font-armada) variable\nfont.\n\n## License\n\nCopyright &copy; 2020 Jon Palmisciano\n\nVFIT is available under the MIT License. See [LICENSE.txt](LICENSE.txt) for\nmore information.\n',
    'author': 'Jon Palmisciano',
    'author_email': 'jp@jonpalmisc.com',
    'maintainer': 'Jon Palmisciano',
    'maintainer_email': 'jp@jonpalmisc.com',
    'url': 'https://github.com/jonpalmisc/vfit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
