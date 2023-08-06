from typing import (
    Any,
    List,
    Dict,
    Callable,
    Tuple
)
from .utils import get_payload_element
from valid_flow_engine.engine.node.link import Link
from pydantic import Field
from abc import ABC, abstractmethod
from valid_flow_engine.engine.invocation import FunctionInvocation, ReturnDefinition

from valid_flow_engine.engine.invocation import FunctionInvocation, ReturnDefinition
from .flow import FlowProperties, FlowNode
from valid_flow_engine.op_set_registry import get_op

class ActionProperties(FlowProperties):
    """
    Node Properties providing function information
    """
    func: FunctionInvocation
    return_def: ReturnDefinition = Field(alias='returnDef')
    IS_ACTION = True

class ActionNode(FlowNode, ABC):
    """
    Nodes for containing Action's (function invocations)
    """
    properties: ActionProperties

    @property
    def op(self) -> Callable[[dict], Any]:
        func: FunctionInvocation = self.properties.func
        return get_op(func.name_space, func.function_key)
    
    @abstractmethod
    def get_next_node_id(self, result: Any, links: List[Link]) -> str:
        pass
    
    def get_kwargs(self, payload: dict) -> Dict[str, Any]:
        kwargs = {}
        for param in self.properties.func.params:
            if param.payload_element:
                value = get_payload_element(payload, param.payload_key)
            else:
                value = param.value
            kwargs[param.key] = value
        return kwargs

    def run(self, payload: dict, nodes: List[FlowNode], links: List[Link]) -> Tuple[str, Any]:
        """
        Run operation of this node and return the
        targets that should be run next
        """
        result = self.op(**self.get_kwargs(payload))
        if self.properties.return_def:
            payload.update({self.properties.return_def.key: result})
        return self.get_next_node_id(result, links), result
