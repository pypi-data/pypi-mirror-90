# lint_review

Plug in any linter for a code review!

## Features:
- Creates merge request comments according to linter comments
- Easy to expand to any linter - just pass `--custom-pattern` with a regex capturing the important parts of the linter errors.
- Automatically resolves any comments that are no longer relevant.

## Usage:
- Create an [access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) with `api` premissions
- Pipe your linter into `lint_review` as part of your merge request CI
- Make a few mistakes (we all do)
- Fix the comments as they pop up


<details>
<summary> Full interface </summary>

```sh
usage: lint_review [-h] [--linter {flake8,mypy}] --reviewer {dry,gitlab}
                   [--custom_pattern CUSTOM_PATTERN] [--token TOKEN]
                   [--project PROJECT] [--merge_request MERGE_REQUEST]

optional arguments:
  -h, --help            show this help message and exit
  --linter {flake8,mypy}
                        Name of the linter to use
  --reviewer {dry,gitlab}
                        The service used to review the code
  --custom_pattern CUSTOM_PATTERN
                        A custom regex pattern to capture comments. The
                        pattern must have the named capture groups: {'line',
                        'message', 'path'} and optionally col

gitlab:
  --token TOKEN         API token for gitlab, Is required for gitlab usage
  --project PROJECT     Project ID of the merge request, defaults to
                        enviroment variable set by pipeline.
  --merge_request MERGE_REQUEST
                        Internal ID of the merge request, defaults to
                        enviroment variable set by pipeline.

```

</details>