from __future__ import annotations
from typing import List
from .link import Link
from .flow import FlowPorts, OutputPort
from .action import ActionNode
from .utils import get_links_for_node

class BoolPorts(FlowPorts):
    """
    Ports Model for Boolean Node
    """
    TRUE: OutputPort
    FALSE: OutputPort

class BoolNode(ActionNode):
    """
    Boolean Node, providing Input, TRUE, and FALSE Ports
    """
    ports: BoolPorts
    nodeType = 'BOOL'

    def get_next_node_id(self, result: bool, links: List[Link]) -> str:
        """
        Find the FlowNode ids that apply given a result
        """
        port_id = 'TRUE' if result else 'FALSE'
        of_node = get_links_for_node(self.id, links)
        ids = [f.to.node_id for f in of_node if f.from_binding.port_id == port_id]
        assert len(ids) == 1
        return ids[0]
