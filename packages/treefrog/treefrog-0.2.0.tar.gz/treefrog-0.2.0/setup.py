# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['treefrog']

package_data = \
{'': ['*']}

install_requires = \
['melee>=0.20.2,<0.21.0',
 'pony>=0.7.13,<0.8.0',
 'py-slippi>=1.6.1,<2.0.0',
 'seaborn>=0.11.0,<0.12.0']

entry_points = \
{'console_scripts': ['treefrog = treefrog.__main__:main']}

setup_kwargs = {
    'name': 'treefrog',
    'version': '0.2.0',
    'description': 'Organize the Slippi game files in your filesystem according to their attributes',
    'long_description': '# `treefrog`\n\n[![](https://img.shields.io/pypi/v/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)\n[![](https://img.shields.io/pypi/dw/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)\n[![](https://img.shields.io/pypi/pyversions/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)\n[![](https://img.shields.io/pypi/format/treefrog.svg?style=flat)](https://pypi.org/pypi/treefrog/)\n[![](https://img.shields.io/pypi/l/treefrog.svg?style=flat)](https://github.com/dawsonbooth/treefrog/blob/master/LICENSE)\n\n## Description\n\nOrganize the Slippi game files in your filesystem according to their attributes.\n\n## Installation\n\nWith [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.\n\n```bash\npip install treefrog\n```\n\n## Usage\n\n### Module\n\nCurrently, the package supports organizing the files according to a supplied hierarchy, flattening the files against the supplied root folder, and renaming all the files according to their attributes. Each of these methods takes in an optional `show_progress` boolean parameter which, when true, invokes the presentation of a progress bar indicating the processing of all the game files according to the method.\n\n#### Organize\n\nThe `organize` method serves the purpose of moving each game file found (deeply or otherwise) under the root folder to its proper location according to the supplied ordering. If no ordering is given, then treefrog will use the default ordering found in the `treefrog.hierarchy` module. Here is a simple example of calling this method:\n\n```python\nfrom treefrog import Hierarchy, Tree\n\ntree = Tree("slp/", "DTB#566") # Root folder and user\'s netplay code\n\nordering = (\n    {\n        Hierarchy.Member.YEAR,\n        Hierarchy.Member.MONTH\n    },\n    {\n        Hierarchy.Member.OPPONENT_CODE\n    },\n    {\n        Hierarchy.Member.CHARACTER,\n        Hierarchy.Member.OPPONENT_CHARACTER\n    },\n    {\n        Hierarchy.Member.STAGE\n    },\n) # An iterable of the desired levels of the hierarchy\n\ntree.organize(ordering) # Organize the files into subfolders according to the supplied attributes\n\ntree.resolve() # Physically adjust the filesystem to reflect the above change\n```\n\nThis package has some intelligence in place for naming the folders at one of these levels according to the combination of members that are provided. For example, if a level only consists of the `CHARACTER` and `OPPONENT_CHARACTER` members, the folders at that level will be named according to the convention: `CHARACTER vs OPPONENT_CHARACTER`.\n\nFeel free to provide your own logic for formatting the names of the folders at a particular level with a corresponding iterable of functions:\n\n```python\nfrom treefrog import Hierarchy, Tree\nfrom treefrog.format import default_format, character_name\n\ntree = Tree("slp/", "DTB#566")\n\nordering = (\n    {\n        Hierarchy.Member.YEAR,\n        Hierarchy.Member.MONTH\n    },\n    {\n        Hierarchy.Member.OPPONENT_CODE\n    },\n    {\n        Hierarchy.Member.CHARACTER,\n        Hierarchy.Member.OPPONENT_CHARACTER\n    },\n    {\n        Hierarchy.Member.STAGE\n    },\n)\n\nformatting = (\n    lambda year, month: f"{default_format(**{Hierarchy.Member.MONTH: month})} {year}",\n    None,\n    lambda character, opponent_character: f"{character_name(character)} VS {character_name(opponent_character)}",\n    None\n)\n\ntree.organize(ordering).resolve()\n```\n\nThe game attributes corresponding to the ordering will be passed as keyword arguments into the function you provide, so be sure to use correct argument names. If `None` formatting is supplied for a level, then treefrog will resort to the `default_format` function.\n\nFurther, notice that you can use cascading methods to simplify your programming. Each of the methods `organize`, `flatten`, and `rename` will return a reference to the instance object on which it was called. Something like this: `tree.organize().rename().resolve()` will organize the game files, rename the files, and resolve the physical paths of the files in the order they are called.\n\n#### Flatten\n\nThe `flatten` method serves the simple purpose of moving each game file found (deeply or otherwise) under the root folder back to the root folder itself. Here\'s an example of what calling this method may look like:\n\n```python\nfrom treefrog import Tree\n\ntree = Tree("slp/", "DTB#566")\ntree.flatten().resolve()\n```\n\n#### Rename\n\nThe `rename` method simply renames each game file according to its attributes. Without a rename function supplied, treefrog will use the `default_rename` function found in the `treefrog.format` module. Alternatively, you may provide your own rename function as shown below:\n\n```python\nfrom treefrog import Hierarchy, Tree\nfrom treefrog.format import character_name\n\ndef rename(code, name, character, opponent_code, opponent_name, opponent_character, **kwargs):\n    return " vs ".join((\n        f"[{code}] {name} ({character_name(character)})",\n        f"[{opponent_code}] {opponent_name} ({character_name(opponent_character)})"\n    )) + ".slp"\n\nTree("slp/", "DTB#566").rename(rename_func=rename).resolve()\n```\n\nAll game attributes will be passed as keyword arguments into the function you provide, so be sure to catch the ones you don\'t use with `**kwargs` or you\'ll get an error!\n\n### Command-Line\n\nThis is also command-line program, and can be executed as follows:\n\n```txt\npython -m treefrog [-h] -c NETPLAY_CODE [-o | -f] [-r] [-p] ROOT_FOLDER\n```\n\nPositional arguments:\n\n```txt\n  ROOT_FOLDER           Slippi folder root path\n```\n\nOptional arguments:\n\n```txt\n  -h, --help            show this help message and exit\n  -c NETPLAY_CODE, --netplay-code NETPLAY_CODE\n                        Netplay code (e.g. DTB#566)\n  -o, --organize        Whether to organize the folder hierarchy\n  -f, --flatten         Whether to flatten the folder hierarchy\n  -r, --rename          Whether to rename the files according to the game attributes\n  -p, --show-progress   Whether to show a progress bar\n```\n\nFor example, the following command will organize all the game files under the `slp` directory.\n\n```bash\npython -m treefrog "slp" -c "DTB#566" -op\n```\n\nFeel free to [check out the docs](https://dawsonbooth.com/treefrog/) for more information.\n\n## License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/treefrog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
