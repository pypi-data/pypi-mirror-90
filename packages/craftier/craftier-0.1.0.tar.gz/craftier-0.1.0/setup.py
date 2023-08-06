# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['craftier', 'craftier.refactors']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'click_pathlib>=2020.3.13,<2021.0.0',
 'libcst>=0.3.15,<0.4.0',
 'loguru>=0.5.3,<0.6.0',
 'typing_extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['craftier = craftier.cli:app']}

setup_kwargs = {
    'name': 'craftier',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Craftier\n\n```\n  ___  ____   __   ____  ____  __  ____  ____ (pre-\xce\xb1)\n / __)(  _ \\ / _\\ (  __)(_  _)(  )(  __)(  _ \\\n( (__  )   //    \\ ) _)   )(   )(  ) _)  )   /\n \\___)(__\\_)\\_/\\_/(__)   (__) (__)(____)(__\\_)\n\n      Your personal Python code reviewer\n```\n\n## What is it?\nCraftier is a framework to easily writing Python code refactors. In the near\nfuture it will also come with a set of predefined refactoring rules.\n\nIt is based on `libcst` and simplifies the use of its API by letting you write\nrefactors just by writing Python code.\n\nIt also preserves relevant comments and ensures the modified code is correct, by\nadding required parentheses.\n\n## Getting started\nAfter installing with `pip install craftier`, you can run the default rules with\n`craftier refactor <python files>`.\n\n## Configuration\nBy default we look for a `.craftier.ini`, if none is found a default\nconfiguration will be used.\n\nYou can also specify the config file with `--config CONFIG_PATH`\n\n### Config format\n\n```ini\n[craftier]\npackages=craftier.refactors,\nexcluded=A,\n         B\n```\n\n## Writing your own rules\n\nAs simple as:\n\n```py\nimport craftier\n\nclass SquareTransformer(craftier.CraftierTransformer):\n    def square_before(self, x):\n        x * x\n\n    def square_after(self, x):\n        x ** 2\n\n\nclass IfTrueTransformer(craftier.CraftierTransformer):\n    def if_true_before(self, x, y):\n        x if True else y\n\n    def if_true_after(self, x):\n        x\n```\n\nTODO: write about custom matchers and type declarations\n\n# Roadmap and TODOs\n* Support multiple expressions in a transformer\n* Add support for statements \n* Complete set of refactorings\n* Add support for typing metadata\n* Generate RE2 filtering based on expressions. This could be used to prefilter\n  the list of files and to test the patterns either in codebase search tools\n  like https://grep.app\n* Extensive validation testing\n\n## Limitations\nThis is a work in progress, and some edges are rough.\n\nGiven that we match code based on actual Python code, some refactorings are not\neasily expressed or may not even be expressible at all.\n\n## History\nTODO: write how I came up with the idea.\n\n### Name\nOriginally I wanted to name this package `pythonista`, but unfortunately someone\nsquatted the name (along with several others) and the name was not released\naccording to procedure. Furthermore, the issue was locked.\n\nThat gave me a chance of rethinking the name, so I started with anagrams of the\nword `refactor`, which was of course unsuccessful. So after some\nexperimentation I replaced the letter `o` with an `i`, giving `refactir`, which\nis an anagram of the word `craftier`.\n\nI like that name, because is like a "refactoring" of the word `refactor`, and\n`craftier` conveys the actual use case of the tool.\n\nBonus: the name sounds somewhat like my surname.',
    'author': 'Sebastian Kreft',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sk-/craftier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
