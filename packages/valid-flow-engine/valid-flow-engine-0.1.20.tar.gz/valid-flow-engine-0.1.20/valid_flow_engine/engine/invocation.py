from __future__ import annotations
from typing import (
    Any,
    List,
    Optional,
)

from pydantic import BaseModel, validator, ValidationError, Field

class ParamInstance(BaseModel):
    """
    Models a Parameter Instance.
    Either payloadKey, or value must be present,
    depending on payloadElement being T/F, respecitively
    """
    key: str
    value: Optional[Any]
    payload_key: Optional[str] = Field(alias='payloadKey')
    payload_element: bool = Field(alias='payloadElement')

    @validator('payload_element')
    def optional_populated(cls, v: Any, values: dict, **kwargs) -> Any:
        if v:
            if values.get('payload_key', None) in [None, '']:
                raise ValidationError('payloadKey is required if ParamInstance is a payloadElement')
        else:
            if values.get('value', None) is None:
                raise ValidationError('value is required if ParamInstance is not a payloadElement')
        return v

class FunctionInvocation(BaseModel):
    """
    Define a Function Shape, used to find the
    operation to run.
    """
    name_space: str = Field(alias='nameSpace')
    function_key: str = Field(alias='functionKey')
    params: List[ParamInstance]

class ReturnDefinition(BaseModel):
    """
    Defines the return shape to add to the payload.
    The `key` is the field added to the payload.
    `type` should be the string name of the type
    that will be returned.
    """
    key: str
    type: str
