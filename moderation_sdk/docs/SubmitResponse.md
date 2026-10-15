# SubmitResponse

Response returned upon submitting a post for AI moderation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Post ID | 
**status** | **str** | New post status after moderation evaluation | 
**reasons** | **List[str]** | List of moderation violation reasons if flagged (empty if approved) | [optional] 
**message** | **str** | Human-readable summary of moderation outcome | 

## Example

```python
from moderation_sdk.models.submit_response import SubmitResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitResponse from a JSON string
submit_response_instance = SubmitResponse.from_json(json)
# print the JSON string representation of the object
print SubmitResponse.to_json()

# convert the object into a dict
submit_response_dict = submit_response_instance.to_dict()
# create an instance of SubmitResponse from a dict
submit_response_form_dict = submit_response.from_dict(submit_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


