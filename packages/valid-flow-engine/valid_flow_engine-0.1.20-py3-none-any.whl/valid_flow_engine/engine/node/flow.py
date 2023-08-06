from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Dict,
    Any,
    List,
    Optional,
    Tuple,
    Type,
    Generic,
    TypeVar, 
)

from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, PrivateAttr
from .link import Link

class FlowPort(BaseModel, ABC):
    """
    The base class for all ports,
    type should be overwritten to be constant
    """
    type: str
    id: str

class InputPort(FlowPort):
    """
    Input Type Port
    """
    type = 'INPUT'

class OutputPort(FlowPort):
    """
    Output Type Port
    """
    type = 'OUTPUT'

class FlowPorts(BaseModel):
    """
    Model for Ports Object on the Flow Node
    """
    INPUT: InputPort

class FlowProperties(BaseModel):
    """
    Base Node Properties
    """
    display_label: str = Field(alias='displayLabel')

class FlowNode(BaseModel):
    """
    Base class for all Flow Nodes
    """
    id: str
    node_type: str = Field(alias='type')
    ports: FlowPorts
    properties: FlowProperties
    _evaluated: bool = PrivateAttr(False) # Use in running nodes, check this so nodes are not re-run
