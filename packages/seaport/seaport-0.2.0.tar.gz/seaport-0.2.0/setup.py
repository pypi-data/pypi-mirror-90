# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seaport']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['seaport = seaport.console:seaport']}

setup_kwargs = {
    'name': 'seaport',
    'version': '0.2.0',
    'description': 'A more mighty port bump',
    'long_description': '# 🌊 seaport\n\n*A more mighty `port bump` for MacPorts!*\n\n| Test Status | [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/harens/seaport/Tests?logo=github&style=flat-square)](https://github.com/harens/seaport/actions?query=workflow%3ATests) [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/harens/seaport/ShellCheck?label=ShellCheck&logo=github%20actions&logoColor=white&style=flat-square)](https://github.com/harens/seaport/actions?query=workflow%3AShellCheck) [![Codecov](https://img.shields.io/codecov/c/github/harens/seaport?logo=codecov&style=flat-square)](https://codecov.io/gh/harens/seaport)  |\n|:--|:--|\n| __Version Info__ | [![PyPI](https://img.shields.io/pypi/v/seaport?logo=pypi&logoColor=white&style=flat-square)](https://pypi.org/project/seaport/) [![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/harens/seaport?logo=github&style=flat-square)](https://github.com/harens/seaport/releases) [![PyPI - Downloads](https://img.shields.io/pypi/dm/seaport?logo=python&logoColor=white&style=flat-square)](https://pypi.org/project/seaport/) |\n| __Code Analysis__ |[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/harens/seaport?logo=lgtm&style=flat-square)](https://lgtm.com/projects/g/harens/seaport/) [![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/harens/seaport?logo=code%20climate&style=flat-square)](https://codeclimate.com/github/harens/seaport) [![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/harens/seaport?logo=codefactor&style=flat-square)](https://www.codefactor.io/repository/github/harens/seaport) [![Codacy grade](https://img.shields.io/codacy/grade/8539131738c3433f8057e65aab21de03?logo=codacy&style=flat-square)](https://app.codacy.com/gh/harens/seaport/dashboard?branch=master)|\n\n## ✨ Features\n\n* __Automatically determines new version numbers and checksums__ for MacPorts portfiles.\n* __Copies the changes to your clipboard 📋__, and optionally __sends a PR to update them__.\n* Contains __additional checking functionality__, such as running tests, linting and installing the updated program.\n\n## 🤖 Example\n\n```\n> seaport gping\n👍 New version is 1.2.0-post\n🔻 Downloading from https://github.com/orf/gping/tarball/v1.2.0-post/gping-1.2.0-post.tar.gz\n🔎 Checksums:\nOld rmd160: 8b274132c8389ec560f213007368c7f521fdf682\nNew rmd160: 4a614e35d4e1e496871ee2b270ba8836f84650c6\nOld sha256: 1879b37f811c09e43d3759ccd97d9c8b432f06c75a27025cfa09404abdeda8f5\nNew sha256: 1008306e8293e7c59125de02e2baa6a17bc1c10de1daba2247bfc789eaf34ff5\nOld size: 853432\nNew size: 853450\n⏪️ Changing revision numbers\nNo changes necessary\n📋 The contents of the portfile have been copied to your clipboard!\n```\n\n## ⬇️ Install\n\nNote that if installing from PyPi or building from source, [MacPorts](https://www.macports.org/) needs to already be installed, and [GitHub CLI](https://cli.github.com/) is required if using the `--pr` flag.\n\n### Homebrew 🍺\n\nBinary bottles are available for x86_64_linux, catalina and big_sur.\n\n```\nbrew install harens/tap/seaport\n```\n\n### PyPi 🐍\n\n```\npip install seaport\n```\n\n## 💻 Usage\n\n```txt\n> seaport --help\nUsage: seaport [OPTIONS] NAME\n\n  Bumps the version number and checksum of NAME, and copies the result to\n  your clipboard\n\nOptions:\n  --version                 Show the version and exit.\n  --bump TEXT               The new version number\n  --pr PATH                 Location for where to clone the macports-ports\n                            repo\n\n  --test / --no-test        Runs port test\n  --lint / --no-lint        Runs port lint --nitpick\n  --install / --no-install  Installs the port and allows testing of basic\n                            functionality\n\n  --help                    Show this message and exit.\n```\n\n### 🚀 Use of sudo\n\nSudo is only required if `--test`, `--lint` or `--install` are specified, and it will be asked for during runtime. This is since the local portfile repo needs to be modified to be able to run the relevant commands.\n\nAny changes made to the local portfile repo are reverted during the cleanup stage.\n\n## 🔨 Contributing\n\nAny change, big or small, that you think can help improve this action is more than welcome 🎉.\n\nAs well as this, feel free to open an issue with any new suggestions or bug reports. Every contribution is appreciated.\n\n## 📒 Notice of Non-Affiliation and Disclaimer\n\n<img src="https://avatars2.githubusercontent.com/u/4225322?s=280&v=4" align="right"\n     alt="MacPorts Logo" width="150">\n\nThis project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with the MacPorts Project, or any of its subsidiaries or its affiliates. The official MacPorts Project website can be found at <https://www.macports.org>.\n\nThe name MacPorts as well as related names, marks, emblems and images are registered trademarks of their respective owners.\n',
    'author': 'harens',
    'author_email': 'harensdeveloper@gmail.com',
    'maintainer': 'harens',
    'maintainer_email': 'harensdeveloper@gmail.com',
    'url': 'https://github.com/harens/seaport',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
