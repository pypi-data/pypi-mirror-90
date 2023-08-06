# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['project_paths']
install_requires = \
['toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'project-paths',
    'version': '0.1.0.post0',
    'description': 'Access file paths from pyproject.toml',
    'long_description': 'project-paths\n=============\n\n![Lint and Test](https://github.com/eddieantonio/project-paths/workflows/Lint%20and%20Test/badge.svg)\n![PyPI](https://img.shields.io/pypi/v/project-paths)\n\nAccess file paths from `pyproject.toml`\n\n> Thanks to [@Madoshakalaka](https://github.com/madoshakalaka) for the idea!\n\n```toml\n# pyproject.toml\n[tool.project-paths]\nreadme = "README.md"\n```\n\n```python\n# app.py\nfrom project_paths import paths\n\n# paths.readme is a pathlib.Path object:\nprint(paths.readme.read_text())\n```\n\nInstall\n-------\n\n    pip install project-paths\n\n\nUsage\n-----\n\nDoes your application have a bunch of configurable file paths? Do you\nwish you just had one place to configure list them all?\n\n### Add paths to `[tool.project-paths]`\n\nWith this module, define your paths in your `pyproject.toml` file under\nthe `[tool.project-paths]` table:\n\n```toml\n[tool.project-paths]\ndocs = "path/to/my/docs"\nsettings = "path/to/my/settings.py"\nconfig = "/opt/path/to/my/config\n# Add as many paths as you want!\n```\n\nAnything string defined with `[tool.project-paths]` will be made\navailable. Relative paths are relative to `pyproject.toml`.\n\n### Access paths using `project_paths.paths.<path name>`\n\nNow you can access all the paths listed in `pyproject.toml` with\n`project_paths.paths`. Every path is returned as\na [`pathlib.Path`][pathlib] object:\n\n```python\nfrom project_paths import paths\n\nprint(paths.docs.glob("*.md"))\nassert paths.config.exists()\nexec(paths.settings.read_text())\n# Or anything you want!\n```\n\n\n### Caveats\n\nNames in `[tool.project-paths]` should be a valid Python identifier\nand the names **cannot** have a leading underscore. If a name has\na leading underscore, a warning is issued and the name is inaccessible:\n\n```toml\n[tool.project-paths]\n# BAD: paths that start with a \'_\' cannot be used\n_my_path = "path/to/wherever"\n# GOOD: path is a valid Python identifier!\nmy_path = "path/to/where\n```\n\n[pathlib]: https://docs.python.org/3/library/pathlib.html\n[tool-table]: https://www.python.org/dev/peps/pep-0518/#tool-table\n\n\nLicense\n-------\n\n2021 © Eddie Antonio Santos. MIT Licensed.\n',
    'author': 'Eddie Antonio Santos',
    'author_email': 'eddieantonio@hey.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eddieantonio/project-paths',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
