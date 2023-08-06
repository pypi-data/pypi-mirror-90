# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['acru_l',
 'acru_l.apps',
 'acru_l.resources',
 'acru_l.resources.canary',
 'acru_l.resources.canary.src',
 'acru_l.resources.rds',
 'acru_l.resources.ses',
 'acru_l.resources.ses.domain_validation',
 'acru_l.resources.ses.verified_emails',
 'acru_l.services',
 'acru_l.services.wsgi',
 'acru_l.services.wsgi.src',
 'acru_l.stacks']

package_data = \
{'': ['*'], 'acru_l.resources.ses': ['layer/*']}

install_requires = \
['acru-l-toolkit>=0.1.0,<0.2.0',
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
 'environs>=9.2.0,<10.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'acru-l',
    'version': '0.1.4',
    'description': '',
    'long_description': '# AWS Cloud Resource Utils - Library (ACRU-L)\n\nPronounced _Ah-crew-el (*ə-kroo͞′l*)_\n\nAn open source framework for collecting and reusing AWS CDK constructs and stacks.\n\n## Why?\nThe problem with infrastructure as code ...\n\nMonorepos...\nSnowflake code...\n\nConfounding application source code with devops \n\nA strict interface and reuse patterns\n\n## Installation\n\n`poetry add -D acru-l`\n\n`pip install acru-l`\n\n## Usage\n\n\n## Core Concepts\n\n* Resources - Extended constructs\n* Services - Collections of Resources that build a service interface\n* Stacks - Collections of Services\n\n### Resources\nExtended constructs with set defaults\n\n### Services\n\nTBD\n\n### Stacks\n\nTBD\n\n### Apps\n\nTBD',
    'author': 'Anthony Almarza',
    'author_email': 'anthony.almarza@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
