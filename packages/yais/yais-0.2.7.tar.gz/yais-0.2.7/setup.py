# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['yais']
install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'beautifulsoup4>=4.8.1,<5.0.0',
 'cloudscraper>=1.2.48,<2.0.0',
 'imagesize>=1.2.0,<2.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['yais = yais:cli']}

setup_kwargs = {
    'name': 'yais',
    'version': '0.2.7',
    'description': 'Yet Another Image Scraper',
    'long_description': "# yais\n\nYet Another Image Scraper\n\n## Changelog\n\n### v0.2.7\n\n- Fix Twitter support\n\n### v0.2.6\n\n- Refine pixiv support\n\n### v0.2.5\n\n- Cache Twitter's `guest_token`\n\n### v0.2.4\n\n- Fix support for Twitter\n\n### v0.2.3\n\n- Improve support for moebooru\n\n### v0.2.2\n\n- Fix suppport for konachan site with http\n\n### v0.2.1\n\n- Fix support for pixiv urls startswith `https://pixiv.net/`\n\n### v0.2.0\n\n- Add support for tweet with multiple images. ( e.g. https://twitter.com/hunwaritoast/status/1188048064948293632 )\n- Add support for zerochan.net\n",
    'author': 'Wu Haotian',
    'author_email': 'whtsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whtsky/yais',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
