# moderation_sdk.PostsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_post**](PostsApi.md#create_post) | **POST** /posts/ | Create a new draft post
[**get_post**](PostsApi.md#get_post) | **GET** /posts/{post_id} | Get single post by ID
[**list_posts**](PostsApi.md#list_posts) | **GET** /posts/ | List all posts
[**publish_post**](PostsApi.md#publish_post) | **PATCH** /posts/{post_id}/publish/ | Publish an approved post
[**submit_post**](PostsApi.md#submit_post) | **POST** /posts/{post_id}/submit/ | Submit post for AI moderation
[**update_post**](PostsApi.md#update_post) | **PUT** /posts/{post_id} | Update an existing post


# **create_post**
> PostResponse create_post(post_create)

Create a new draft post

Create a new post in draft status.  Title must be 1-200 non-blank characters. Content can be up to 10,000 characters. Moderation length rules (50-2000 chars) are enforced at submit time.

### Example


```python
import moderation_sdk
from moderation_sdk.models.post_create import PostCreate
from moderation_sdk.models.post_response import PostResponse
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
    api_instance = moderation_sdk.PostsApi(api_client)
    post_create = moderation_sdk.PostCreate() # PostCreate | 

    try:
        # Create a new draft post
        api_response = api_instance.create_post(post_create)
        print("The response of PostsApi->create_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PostsApi->create_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **post_create** | [**PostCreate**](PostCreate.md)|  | 

### Return type

[**PostResponse**](PostResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_post**
> PostResponse get_post(post_id)

Get single post by ID

Retrieve full details of a single post by its ID.

### Example


```python
import moderation_sdk
from moderation_sdk.models.post_response import PostResponse
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
    api_instance = moderation_sdk.PostsApi(api_client)
    post_id = 56 # int | 

    try:
        # Get single post by ID
        api_response = api_instance.get_post(post_id)
        print("The response of PostsApi->get_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PostsApi->get_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **post_id** | **int**|  | 

### Return type

[**PostResponse**](PostResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Post not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_posts**
> List[PostResponse] list_posts(status=status)

List all posts

Retrieve all posts ordered newest first (ID descending).  Supports optional status filtering against allowed statuses.

### Example


```python
import moderation_sdk
from moderation_sdk.models.post_response import PostResponse
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
    api_instance = moderation_sdk.PostsApi(api_client)
    status = moderation_sdk.Status() # Status | Filter posts by status (draft, flagged, approved, published) (optional)

    try:
        # List all posts
        api_response = api_instance.list_posts(status=status)
        print("The response of PostsApi->list_posts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PostsApi->list_posts: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | [**Status**](.md)| Filter posts by status (draft, flagged, approved, published) | [optional] 

### Return type

[**List[PostResponse]**](PostResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **publish_post**
> PostResponse publish_post(post_id)

Publish an approved post

Publish an approved post.  Only posts currently in 'approved' status can be published. Once published, the post becomes read-only and immutable.

### Example


```python
import moderation_sdk
from moderation_sdk.models.post_response import PostResponse
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
    api_instance = moderation_sdk.PostsApi(api_client)
    post_id = 56 # int | 

    try:
        # Publish an approved post
        api_response = api_instance.publish_post(post_id)
        print("The response of PostsApi->publish_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PostsApi->publish_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **post_id** | **int**|  | 

### Return type

[**PostResponse**](PostResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Post not found |  -  |
**409** | Invalid state transition |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_post**
> SubmitResponse submit_post(post_id)

Submit post for AI moderation

Submit a post for automated AI content moderation.  Allowed only from 'draft' or 'flagged' status (re-submitting a flagged post is allowed). Evaluates profanity, content length (50-2000 characters), and AI tone. Transitions status to 'approved' or 'flagged'.

### Example


```python
import moderation_sdk
from moderation_sdk.models.submit_response import SubmitResponse
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
    api_instance = moderation_sdk.PostsApi(api_client)
    post_id = 56 # int | 

    try:
        # Submit post for AI moderation
        api_response = api_instance.submit_post(post_id)
        print("The response of PostsApi->submit_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PostsApi->submit_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **post_id** | **int**|  | 

### Return type

[**SubmitResponse**](SubmitResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Post not found |  -  |
**409** | Invalid state transition |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_post**
> PostResponse update_post(post_id, post_update)

Update an existing post

Update post title and/or content.  Resets post status back to 'draft' and clears flagged reasons. Published posts cannot be edited and return 409 Conflict.

### Example


```python
import moderation_sdk
from moderation_sdk.models.post_response import PostResponse
from moderation_sdk.models.post_update import PostUpdate
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
    api_instance = moderation_sdk.PostsApi(api_client)
    post_id = 56 # int | 
    post_update = moderation_sdk.PostUpdate() # PostUpdate | 

    try:
        # Update an existing post
        api_response = api_instance.update_post(post_id, post_update)
        print("The response of PostsApi->update_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PostsApi->update_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **post_id** | **int**|  | 
 **post_update** | [**PostUpdate**](PostUpdate.md)|  | 

### Return type

[**PostResponse**](PostResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Post not found |  -  |
**409** | Invalid state transition |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

