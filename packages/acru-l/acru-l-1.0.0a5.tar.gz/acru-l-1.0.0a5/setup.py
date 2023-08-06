# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['acru_l',
 'acru_l.resources',
 'acru_l.resources.canary',
 'acru_l.resources.canary.src',
 'acru_l.resources.rds',
 'acru_l.resources.ses',
 'acru_l.resources.ses.configuration_set',
 'acru_l.resources.ses.domain_validation',
 'acru_l.resources.ses.verified_emails',
 'acru_l.services',
 'acru_l.services.api',
 'acru_l.services.api.wsgi',
 'acru_l.services.api.wsgi.src',
 'acru_l.stacks']

package_data = \
{'': ['*'], 'acru_l.resources.ses': ['layer/*']}

install_requires = \
['acru-l-toolkit>=1.0.0-alpha,<2.0.0',
 'aws-cdk.aws-apigatewayv2-integrations==1.79.0',
 'aws-cdk.aws-apigatewayv2==1.79.0',
 'aws-cdk.aws-cloudfront==1.79.0',
 'aws-cdk.aws-dynamodb==1.79.0',
 'aws-cdk.aws-events-targets==1.79.0',
 'aws-cdk.aws-events==1.79.0',
 'aws-cdk.aws-lambda-nodejs==1.79.0',
 'aws-cdk.aws-lambda-python==1.79.0',
 'aws-cdk.aws-lambda==1.79.0',
 'aws-cdk.aws-rds==1.79.0',
 'aws-cdk.aws-route53==1.79.0',
 'aws-cdk.aws-s3==1.79.0',
 'aws-cdk.aws-secretsmanager==1.79.0',
 'aws-cdk.core==1.79.0',
 'aws-cdk.custom-resources==1.79.0',
 'click>=7.1.2,<8.0.0',
 'pydantic[email]>=1.7.3,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['acrul = acru_l.cli:main']}

setup_kwargs = {
    'name': 'acru-l',
    'version': '1.0.0a5',
    'description': '',
    'long_description': '# AWS Cloud Resource Utils - Library (ACRU-L)\n\n[![codecov](https://codecov.io/gh/quadio-media/acru-l/branch/main/graph/badge.svg?token=kWn6eJxFwr)](https://codecov.io/gh/quadio-media/acru-l)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![Build](https://github.com/quadio-media/acru-l/workflows/Build/badge.svg)\n\nPronounced _Ah-crew-el (*ə-kroo͞′l*)_\n\nAn open source framework for collecting and reusing AWS CDK constructs and stacks.\n\n> NOTE: This project is currently not stable (alpha releases only) and is subject change at any time.\n> Please use at your own risk.\n\n## Usage: ACRU-L Action\n\nThis action provisions AWS stacks given an ACRU-L configuration file. The intention is to encapsulate\nthe code needed to provision resources without conflating application code with devops requirements.\n\nThe goal is to avoid conflating microservice application code with "infrastructure as code".\n\n### Inputs\n\n### `subcommand`\n\n**Optional** The aws-cdk subcommand to run. Default `"deploy -f --require-approval=never"`.\n\n## Example usage\n\n```yaml\n- user: actions/setup-python@v2\n  with:\n  python-version: 3.8\n- uses: actions/setup-node@v2\n  with:\n  node-version: 12\n- uses: quadio-media/acru-l@1.0.0a5\n  with:\n    subcommand: deploy -f\n  env:\n    AWS_REGION: us-east-1\n    AWS_ACCOUNT_ID: ${{ secrets.AWS_ACCOUNT_ID }}\n    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}\n    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}\n    DEPLOY_ID: ${{ github.sha }}\n    ACRUL_CONFIG_PATH: "./acru-l.toml"\n```\n\n### Configuration\n\nThe following settings must be passed as environment variables as shown in the example. Sensitive information, especially `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, should be [set as encrypted secrets](https://help.github.com/en/articles/virtual-environments-for-github-actions#creating-and-using-secrets-encrypted-variables) — otherwise, they\'ll be public to anyone browsing your repository\'s source code and CI logs.\n\n| Key | Value | Suggested Type | Required | Default |\n| ------------- | ------------- | ------------- | ------------- | ------------- |\n| `AWS_ACCOUNT_ID` | Your AWS Account ID. | `secret env` | **Yes** | N/A |\n| `AWS_ACCESS_KEY_ID` | Your AWS Access Key. [More info here.](https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html) | `secret env` | **Yes** | N/A |\n| `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Access Key. [More info here.](https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html) | `secret env` | **Yes** | N/A |\n| `AWS_REGION` | The region you want the VPC Stack to live in. | `env` | **Yes** | N/A |\n| `DEPLOY_ID` | SHA of the commit that triggered the action. | `env` / `github.sha` | **Yes** | N/A |\n| `ACRUL_CONFIG_PATH` | Path to the ACRU-L configuration file to use. | `env` | No | `./acru-l.toml` |\n\n\n## License\n\nThis project is distributed under the [MIT license](LICENSE).\n\n\n## Why?\nThe problem with infrastructure as code ...\n\nMonorepos...\nSnowflake code...\n\nConfounding application source code with devops\n\nA strict interface and reuse patterns\n\n## Installation\n\n`poetry add -D acru-l`\n\n`pip install acru-l`\n\n\n\n## About\n\n### Core Concepts\n\n* Resources - Extended constructs\n* Services - Collections of Resources that build a service interface\n* Stacks - Collections of Services\n\n#### Resources\nExtended constructs with set defaults\n\n#### Services\n\nTBD\n\n#### Stacks\n\nTBD\n',
    'author': 'Anthony Almarza',
    'author_email': 'anthony.almarza@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
