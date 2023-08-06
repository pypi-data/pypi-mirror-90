# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fastapi_slack']
setup_kwargs = {
    'name': 'fastapi-slack',
    'version': '0.2.2',
    'description': 'Slack extension for FastAPI.',
    'long_description': '# fastapi-slack\n\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-brightgreen.svg)](https://conventionalcommits.org)\n[![CircleCI](https://circleci.com/gh/dialoguemd/fastapi-slack.svg?style=svg&circle-token=d5088d3188d29980a98d21136927b0693ea7d90e)](https://circleci.com/gh/dialoguemd/fastapi-slack)\n[![codecov](https://codecov.io/gh/dialoguemd/fastapi-slack/branch/master/graph/badge.svg?token=CVU9WOYOEG)](https://codecov.io/gh/dialoguemd/fastapi-slack)\n\nSlack extension for FastAPI.\n\n## Configuration - Environment Variables\n\n### `slack_access_token`\n\nBot User OAuth Access Token as defined in OAuth & Permissions menu of the slack app.\n\n### `slack_signing_secret`\n\nApp signing secret as shown in Basic Information menu of the slack app in the App\nCredentials section.\n\n## Setup\n\n* Include fastapi-slack router:\n\n```python\nimport fastapi_slack\nfrom fastapi import FastAPI\n\n\napp = FastAPI()\napp.include_router(fastapi_slack.router)\n```\n\n## [Slash Commands]\n\n* Depending on `fastapi_slack.SlashCommand` automatically validates Slack request\n  signature and extract the info needed to process it:\n\n```python\nfrom fastapi import Depends, FastAPI\nfrom fastapi_slack import SlashCommand, router\n\napp = FastAPI()\napp.include_router(router)\n\n\n@app.post("/slash-commands")\ndef process_commands(slash_command: SlashCommand = Depends()):\n    pass\n```\n\n\n[Slash Commands]: https://api.slack.com/interactivity/slash-commands\n',
    'author': 'Hadrien David',
    'author_email': 'hadrien@dialogue.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dialoguemd/fastapi-slack',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
