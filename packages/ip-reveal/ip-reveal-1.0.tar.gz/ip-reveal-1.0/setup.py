# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ip_reveal',
 'ip_reveal.assets',
 'ip_reveal.assets.sounds',
 'ip_reveal.assets.sounds.alerts',
 'ip_reveal.assets.ui_elements',
 'ip_reveal.assets.ui_elements.backgrounds',
 'ip_reveal.assets.ui_elements.icons',
 'ip_reveal.assets.ui_elements.icons.alerts',
 'ip_reveal.assets.ui_elements.themes',
 'ip_reveal.gui',
 'ip_reveal.gui. windows',
 'ip_reveal.gui. windows.backgrounds',
 'ip_reveal.popups',
 'ip_reveal.timers',
 'ip_reveal.tools',
 'ip_reveal.tools.arguments',
 'ip_reveal.tools.network']

package_data = \
{'': ['*'], 'ip_reveal': ['.idea/*', '.idea/inspectionProfiles/*']}

install_requires = \
['PySimpleGUI>=4.30.0,<5.0.0',
 'PySimpleGUIQt>=0.35.0,<0.36.0',
 'humanize>=3.1.0,<4.0.0',
 'inspy_logger==2.0.0a6',
 'inspyred_print>=1.0,<2.0',
 'requests>=2.25.0,<3.0.0',
 'simpleaudio>=1.0.4,<2.0.0']

entry_points = \
{'console_scripts': ['ip-reveal = ip_reveal:main']}

setup_kwargs = {
    'name': 'ip-reveal',
    'version': '1.0',
    'description': 'A GUI-based widget that checks your IP address periodically, sending notifications if it changes.',
    'long_description': None,
    'author': 'Taylor B.',
    'author_email': 'tayjaybabee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
