from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from govflow_shared_types import GraphNode, GraphEdge, NodePosition
import uuid

from src.modules.graph.repository import GraphRepository
from src.modules.graph.status_resolver import resolve_node_status
from src.modules.graph.schemas import GraphResponse

class GraphService:
    @staticmethod
    async def get_bidder_graph(db: AsyncSession, tender_id: str, bidder_id: str) -> GraphResponse:
        bidder = await GraphRepository.get_bidder(db, bidder_id)
        if not bidder:
            raise ValueError(f"Bidder {bidder_id} not found")

        requirements = await GraphRepository.get_tender_requirements(db, tender_id)
        documents = await GraphRepository.get_documents_by_bidder(db, tender_id, bidder_id)
        flags = await GraphRepository.get_compliance_flags(db, tender_id, bidder_id)

        nodes: List[GraphNode] = []
        edges: List[GraphEdge] = []

        # Central Bidder Node
        bidder_node = GraphNode(
            id=f"bidder-{bidder.id}",
            type="BIDDER",
            label=bidder.legal_name,
            status="VERIFIED",  # The bidder root node doesn't have a status in the same way, or it inherits
            position=NodePosition(x=0, y=0),
            metadata={"bidderId": bidder.id}
        )
        nodes.append(bidder_node)

        # Build lookup for documents by type
        docs_by_type = {}
        for d in documents:
            # We assume d.document_type maps to the requirement
            if d.document_type not in docs_by_type:
                docs_by_type[d.document_type] = []
            docs_by_type[d.document_type].append(d)

        # Circular layout parameters
        import math
        radius = 250
        angle_step = (2 * math.pi) / max(len(requirements), 1)

        for i, req in enumerate(requirements):
            angle = i * angle_step
            x = int(radius * math.cos(angle))
            y = int(radius * math.sin(angle))
            pos = NodePosition(x=x, y=y)

            req_docs = docs_by_type.get(req, [])
            
            if not req_docs:
                # Spawn a MISSING node
                node_id = f"missing-{req}"
                status = resolve_node_status("MISSING", [])
                node = GraphNode(
                    id=node_id,
                    type="DOCUMENT",
                    label=req,
                    status=status,
                    position=pos,
                    metadata={"documentType": req}
                )
                nodes.append(node)
                edges.append(GraphEdge(
                    id=f"edge-{bidder_node.id}-{node_id}",
                    source=bidder_node.id,
                    target=node_id,
                    label="requires"
                ))
            else:
                for idx, doc in enumerate(req_docs):
                    # Fetch processing status
                    job = await GraphRepository.get_processing_job(db, doc.id)
                    processing_status = job.status if job else "COMPLETED"

                    # Fetch flags for this document. 
                    # Flags have an anchors array, we check if it matches the doc id
                    doc_flags = []
                    for f in flags:
                        for anchor in f.anchors:
                            if anchor.get("documentId") == doc.id:
                                doc_flags.append(f.status)
                                break # once per flag

                    status = resolve_node_status(processing_status, doc_flags)
                    
                    # Spread out if multiple docs for same requirement (edge case, but possible)
                    doc_pos = NodePosition(x=x + (idx * 50), y=y + (idx * 50))

                    node = GraphNode(
                        id=f"doc-{doc.id}",
                        type="DOCUMENT",
                        label=doc.original_filename,
                        status=status,
                        position=doc_pos,
                        metadata={"documentId": doc.id, "documentType": doc.document_type}
                    )
                    nodes.append(node)
                    edges.append(GraphEdge(
                        id=f"edge-{bidder_node.id}-{node.id}",
                        source=bidder_node.id,
                        target=node.id,
                        label="provided"
                    ))

        return GraphResponse(nodes=nodes, edges=edges)
