# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ehelply_python_sdk',
 'ehelply_python_sdk.services',
 'ehelply_python_sdk.services.access',
 'ehelply_python_sdk.services.security']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.9.2,<3.0.0',
 'ehelply-logger>=0.0.8,<0.0.9',
 'isodate>=0.6.0,<0.7.0',
 'passlib[bcrypt]>=1.7.2,<2.0.0',
 'pdoc3>=0.9.2,<0.10.0',
 'pydantic>=1.7.3,<2.0.0',
 'pyjwt>=1.7.1,<2.0.0',
 'pyopenssl>=19.1.0,<20.0.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'python-jose[cryptography]>=3.1.0,<4.0.0',
 'python-slugify>=4.0.0,<5.0.0',
 'python_dateutil>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'typer>=0.2.1,<0.3.0',
 'wheel>=0.34.2,<0.35.0']

entry_points = \
{'console_scripts': ['ehelply_sdk = ehelply_python_sdk.cli:cli_main']}

setup_kwargs = {
    'name': 'ehelply-python-sdk',
    'version': '0.1.0',
    'description': '',
    'long_description': '# eHelply Python SDK\n\n## Usage\n(Recommended) Approach 1: Create a SDK object which can be used to create a client for any of the eHelply services\n```python\nfrom ehelply_python_sdk.sdk import SDKConfiguration, eHelplySDK, ErrorResponse, is_response_error\n\nsdk: eHelplySDK = eHelplySDK(\n    sdk_configuration=SDKConfiguration(\n        access_token="",\n        secret_token="",\n        project_identifier="ehelply-resources",\n        base_url_override="http://localhost"\n    )\n)\n\naccess_client = sdk.make_access()\n\nresponse = access_client.search_types(name="eHelply Access")\n\nif is_response_error(response):\n    response: ErrorResponse = response\n    print("I\'m sadness")\n    print(response.status_code)\n    print(response.message)\nelse:\n    print(response.dict())\n```\n\nApproach 2: Alternatively, you can set up a client manually and forego the SDK object. That said, the SDK object provides minimal overhead, so I\'m not sure why you would want to do this.\n```python\nfrom ehelply_python_sdk.sdk import SDKConfiguration, eHelplySDK, ErrorResponse, is_response_error\nfrom ehelply_python_sdk.services.access.sdk import AccessSDK\nfrom ehelply_python_sdk.utils import make_requests\n\nsdk_config = SDKConfiguration(\n    access_token="",\n    secret_token="",\n    project_identifier="ehelply-resources",\n    base_url_override="http://localhost"\n)\n\naccess_only_sdk = AccessSDK(\n    sdk_configuration=sdk_config,\n    requests_session=make_requests(sdk_configuration=sdk_config)\n)\n\nresponse = access_only_sdk.search_types(name="eHelply Access")\n\nif is_response_error(response):\n    response: ErrorResponse = response\n    print("I\'m sadness")\n    print(response.status_code)\n    print(response.message)\nelse:\n    print(response.dict())\n```\n\n## Help\n* Docs site: https://ehelply.github.io/Python-eHelply-SDK/\n\n## Development\n* Generate the latest version of the docs by running this command from the repository root `ehelply dev export-code-docs`\n* In the event that the eHelply command above is not working, you can also run it like this: `pdoc --html -o docs --force ehelply_python_sdk`\n    * Then copy the files up one level.',
    'author': 'Shawn Clake',
    'author_email': 'shawn.clake@ehelply.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ehelply.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
