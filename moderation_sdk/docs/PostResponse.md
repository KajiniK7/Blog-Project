# PostResponse

Schema representing a post entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Unique post ID | 
**title** | **str** | Post title | 
**content** | **str** | Post body content | 
**status** | **str** | Current status in moderation lifecycle | 
**flagged_reasons** | [**FlaggedReasons**](FlaggedReasons.md) |  | [optional] 
**created_at** | [**CreatedAt**](CreatedAt.md) |  | [optional] 

## Example

```python
from moderation_sdk.models.post_response import PostResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PostResponse from a JSON string
post_response_instance = PostResponse.from_json(json)
# print the JSON string representation of the object
print PostResponse.to_json()

# convert the object into a dict
post_response_dict = post_response_instance.to_dict()
# create an instance of PostResponse from a dict
post_response_form_dict = post_response.from_dict(post_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


