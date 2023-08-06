# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jpgdl']
install_requires = \
['Pillow>=8.0.1,<9.0.0', 'httpx>=0.16.1,<0.17.0']

entry_points = \
{'console_scripts': ['jpgdl = jpgdl:cli']}

setup_kwargs = {
    'name': 'jpgdl',
    'version': '0.1.4',
    'description': 'Just a simple script and library image downloader and saving it in JPEG format, nothing fancy.',
    'long_description': "# jpgdl\n\nJust a simple script and library image downloader and saving it in JPEG format, nothing fancy.\n\n### Use Library\n\n```python3\nfrom jpgdl import JPGDL\n\nJPGDL.download(download_url='https://picsum.photos/200/300', filename='test')\n```\n\n### CLI\n\n```\njpgdl -h\n```\n\n#### Made By:\n\n##### TheBoringDude\n",
    'author': 'TheBoringDude',
    'author_email': 'iamcoderx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TheBoringDude/jpgdl',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
