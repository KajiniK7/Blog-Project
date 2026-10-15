# FlaggedReasons

List of moderation violation reasons if flagged, otherwise null

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from moderation_sdk.models.flagged_reasons import FlaggedReasons

# TODO update the JSON string below
json = "{}"
# create an instance of FlaggedReasons from a JSON string
flagged_reasons_instance = FlaggedReasons.from_json(json)
# print the JSON string representation of the object
print FlaggedReasons.to_json()

# convert the object into a dict
flagged_reasons_dict = flagged_reasons_instance.to_dict()
# create an instance of FlaggedReasons from a dict
flagged_reasons_form_dict = flagged_reasons.from_dict(flagged_reasons_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


