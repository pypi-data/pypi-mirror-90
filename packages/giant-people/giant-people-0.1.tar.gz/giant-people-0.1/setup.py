# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['people', 'people.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-filer>=1.7.1,<2.0.0', 'giant-mixins']

setup_kwargs = {
    'name': 'giant-people',
    'version': '0.1',
    'description': 'A small reusable package that adds a People app to a project',
    'long_description': '# Giant People\n\nA re-usable package which can be used in any project that requires a generic `People` app. \n\nThis will include the basic formatting and functionality such as model creation via the admin.\n\n## Installation\n\nTo install with the package manager, run:\n\n    $ poetry add giant-people\n\nYou should then add `"people", "easy_thumbnails" and "filer"` to the `INSTALLED_APPS` in your settings file. \nThe detail pages in this app use plugins which are not contained within this app. It is recommended that you include a set of plugins in your project, or use the `giant-plugins` app.\n\nIn order to run `django-admin` commands you will need to set the `DJANGO_SETTINGS_MODULE` by running\n\n    $ export DJANGO_SETTINGS_MODULE=settings\n\n## Preparing for release\n \nIn order to prep the package for a new release on TestPyPi and PyPi there is one key thing that you need to do. You need to update the version number in the `pyproject.toml`.\nThis is so that the package can be published without running into version number conflicts. The version numbering must also follow the Semantic Version rules which can be found here https://semver.org/.\n\n## Publishing\n\nPublishing a package with poetry is incredibly easy. Once you have checked that the version number has been updated (not the same as a previous version) then you only need to run two commands.\n\n  $ `poetry build` \n\nwill package the project up for you into a way that can be published.\n\n  $ `poetry publish`\n\nwill publish the package to PyPi. You will need to enter the username and password for the account which can be found in the company password manager\n',
    'author': 'Will-Hoey',
    'author_email': 'will.hoey@giantmade.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantmade/giant-people',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
