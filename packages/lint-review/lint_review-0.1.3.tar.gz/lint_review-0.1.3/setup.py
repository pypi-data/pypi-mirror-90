# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lint_review']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.4.0,<9.0.0',
 'python-gitlab>=2.3.1,<3.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['lint_review = lint_review:main']}

setup_kwargs = {
    'name': 'lint-review',
    'version': '0.1.3',
    'description': 'Code review from any linter!',
    'long_description': "# lint_review\n\nPlug in any linter for a code review!\n\n## Features:\n- Creates merge request comments according to linter comments\n- Easy to expand to any linter - just pass `--custom-pattern` with a regex capturing the important parts of the linter errors.\n- Automatically resolves any comments that are no longer relevant.\n\n## Usage:\n- Create an [access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) with `api` premissions\n- Pipe your linter into `lint_review` as part of your merge request CI\n- Make a few mistakes (we all do)\n- Fix the comments as they pop up\n\n\n<details>\n<summary> Full interface </summary>\n\n```sh\nusage: lint_review [-h] [--linter {flake8,mypy}] --reviewer {dry,gitlab}\n                   [--custom_pattern CUSTOM_PATTERN] [--token TOKEN]\n                   [--project PROJECT] [--merge_request MERGE_REQUEST]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --linter {flake8,mypy}\n                        Name of the linter to use\n  --reviewer {dry,gitlab}\n                        The service used to review the code\n  --custom_pattern CUSTOM_PATTERN\n                        A custom regex pattern to capture comments. The\n                        pattern must have the named capture groups: {'line',\n                        'message', 'path'} and optionally col\n\ngitlab:\n  --token TOKEN         API token for gitlab, Is required for gitlab usage\n  --project PROJECT     Project ID of the merge request, defaults to\n                        enviroment variable set by pipeline.\n  --merge_request MERGE_REQUEST\n                        Internal ID of the merge request, defaults to\n                        enviroment variable set by pipeline.\n\n```\n\n</details>",
    'author': 'Tomer Keren',
    'author_email': 'tomer.keren.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/Tadaboody/lint-review',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
