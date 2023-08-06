from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from .flow import FlowNode, FlowProperties
from .utils import get_payload_element

class OutputField(BaseModel):
    key: str
    literal: Optional[Any]
    payload_key: Optional[str]
    payload_element: bool

class OutputProperties(FlowProperties):
    output_fields: List[OutputField] = Field(alias='outputFields')


class OutputNode(FlowNode):
    """
    Output node, inherits from FlowNode and provides no additional
    ports outside of INPUT. Provides an (TODO) OutputDef,
    defining the output that will be recieved when flow leads to this node.
    """
    nodeType = 'OUTPUT'
    properties: OutputProperties

    def process_results(self, payload: Dict) -> Dict:
        result = {}
        for field in self.properties.output_fields:
            if field.payload_element:
                result[field.key] = get_payload_element(payload, field.payload_key)
            else:
                result[field.key] = field.literal
        return result
