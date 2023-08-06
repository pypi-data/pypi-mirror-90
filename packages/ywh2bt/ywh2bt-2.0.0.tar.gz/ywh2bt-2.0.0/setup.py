# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ywh2bt',
 'ywh2bt.cli',
 'ywh2bt.cli.commands',
 'ywh2bt.core',
 'ywh2bt.core.api',
 'ywh2bt.core.api.formatter',
 'ywh2bt.core.api.models',
 'ywh2bt.core.api.trackers',
 'ywh2bt.core.api.trackers.github',
 'ywh2bt.core.api.trackers.jira',
 'ywh2bt.core.configuration',
 'ywh2bt.core.configuration.trackers',
 'ywh2bt.core.crypt',
 'ywh2bt.core.mixins',
 'ywh2bt.core.schema',
 'ywh2bt.core.serializers',
 'ywh2bt.core.state',
 'ywh2bt.core.synchronizer',
 'ywh2bt.core.tester',
 'ywh2bt.gui',
 'ywh2bt.gui.dialog',
 'ywh2bt.gui.widgets',
 'ywh2bt.gui.widgets.attribute',
 'ywh2bt.gui.widgets.thread']

package_data = \
{'': ['*'],
 'ywh2bt.gui': ['resources/icons/*',
                'resources/icons/types/*',
                'resources/icons/types/TrackerConfiguration/*',
                'resources/translations/*']}

install_requires = \
['PyGithub>=1.53,<2.0',
 'PySide2>=5.15.1,<6.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'html2text>=2020.1.16,<2021.0.0',
 'jira>=3.0a2,<4.0',
 'lxml>=4.5.2,<5.0.0',
 'markdown>=3.3.3,<4.0.0',
 'python-gitlab>=2.5.0,<3.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.24.0,<3.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'singledispatchmethod>=1.0,<2.0',
 'tomlkit>=0.7.0,<0.8.0',
 'typing-extensions',
 'yeswehack<1.0.0']

entry_points = \
{'console_scripts': ['ywh2bt = ywh2bt.cli.main:run',
                     'ywh2bt-gui = ywh2bt.gui.main:run']}

setup_kwargs = {
    'name': 'ywh2bt',
    'version': '2.0.0',
    'description': 'ywh2bt - YesWeHack to Bug Tracker',
    'long_description': '# ywh2bt\n\nywh2bt is a tool to integrate your bug tracking system(s) with [YesWeHack platform][YesWeHack-Platform].\nIt automatically creates issues in your bug tracking system for all your program\'s report,\nand add to the concerned reports the link to the issue.\n\nThis tool requires you to have "Use Apps API" right on [YesWeHack platform][YesWeHack-Platform],\nand a custom HTTP header value to put in your configuration. \nBoth of them can be obtained by e-mailing us at support@yeswehack.com.\n\n- [Features](#features)\n    - [Supported trackers](#supported-trackers)\n- [Requirements](#requirements)\n- [Installation](#installation)\n- [GUI](#gui)\n    - [Usage](#usage)\n    - [Screenshots](#screenshots)\n- [Command line](#command-line)\n    - [`ywh2bt`](#ywh2bt-1)\n        - [Commands](#commands)\n        - [Example usages](#example-usages)\n- [Supported configuration file formats](#supported-configuration-file-formats)\n- [Known limitations and specific behaviours](#known-limitations-and-specific-behaviours)\n- [Changelog](#changelog)\n- [Local development](#local-development)\n    - [Requirements](#requirements-1)\n    - [Installation](#installation-1)\n    - [Usage](#usage-1)\n\n## Features\n\n- synchronization from [YesWeHack platform][YesWeHack-Platform] to trackers:\n    - platform reports to tracker issues\n    - reports logs/comments to issues comments\n- creation, modification, synchronization, validation, conversion of configuration files through a GUI\n- validation of configuration files\n- format conversion of configuration files\n\n### Supported trackers\n\n- github\n- gitlab\n- jira / jiracloud\n\n## Requirements\n\n- `python` >= 3.7,<3.9\n- [`pip`](https://pip.pypa.io/en/stable/installing/)\n\n## Installation\n\n```sh\npip install ywh2bt\n```\n\n## GUI\n\nThe GUI provides assistance to create, modify and validate/test configurations. \nIt also allows synchronization with bug trackers.\n\nTo run it, simply type `ywh2bt-gui` in a shell.\n\n### Usage\n\n- Changes to the configuration can be made either in the configuration tab or in the "Raw" tab ; \n  changes made in one tab are automatically reflected in the other tab.\n- Hovering labels and buttons with the mouse pointer often reveals more information in a floating tooltip \n  or in the status bar.\n- A description of the schema of the configuration files is accessible via the "Help > Schema documentation" menu\n  or by clicking on the ![Icon for help button](doc/img/icon-help.png) button in the main toolbar.\n\n### Screenshots\n\n- [example.yml](doc/examples/example.yml) configuration:\n\n![Screenshot of GUI with loaded example file](doc/img/screenshot-gui-example.png)\n\n- [empty configuration](doc/img/screenshot-gui-new.png)\n\n## Command line\n\n### `ywh2bt`\n\nMain script used to execute synchronization, validate and test configurations.\n\nUsage: `ywh2bt [command]`. See `ywh2bt -h` or `ywh2bt [command] -h` for detailed help.\n\n#### Commands\n\n- `validate`: validate a configuration file (mandatory fields, data types, ...)\n- `test`: test the connection to the trackers\n- `convert`: convert a configuration file into another format\n- `synchronize` (alias `sync`): synchronize trackers with YesWeHack reports\n- `schema`: dump a schema of the structure of the configuration files in [Json-Schema][Json-Schema], markdown \n  or plaintext\n\n#### Example usages\n\nValidation:\n```sh\n$ ywh2bt validate \\\n    --config-file=my-config.yml \\\n    --config-format=yaml && echo OK\nOK\n```\n\nConversion (`yaml` to `json`):\n```sh\n$ ywh2bt convert \\\n    --config-file=my-config.yml \\\n    --config-format=yaml \\\n    --destination-file=/tmp/cfg.json \\\n    --destination-format=json\n```\n\nSynchronization:\n```sh\n$ ywh2bt synchronize --config-file=my-config.json --config-format=json\n[2020-12-21 10:20:58.881315] Starting synchronization:\n[2020-12-21 10:20:58.881608]   Processing YesWeHack "yeswehack1": \n[2020-12-21 10:20:58.881627]     Fetching reports for program "my-program": 2 report(s)\n[2020-12-21 10:21:08.341460]     Processing report #123 (CVE-2017-11882 on program) with "my-github": https://github.com/user/project/issues/420 (untouched ; 0 comment(s) added) | tracking status unchanged\n[2020-12-21 10:21:09.656178]     Processing report #96 (I found a bug) with "my-github": https://github.com/user/project/issues/987 (created ; 3 comment(s) added) | tracking status updated\n[2020-12-21 10:21:10.773688] Synchronization done.\n```\n\n## Supported configuration file formats\n\n- `yaml` (legacy)\n- `json`\n\nUse `ywh2bt schema -f json` to obtain a [Json-Schema][Json-Schema] describing the format.\nBoth `yaml` and `json` configuration files should conform to the schema. \n\n## Known limitations and specific behaviours\n\n- Apps API doesn\'t require TOTP authentication, even if corresponding user has TOTP enabled.  \n  However, on a secured program, information is limited for user with TOTP disabled, even in apps.  \n  As a consequence, to allow proper bug tracking integration on a secured program,\n  program consumer must have TOTP enabled and, in BTI configuration TOTP must be set to `false`.\n- References to a same uploaded attachment in different comments is not supported yet,\n  i.e., if an attachment is referenced (either displayed inline or as a link) in several comments,\n  only first one will be correctly handled.\n- Manually tracked reports (i.e., where a manager directly set the Tracking status to "tracked") \n  are also integrated in the tracker the way they are when a manager set "Ask for integration".\n- Since v2.0.0, unlike in previous versions, setting a tracked report back to "Ask for integration" \n  won\'t create a new issue in the tracker but update the existing one.\n\n## Changelog\n\n- v0.* to v2.0.0:\n    - behavior changes:\n        - reports logs can selectively be synchronized with the trackers:\n            - public comments\n            - private comments\n            - report details changes\n            - report status changes\n            - rewards\n        - a program can now only be synchronized with 1 tracker\n    - added support for JSON configuration files\n    - removed `ywh-bugtracker` command (use `ywh2bt synchronize`)\n    - added `ywh2bt` command:\n        - added `ywh2bt synchronize`:\n            - note: `ywh2bt synchronize --config-file FILE --config-format FORMAT` \n              is the equivalent of `ywh-bugtracker -n -f FILE` in v0.*\n        - added `ywh2bt validate`\n        - added `ywh2bt test`\n        - added `ywh2bt convert`\n        - added `ywh2bt schema`\n    - removed command line interactive mode\n    - added GUI via `ywh2bt-gui` command\n\n## Local development\n\n### Requirements\n\n- [`poetry`](https://python-poetry.org/) (`pip install poetry`)\n\n### Installation\n\n- `make install` (or `poetry install`): creates a virtualenv and install dependencies\n\n### Usage\n\nInstead of `ywh2bt [command]`, run commands using `poetry run ywh2bt [command]`.\n\nSame goes for `ywh2bt-gui`, run `poetry run ywh2bt-gui` instead.\n\n\n[YesWeHack-Platform]: https://www.yeswehack.com/\n[Json-Schema]: https://json-schema.org/specification.html',
    'author': 'm.honel',
    'author_email': 'm.honel@yeswehack.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yeswehack/ywh2bugtracker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<3.9',
}


setup(**setup_kwargs)
