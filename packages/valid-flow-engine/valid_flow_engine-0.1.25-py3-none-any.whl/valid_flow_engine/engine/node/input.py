from typing import List, Any
from pydantic import BaseModel
from .flow import OutputPort, FlowNode
from .link import Link
from .utils import get_links_for_node

class InputNodePorts(BaseModel):
    """
    Ports Mode for Input Node,
    Only has an OUTPUT port
    """
    OUTPUT: OutputPort

class InputNode(FlowNode):
    """
    Input Node, providing only outputs.
    Kicks off all flow
    """
    ports: InputNodePorts
    nodeType = 'INPUT'
    _evaluated = True

    def get_next_node_id(self, result: Any, links: List[Link]) -> str:
        of_node = get_links_for_node(self.id, links)
        ids = [f.to.node_id for f in of_node if f.from_binding.port_id == 'OUTPUT' and not f.to.node_id == self.id]
        assert len(ids) == 1
        return ids[0]
