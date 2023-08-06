# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cookiecutter_cruft_poetry_tox_pre_commit_ci_cd_instance']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'structlog-sentry-logger>=0.5.6,<0.6.0']

entry_points = \
{'console_scripts': ['cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance '
                     '= '
                     'cookiecutter_cruft_poetry_tox_pre_commit_ci_cd_instance.__main__:main']}

setup_kwargs = {
    'name': 'cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance',
    'version': '0.0.0',
    'description': 'Cookiecutter Cruft Poetry Tox Pre Commit Ci Cd Instance',
    'long_description': "cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance\n==============================\n\n![CI](https://github.com/TeoZosa/cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance/workflows/CI/badge.svg)\n[![codecov](https://codecov.io/gh/TeoZosa/cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance/branch/master/graph/badge.svg?token=3HF21UWY82)](undefined)\n![License](https://img.shields.io/github/license/TeoZosa/cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance?style=plastic)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance?style=plastic)\n![PyPI](https://img.shields.io/pypi/v/cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance?color=informational&style=plastic)\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![powered by semgrep](https://img.shields.io/badge/powered%20by-semgrep-1B2F3D?labelColor=lightgrey&link=https://semgrep.dev/&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAA0AAAAOCAYAAAD0f5bSAAAABmJLR0QA/gD+AP+cH+QUAAAACXBIWXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH5AYMEy0l8dkqrQAAAvFJREFUKBUB5gIZ/QEAAP8BAAAAAAMG6AD9+hn/GzA//wD//wAAAAD+AAAAAgABAQDl0MEBAwbmAf36GQAAAAAAAQEC9QH//gv/Gi1GFQEC+OoAAAAAAAAAAAABAQAA//8AAAAAAAAAAAD//ggX5tO66gID9AEBFSRxAgYLzRQAAADpAAAAAP7+/gDl0cMPAAAA+wAAAPkbLz39AgICAAAAAAAAAAAs+vU12AEbLz4bAAAA5P8AAAAA//4A5NDDEwEBAO///wABAQEAAP//ABwcMD7hAQEBAAAAAAAAAAAaAgAAAOAAAAAAAQEBAOXRwxUAAADw//8AAgAAAAD//wAAAAAA5OXRwhcAAQEAAAAAAAAAAOICAAAABP3+/gDjzsAT//8A7gAAAAEAAAD+AAAA/wAAAAAAAAAA//8A7ePOwA/+/v4AAAAABAIAAAAAAAAAAAAAAO8AAAABAAAAAAAAAAIAAAABAAAAAAAAAAgAAAD/AAAA8wAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAA8AAAAEAAAA/gAAAP8AAAADAAAA/gAAAP8AAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAA7wAAAPsAAAARAAAABAAAAP4AAAAAAAAAAgAAABYAAAAAAAAAAAIAAAD8AwICAB0yQP78/v4GAAAA/wAAAPAAAAD9AAAA/wAAAPr9//8aHTJA6AICAgAAAAD8AgAAADIAAAAAAP//AB4wPvgAAAARAQEA/gEBAP4BAQABAAAAGB0vPeIA//8AAAAAAAAAABAC+vUz1QAAAA8AAAAAAwMDABwwPu3//wAe//8AAv//ABAcMD7lAwMDAAAAAAAAAAAG+vU0+QEBAvUB//4L/xotRhUBAvjqAAAAAAAAAAAAAQEAAP//AAAAAAAAAAAA//4IF+bTuuoCA/QBAQAA/wEAAAAAAwboAP36Gf8bMD//AP//AAAAAP4AAAACAAEBAOXQwQEDBuYB/foZAAAAAAD4I6qbK3+1zQAAAABJRU5ErkJggg==)](https://semgrep.dev/)\n[![Dependabot](https://api.dependabot.com/badges/status?host=github&repo=TeoZosa/cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance)](https://dependabot.com/)\n\n\nOverview\n------------------------------\n- TODO\n\nFeatures\n------------\n- TODO\n\nRequirements\n------------\n- TODO\n\n------------\n\nTable of Contents\n<!-- toc -->\n\nInstallation\n==============================\nYou can install Cookiecutter Cruft Poetry Tox Pre Commit Ci Cd Instance via [pip](https://pip.pypa.io/):\n ```shell script\npip install cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance\n```\n\nUsage\n==============================\n- TODO\n    - High-level usage overview\n------------\n- TODO\n    - Step 0 description\n```python\nimport cookiecutter_cruft_poetry_tox_pre_commit_ci_cd_instance\n\n# TODO\n```\n\nDevelopment\n==============================\n\nFor convenience, many of the below processes are abstracted away and encapsulated in\nsingle [`make`](https://www.gnu.org/software/make/) targets.\n\nTip: invoking `make` without any arguments will display auto-generated\ndocumentation on available commands.\n\nPackage and Dependencies Installation\n------------\n\n**Note**: `poetry` is a required dependency.\n\nTo install the package and all dev dependencies, run:\n```shell script\nmake provision_environment\n```\n\nTesting\n------------\n\nWe use [`tox`](https://tox.readthedocs.io/en/latest/) for our automation framework\n  and [`pytest`](https://docs.pytest.org/en/stable/) for our testing framework.\n  To invoke the tests, run:\n\n```shell script\nmake test\n```\n\nCode Quality\n------------\n\nWe are using [`pre-commit`](https://pre-commit.com/) for our code quality\nstatic analysis automation and management framework. To invoke the analyses and\nauto-formatting over all version-controlled files, run:\n\n```shell script\nmake lint\n```\n\n**Note**: CI will fail if either testing or code quality fail, so it is recommended to automatically\n  run the above locally prior to every commit that is pushed.\n\n### Automate via Git Pre-Commit Hooks\n\nTo automatically run code quality validation on every commit (over to-be-committed\nfiles), run:\n\n```shell script\nmake install-pre-commit-hooks\n```\n\n**Note**: This will prevent commits if any single pre-commit hook fails (unless it\nis allowed to fail) or a file is modified by an auto-formatting job; in the\nlatter case, you may simply repeat the commit and it should pass.\n\nSummary\n==============================\n- TODO\n\nFurther Reading\n==============================\n- TODO\n\n---\n\nLegal\n==============================\n\nLicense\n-------\n\ncookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance is licensed under the Apache License, Version 2.0.\nSee [LICENSE](./LICENSE) for the full license text.\n\n\nCredits\n-------\n\nThis project was generated from\n[`@TeoZosa`'s](https://github.com/TeoZosa)\n[`cookiecutter-cruft-poetry-tox-pre-commit-ci-cd`](https://github.com/TeoZosa/cookiecutter-cruft-poetry-tox-pre-commit-ci-cd)\ntemplate.\n",
    'author': 'Teo Zosa',
    'author_email': 'teo@sonosim.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TeoZosa/cookiecutter-cruft-poetry-tox-pre-commit-ci-cd-instance',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
