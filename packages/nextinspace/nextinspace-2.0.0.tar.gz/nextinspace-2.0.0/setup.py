# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nextinspace', 'nextinspace.cli']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0', 'requests>=2.24,<3.0']

entry_points = \
{'console_scripts': ['nextinspace = nextinspace.cli.console:run']}

setup_kwargs = {
    'name': 'nextinspace',
    'version': '2.0.0',
    'description': 'Never miss a launch.',
    'long_description': '# Nextinspace\n\n<p align="center">\n<a href="https://github.com/The-Kid-Gid/nextinspace/actions?query=workflow%3ATest"><img alt="Test" src="https://github.com/The-Kid-Gid/nextinspace/workflows/Test/badge.svg"></a>\n<a href=\'https://nextinspace.readthedocs.io/en/feat-v2/?badge=feat-v2\'><img src=\'https://readthedocs.org/projects/nextinspace/badge/?version=feat-v2\'alt=\'Documentation Status\' /></a>\n<a href="https://codecov.io/gh/The-Kid-Gid/nextinspace">\n<img src="https://codecov.io/gh/The-Kid-Gid/nextinspace/branch/master/graph/badge.svg?token=OCYIVWG21F"/></a>\n<a href="https://pypi.org/project/nextinspace"><img alt="PyPI" src="https://img.shields.io/pypi/v/nextinspace?color=lgreen&label=PyPI%20Package"></a>\n<a href="https://github.com/The-Kid-Gid/nextinspace/releases/latest"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/The-Kid-Gid/nextinspace?label=Github%20Release"></a>\n<a href="https://pepy.tech/project/nextinspace"><img alt="Downloads" src="https://static.pepy.tech/personalized-badge/nextinspace?period=total&units=none&left_color=grey&right_color=green&left_text=Downloads"></a>\n<a href="https://img.shields.io/pypi/pyversions/nextinspace"><img alt="Pyversions" src="https://img.shields.io/pypi/pyversions/nextinspace"></a>\n<a href="https://www.gnu.org/licenses/gpl-3.0"><img alt="License: GPL v3" src="https://img.shields.io/badge/License-GPLv3-blue.svg"></a>\n</p>\n\n> *“Never miss a launch.”*\n\n## Overview\n\nA command-line tool for seeing the latest in space. Nextinspace also supports use as a Python library, so you can integrate it into your application. You can also get data printed to the terminal in JSON, which can be piped into another program.\n\n[Features](#features) • [Installation and Documentation](#installation-and-documentation) • [Using the Nextinspace Public API](#using-the-nextinspace-public-api) • [Using Nextinspace in Shell Scripting](#using-nextinspace-in-shell-scripting) • [CLI Reference](#cli-reference) • [Credits](#credits)\n\n## Features\n\n- **Get the next *n* items:** Nextinspace by default prints the closest upcoming item, but you can request as many items as the [LL2 API](https://thespacedevs.com/llapi)\nwill provide.\n\n- **Filter by type:** Nextinspace allows you to filter upcoming-related by type. You can choose to only see `launches`, only see `events`, or both.\n\n- **Toggle the verbosity:** Nextinspace offers quiet, normal, and verbose modes. With `--quiet`, you can get a quick overview of upcoming items.\nWith `--verbose`, you can see all of the important details such as description and launcher.\n\n- **JSON output:** Nextinspace provides a `--json` flag for output in JSON format. This can be parsed with tools like [`jq`](https://github.com/stedolan/jq).\n\n- **Pretty printing:** Nextinspace prints upcoming items in formatted panels and with colored text.\n\n<p align="center">\n  <img height=550 src="https://raw.githubusercontent.com/The-Kid-Gid/nextinspace/master/img/demo.svg" />\n</p>\n\n## Installation and Documentation\n\nNextinspace can be installed using `pip`:\n\n```bash\npip install nextinspace\n```\n\nIt can also be installed directly from Github:\n\n```bash\npip install git+https://github.com/The-Kid-Gid/nextinspace\n```\n\nOr you can use your favorite package manager:\n\n```bash\n# Arch Linux\nyay -S nextinspace\n\n# Nix\nnix-env -iA nixpkgs.nextinspace\n```\n\nDocumentation can be found at [Read the Docs](https://nextinspace.readthedocs.io).\n\n## Using the Nextinspace Public API\n\nNextinspace defines a [public API](https://nextinspace.readthedocs.io/en/stable/nextinspace.html) of functions and classes that you can use in your code.\n\n```python\n>>> import nextinspace\n```\n\n### Example 1: Get the next upcoming space-related thing\n\n```python\n>>> next_in_space = nextinspace.nextinspace(1)\n>>> next_in_space\n(nextinspace.Event(\'Starship SN9 Pressure Test\', \'Boca Chica, Texas\', datetime.datetime(2020, 12, 28, 21, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400), \'EST\')), \'SpaceX has conducted a pressure test on Starship SN9.\', \'Ambient Pressure Test\'),)\n>>> print(next_in_space[0].date)\n2020-12-28 21:00:00-05:00\n```\n\n### Example 2: Get the next two upcoming events\n\n```python\n>>> next_2_events = nextinspace.next_event(2)\n>>> next_2_events\n(nextinspace.Event(\'Starship SN9 Pressure Test\', \'Boca Chica, Texas\', datetime.datetime(2020, 12, 28, 21, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400), \'EST\')), \'SpaceX has conducted a pressure test on Starship SN9.\', \'Ambient Pressure Test\'), nextinspace.Event(\'Starship SN9 Cryoproof Test\', \'Boca Chica, Texas\', datetime.datetime(2020, 12, 29, 18, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400), \'EST\')), \'SpaceX will likely conduct a cryoproof test on Starship SN9. This is the first cryo test performed on the vehicle.\', \'Cryoproof Test\'))\n>>> next_2_events[1].name\n\'Starship SN9 Cryoproof Test\'\n```\n\n### Example 3: Get the next upcoming launch\n\n```python\n>>> next_space_launch = nextinspace.next_launch(1)\n>>> next_space_launch\n(nextinspace.Launch(\'Soyuz STA/Fregat | CSO-2\', \'Soyuz Launch Complex, Kourou, French Guiana\', datetime.datetime(2020, 12, 29, 11, 42, 7, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400), \'EST\')), \'The CSO-2 (Composante Spatiale Optique-2) satellite is the second of three new-generation high-resolution optical imaging satellites for the French military, replacing the Helios 2 spy satellite series.\', \'Government/Top Secret\', None),)\n>>> print(next_space_launch[0].launcher)\nNone\n```\n\n### Example 4: Get the next two upcoming launches and their launchers\n\n```python\n>>> next_2_launches = nextinspace.next_launch(2, include_launcher=True)\n>>> next_2_launches\n(nextinspace.Launch(\'Soyuz STA/Fregat | CSO-2\', \'Soyuz Launch Complex, Kourou, French Guiana\', datetime.datetime(2020, 12, 29, 11, 42, 7, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400), \'EST\')), \'The CSO-2 (Composante Spatiale Optique-2) satellite is the second of three new-generation high-resolution optical imaging satellites for the French military, replacing the Helios 2 spy satellite series.\', \'Government/Top Secret\', nextinspace.Launcher(\'Soyuz STA/Fregat\', 7020, 2810, None, 312, 3, 46.3, 8, 8, 0, datetime.datetime(2011, 12, 16, 19, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400), \'EST\')))), nextinspace.Launch(\'Falcon 9 Block 5 | Türksat 5A\', \'Space Launch Complex 40, Cape Canaveral, FL, USA\', datetime.datetime(2021, 1, 4, 20, 27, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400), \'EST\')), \'Türksat 5A is the first of two Turkish next generation communications satellites, which will be operated by Türksat for commercial and military purposes.\', \'Communications\', nextinspace.Launcher(\'Falcon 9 Block 5\', 22800, 8300, 7607, 549, 2, 70.0, 47, 47, 0, datetime.datetime(2018, 5, 10, 20, 0, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000), \'EDT\')))))\n>>> next_2_launches[0].launcher.failed_launches\n0\n```\n\n## Using Nextinspace in Shell Scripting\n\nNextinspace is capable of outputting structured JSON data that can be parsed by the likes of [`jq`](https://github.com/stedolan/jq). As such, you can do something like this:\n\n```bash\n❯ next_3_in_space=$(nextinspace 3 --verbose --json)\n❯ echo $next_3_in_space | jq "."\n[\n  {\n    "type": "launch",\n    "name": "Soyuz STA/Fregat | CSO-2",\n    "location": "Soyuz Launch Complex, Kourou, French Guiana",\n    "date": "2020-12-29T16:42:07Z",\n    "description": "The CSO-2 (Composante Spatiale Optique-2) satellite is the second of three new-generation high-resolution optical imaging satellites for the French military, replacing the Helios 2 spy satellite series.",\n    "subtype": "Government/Top Secret",\n    "launcher": {\n      "name": "Soyuz STA/Fregat",\n      "payload_leo": 7020,\n      "payload_gto": 2810,\n      "liftoff_thrust": null,\n      "liftoff_mass": 312,\n      "max_stages": 3,\n      "height": 46.3,\n      "successful_launches": 8,\n      "consecutive_successful_launches": 8,\n      "failed_launches": 0,\n      "maiden_flight_date": "2011-12-17"\n    }\n  },\n  {\n    "type": "event",\n    "name": "Starship SN9 Cryoproof Test",\n    "location": "Boca Chica, Texas",\n    "date": "2020-12-29T23:00:00Z",\n    "description": "SpaceX will likely conduct a cryoproof test on Starship SN9. This is the first cryo test performed on the vehicle.",\n    "subtype": "Cryoproof Test"\n  },\n  {\n    "type": "event",\n    "name": "SLS Green Run Hot Fire",\n    "location": "Stennis Space Center, Mississippi",\n    "date": "2020-12-31T00:00:00Z",\n    "description": "The core stage of the Space Launch System will undergo the final \'Green Run\' test, where the core stage will be fired for 8 minutes, demonstrating performance similar to an actual launch.",\n    "subtype": "Static Fire"\n  }\n]\n❯ echo $next_3_in_space | jq ".[].name"\n"Soyuz STA/Fregat | CSO-2"\n"Starship SN9 Cryoproof Test"\n"SLS Green Run Hot Fire"\n```\n\nThe structure of the JSON outputted by nextinspace is basically demonstrated in the example above.\nThe structure and values of the data reflect the relationships between the `Launch`, `Event`, and `Launcher` classes, with a few notable exceptions:\n\n- **The `type` attribute:** The `type` attribute of Nextinspace `Event` and `Launch` objects is actually stored in the `subtype` key. The `type` key actually holds the class of the Nextinspace object represented in the JSON object (either `launch` or `event`).\n- **The `date` key:** Internally, Nextinspace stores dates and times in local time, but for JSON output Nextinspace converts date and time values to UTC. Also, Nextinspace outputs date and time values in [ISO 8601 format](https://www.iso.org/iso-8601-date-and-time-format.html).\n\n## CLI Reference\n\n```\n❯ nextinspace --help\nusage: nextinspace [-h] [-e | -l] [-v | -q] [--version] [number of items]\n\nNever miss a launch.\n\npositional arguments:\n  number of items      The number of items to display.\n\noptional arguments:\n  -h, --help           show this help message and exit\n  -e, --events-only    Only show events. These are typically not covered by standard launches. These events could be spacecraft landings, engine tests, or spacewalks.\n  -l, --launches-only  Only display orbital and suborbital launches. Generally these will be all orbital launches and suborbital launches which aim to reach “space” or the Karman line.\n  -v, --verbose        Display additional details about launches.\n  -q, --quiet          Only display name, location, date, and type.\n  --version            show program\'s version number and exit\n\n```\n\n## Credits\n\nThis project would not have been possible without the [Launch Library 2 API](https://thespacedevs.com/llapi). Please consider [sponsoring them on Patreon](https://www.patreon.com/TheSpaceDevs).\n',
    'author': 'Gideon Shaked',
    'author_email': 'gideonshaked@gmail.com',
    'maintainer': 'Gideon Shaked',
    'maintainer_email': 'gideonshaked@gmail.com',
    'url': 'https://github.com/The-Kid-Gid/nextinspace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
