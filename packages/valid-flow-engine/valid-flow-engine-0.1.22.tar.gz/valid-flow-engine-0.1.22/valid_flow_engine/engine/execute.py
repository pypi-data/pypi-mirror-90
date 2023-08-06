from typing import List, Dict, Tuple

from .node.link import Link
from .node.flow import FlowNode
from .node.input import InputNode
from .node.output import OutputNode
from .node.action import ActionNode
from .node.utils import find_node
from .node import create_node
import logging

def process_json(chart: Dict[str, Dict]) -> Tuple[List[FlowNode], List[Link]]:
    """Get Flow Nodes and Links from the JSON Definition

    Args:
        chart (Dict[str, Dict]): JSON coming from the front end

    Returns:
        Tuple[List[FlowNode], List[Link]]: Tuple of a List of Flow Nodes and List of Links
    """
    nodes = chart.get('nodes').values()
    nodes = [create_node(n) for n in nodes]
    links = chart.get('links').values()
    links = [Link(**l) for l in links]
    return nodes, links

def get_input_node(nodes: List[FlowNode]) -> InputNode:
    """Find the input node i the list of nodes

    Args:
        nodes (List[FlowNode]): List of Flow Nodes to search

    Returns:
        InputNode: The input node of the list
    """
    for node in nodes:
        if isinstance(node, InputNode):
            return node
    return None

def execute_flow(nodes: List[FlowNode], links: List[Link], payload: Dict) -> Dict:
    """Run the Node and Links to get the flow's results

    Args:
        nodes (List[FlowNode]): List of FlowNodes to process
        links (List[Link]): List of Links that define node connections
        payload (Dict): Payload Data to use in the node processing

    Returns:
        Tuple[Dict, Dict]: Output of the flow, Inidividual Node Results
    """
    node_results = {}
    logging.info(nodes)
    node: InputNode = get_input_node(nodes)
    next_node_id = node.get_next_node_id(None, links)
    node = find_node(nodes, next_node_id)
    while isinstance(node, ActionNode):
        next_node_id, node_result = node.run(payload)
        node_result[node.id] = node_result
        node = find_node(nodes, next_node_id)
    assert isinstance(node, OutputNode)
    return node.process_results(payload), node_results
