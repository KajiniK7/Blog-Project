# moderation_sdk.HealthApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**root**](HealthApi.md#root) | **GET** / | Health check


# **root**
> object root()

Health check

Health check / root endpoint.

### Example


```python
import moderation_sdk
from moderation_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = moderation_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with moderation_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = moderation_sdk.HealthApi(api_client)

    try:
        # Health check
        api_response = api_instance.root()
        print("The response of HealthApi->root:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling HealthApi->root: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

