from typing import List, Dict, Any
from .link import Link
from .flow import FlowNode



def get_links_for_node(node_id: str, links: List[Link]) -> List[Link]:
    """
    Find the Links that apply to this node
    """
    of_node = [l for l in links if node_id in [l.to.node_id, l.from_binding.node_id]]
    return of_node

def get_payload_element(payload: Dict[str, Any], element_key: str):
    if '.' not in element_key:
        return payload.get(element_key, element_key)
    else:
        ret = payload
        keys = element_key.split('.')
        for key in keys:
            ret = ret.get(key, None)
            if ret is None:
                return key
        return ret


def find_node(nodes: List[FlowNode], id: str) -> FlowNode:
    for node in nodes:
        if node.id == id:
            return node

