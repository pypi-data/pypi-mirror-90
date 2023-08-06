from __future__ import annotations
from typing import (
    Any,
    List,
)
from .flow import FlowPorts, OutputPort
from .action import ActionNode
from .utils import get_links_for_node
from .link import Link

class FuncPorts(FlowPorts):
    """
    Ports Model for Function Node
    """
    OUTPUT: OutputPort

class FuncNode(ActionNode):
    """
    Function node, proving Input and Output
    """
    ports: FuncPorts
    nodeType = 'FUNC'

    def get_next_node_id(self, result: Any, links: List[Link]) -> str:
        """
        Get the Flow Node ids for the output of this FuncNode
        """
        of_node = get_links_for_node(self.id, links)
        ids = [f.to.node_id for f in of_node if f.from_binding.port_id == 'OUTPUT' and not f.to.node_id == self.id]
        assert len(ids) == 1
        return ids[0]
