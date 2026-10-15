# PostUpdate

Schema for updating an existing post (resets status back to draft).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | [**Title**](Title.md) |  | [optional] 
**content** | [**Content**](Content.md) |  | [optional] 

## Example

```python
from moderation_sdk.models.post_update import PostUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of PostUpdate from a JSON string
post_update_instance = PostUpdate.from_json(json)
# print the JSON string representation of the object
print PostUpdate.to_json()

# convert the object into a dict
post_update_dict = post_update_instance.to_dict()
# create an instance of PostUpdate from a dict
post_update_form_dict = post_update.from_dict(post_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


