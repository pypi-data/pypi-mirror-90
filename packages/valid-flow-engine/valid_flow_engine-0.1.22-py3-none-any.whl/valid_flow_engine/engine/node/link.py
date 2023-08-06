from pydantic import BaseModel, Field

class LinkBinding(BaseModel):
    """
    Describes the binding to ports
    """
    node_id: str = Field(alias='nodeId')
    port_id: str = Field(alias='portId')

class Link(BaseModel):
    """
    Link's two ports
    """
    id: str
    from_binding: LinkBinding = Field(alias='from')
    to: LinkBinding
