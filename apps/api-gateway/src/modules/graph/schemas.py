from typing import List
from pydantic import BaseModel
from govflow_shared_types import GraphNode, GraphEdge

class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
