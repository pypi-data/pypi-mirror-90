# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exclock', 'exclock.mains']

package_data = \
{'': ['*'], 'exclock': ['assets/clock/*', 'assets/sound/*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0', 'json5>=0.9.5,<0.10.0', 'ycontract>=0.3.2']

entry_points = \
{'console_scripts': ['exclock = exclock.main:main']}

setup_kwargs = {
    'name': 'exclock',
    'version': '0.3.0.1',
    'description': 'exclock is a cui extended timer.',
    'long_description': 'Exclock\n=======\n\n![image](https://img.shields.io/pypi/v/exclock)\n![image](https://img.shields.io/pypi/pyversions/exclock)\n![image](https://gitlab.com/yassu/exclock/badges/master/pipeline.svg)\n![image](https://gitlab.com/yassu/exclock/badges/master/coverage.svg)\n![image](https://img.shields.io/pypi/l/exclock)\n\nexclock is a cui extended timer.\n\nRequired\n--------\n\n-   mplayer\n-   xmessage or terminal-notifier(If you use mac, I recommend\n    terminal-notifier)\n\nHow to install\n--------------\n\n    $ pip install exclock\n\nUsage\n-----\n\n    $ exclock [options] {clock-filename}\n\nFeatures\n--------\n\n-   Sound an alarm at a specified time.\n-   Sound the alarm after the specified time has elapsed.\n-   You can flexibly set the alarm.\n\nOptions\n-------\n\n-   `--version`: show program\'s version number and exit\n-   `-h, --help`: show this help message and exit\n-   `-l, --list`: show clock names in your PC and exit\n-   `-t, --time`: Time which spends until or to specified\n-   `-r, --ring-filename`: Sound-filename which used for ringing with\n    -t, --time option. Note that you can use EXCLOCK\\_RING\\_FILENAME\n    system variable if you often indicate ring-filename option.\n-   `--trace, --traceback`: show traceback\n\nHow to sound an alarm at a specified time\n-----------------------------------------\n\nEnter\n\n    $ exclock -t {time}\n\nformat command.\n\nWhere time is given in the {hour}:{min} or {hour}:{min}:{sec} format.\n\nEx.\n\n    $ exclock -t "1:00"\n    $ exclock -t "1:00:20"\n\nHow to sound the alarm after the specified time has elapsed\n-----------------------------------------------------------\n\nEnter\n\n    $ exclock -t {time}\n\nformat command.\n\nWhere time is given in the {sec}, {sec}s, {min}m or {min}m{sec}s.\n\nEx.\n\n    $ exclock -t 3\n    $ exclock -t 3s\n    $ exclock -t 2m\n    $ exclock -t 2m3s\n\nHow to flexibly set the alarm\n-----------------------------\n\nEnter\n\n    $ exclock {clock-filename}\n\nformat command. Although {clock-filename} can be omitted as descrived\nbelow.\n\nclock-file should be a file in json5 format.\n\nOfficial page for json5 format is [Here](https://json5.org/).\n\nclock file format\n-----------------\n\n    {\n      "title": "title(optional)",\n      "sounds": {\n        "time1": {\n          "message": "message1",\n          "sound_filename": "sound_filename1",\n        },\n        "time2":{\n        "message": "message2",\n        "sound_filename": "sound_filename2",\n        },\n        ...\n      },\n      "show_message": show_message(optional),\n      "loop": loop_number(optional)\n    }\n\n-   title(Optional): string which be used for notification. Then the\n    property is computed from clock-filename if this option is not\n    indicated.\n-   sounds: dictionary from time to dictionary which includes message\n    and sound\\_filename.\n    -   time format is "{sec}", "{sec}s", "{min}m" or "{min}m{sec}s"\n        format.\n    -   message is a string which be used for notification and terminal\n        output. Then message is replaced by "{count}" to number of how\n        many times execute.\n    -   sound\\_filename is a string which be used for play the sound.\n-   show_message(Option): bool of show_message using xmessage or terminal-notifier\n-   loop(Option): number of iterations for above clock timer. If this is\n    nil, this means repeatation a number of times. Default value is 1.\n\nThere are sample files in [sample dir in\ngitlab](https://gitlab.com/yassu/exclock/-/tree/master/exclock/assets/clock).\n\nHow to omit clock filename\n--------------------------\n\nClock filename can be omitted for some case.\n\nRules are\n\n-   If extension of clock filename is .json5, extension can be\n    omitted(ex: pomodoro.json5 =&gt; pomodoro).\n-   If dir is in the specified directory(\\~/.config/exclock/clock/ or\n    environment variable EXCLOCK\\_CLOCK\\_DIR), dir is omitted (ex:\n    \\~/.config/exclock/clock/abc.json5 =&gt; abc).\n-   Buitin clock file can be accessed. There are in [sample dir in\n    gitlab]() (ex: 3m or pomodoro).\n\nHow to omit sound filename\n--------------------------\n\nSound filename can be omitted for some case.\n\nRules are\n\n-   If dir is in the specified directory(\\~/.config/exclock/sound/ or\n    environment variable EXCLOCK\\_SOUND\\_DIR), dir is omitted (ex:\n    \\~/.config/exclock/sound/abc.mp3 =&gt; abc.mp3).\n-   Buitin sound file can be accessed. There are in [sample sound dir in\n    gitlab](https://gitlab.com/yassu/exclock/-/tree/master/exclock/assets/sound)\n    (ex: silent.mp3 or ring.mp3).\n\nLICENSE\n-------\n\n[Apache 2.0](https://gitlab.com/yassu/exclock/blob/master/LICENSE)\n',
    'author': 'yassu',
    'author_email': 'yasu0320.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/yassu/exclock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
