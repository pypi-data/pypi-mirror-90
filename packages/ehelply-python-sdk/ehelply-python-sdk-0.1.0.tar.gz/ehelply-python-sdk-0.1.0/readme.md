# eHelply Python SDK

## Usage
(Recommended) Approach 1: Create a SDK object which can be used to create a client for any of the eHelply services
```python
from ehelply_python_sdk.sdk import SDKConfiguration, eHelplySDK, ErrorResponse, is_response_error

sdk: eHelplySDK = eHelplySDK(
    sdk_configuration=SDKConfiguration(
        access_token="",
        secret_token="",
        project_identifier="ehelply-resources",
        base_url_override="http://localhost"
    )
)

access_client = sdk.make_access()

response = access_client.search_types(name="eHelply Access")

if is_response_error(response):
    response: ErrorResponse = response
    print("I'm sadness")
    print(response.status_code)
    print(response.message)
else:
    print(response.dict())
```

Approach 2: Alternatively, you can set up a client manually and forego the SDK object. That said, the SDK object provides minimal overhead, so I'm not sure why you would want to do this.
```python
from ehelply_python_sdk.sdk import SDKConfiguration, eHelplySDK, ErrorResponse, is_response_error
from ehelply_python_sdk.services.access.sdk import AccessSDK
from ehelply_python_sdk.utils import make_requests

sdk_config = SDKConfiguration(
    access_token="",
    secret_token="",
    project_identifier="ehelply-resources",
    base_url_override="http://localhost"
)

access_only_sdk = AccessSDK(
    sdk_configuration=sdk_config,
    requests_session=make_requests(sdk_configuration=sdk_config)
)

response = access_only_sdk.search_types(name="eHelply Access")

if is_response_error(response):
    response: ErrorResponse = response
    print("I'm sadness")
    print(response.status_code)
    print(response.message)
else:
    print(response.dict())
```

## Help
* Docs site: https://ehelply.github.io/Python-eHelply-SDK/

## Development
* Generate the latest version of the docs by running this command from the repository root `ehelply dev export-code-docs`
* In the event that the eHelply command above is not working, you can also run it like this: `pdoc --html -o docs --force ehelply_python_sdk`
    * Then copy the files up one level.