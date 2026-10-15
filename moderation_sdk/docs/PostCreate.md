# PostCreate

Schema for creating a new post (starts in draft status).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Title of the post (1-200 characters, non-blank) | 
**content** | **str** | Body content (non-blank, up to 10000 characters at creation) | 

## Example

```python
from moderation_sdk.models.post_create import PostCreate

# TODO update the JSON string below
json = "{}"
# create an instance of PostCreate from a JSON string
post_create_instance = PostCreate.from_json(json)
# print the JSON string representation of the object
print PostCreate.to_json()

# convert the object into a dict
post_create_dict = post_create_instance.to_dict()
# create an instance of PostCreate from a dict
post_create_form_dict = post_create.from_dict(post_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


