from typing import TYPE_CHECKING, Type, Dict, Any

from .input import InputNode
from .output import OutputNode
from .bool import BoolNode
from .func import FuncNode


from .flow import FlowNode


node_registry: Dict[str, Type[FlowNode]] = {
    'INPUT': InputNode,
    'OUTPUT': OutputNode,
    'FUNC': FuncNode,
    'BOOL': BoolNode
}

def register_node(node_type_key: str, node_type: Type[FlowNode]) -> None:
    """Register a node type for construction

    Args:
        node_type_key (str): key for the node type
        node_type (Type[FlowNode]): Class, must subclass FlowNode
    """
    assert node_type_key not in node_registry, f'Node key: {node_type_key} is already used'
    node_registry.update({node_type_key, node_type})

def create_node(node_def: Dict[str, Any]) -> FlowNode:
    """Create a Node from the provided node_def

    Args:
        node_def (Dict[str, Any]): Dictionary to Deserialize into a FlowNode (subclass)

    Returns:
        FlowNode: Constructed flow Node
    """
    node_type = node_def.get('type', None)
    assert node_type is not None, 'Invalid Node Definition, `node_type` is missing'
    node_type_class = node_registry.get(node_type)
    assert node_type_class is not None, f'Node Type: {node_type} is not registered'
    return node_type_class(**node_def)
