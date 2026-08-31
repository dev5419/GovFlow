"use client";
import React, { useEffect, useState, useCallback } from "react";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { 
  ReactFlow, 
  Background, 
  Controls, 
  ReactFlowProvider,
  Node,
  Edge
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import { graphApi } from "../api/graphApi";
import { BidderNode } from "./BidderNode";
import { DocumentNode } from "./DocumentNode";
import { GraphLegend } from "./GraphLegend";
import { NodeDetailPanel } from "./NodeDetailPanel";
import { GraphNode } from "@govflow/shared-types";

// Register custom node types
const nodeTypes = {
  BIDDER: BidderNode,
  DOCUMENT: DocumentNode,
};

interface BidderStarGraphProps {
  tenderId: string;
  bidderId: string;
}

function StarGraphInternal({ tenderId, bidderId }: BidderStarGraphProps) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [rawNodes, setRawNodes] = useState<GraphNode[]>([]);
  const [loading, setLoading] = useState(true);

  // Derive selection strictly from URL query param to satisfy PRD §8.5 persistence
  const selectedNodeId = searchParams.get("selectedNodeId");
  const selectedGraphNode = rawNodes.find(n => n.id === selectedNodeId) || null;

  useEffect(() => {
    async function loadGraph() {
      setLoading(true);
      try {
        const data = await graphApi.getBidderGraph(tenderId, bidderId);
        setRawNodes(data.nodes);
        
        // Map backend GraphNodes to React Flow nodes
        const flowNodes: Node[] = data.nodes.map((n) => ({
          id: n.id,
          type: n.type,
          position: { x: n.position.x, y: n.position.y },
          data: { label: n.label, status: n.status, metadata: n.metadata },
        }));

        // Map backend GraphEdges to React Flow edges
        const flowEdges: Edge[] = data.edges.map((e) => ({
          id: e.id,
          source: e.source,
          target: e.target,
          label: e.label,
          type: 'straight',
          style: { stroke: "#CBD5E1", strokeWidth: 2 },
          animated: false,
        }));

        setNodes(flowNodes);
        setEdges(flowEdges);
      } catch (e) {
        console.error("Failed to load graph", e);
      } finally {
        setLoading(false);
      }
    }
    loadGraph();
  }, [tenderId, bidderId]);

  const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    // Persist selection in URL
    const params = new URLSearchParams(searchParams.toString());
    params.set("selectedNodeId", node.id);
    router.push(`${pathname}?${params.toString()}`, { scroll: false });
  }, [pathname, router, searchParams]);

  if (loading) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-[#F8F9FA] text-slate-500">
        Constructing Graph...
      </div>
    );
  }

  return (
    <div className="flex w-full h-[800px] overflow-hidden border border-slate-200 rounded-lg">
      {/* Canvas Area */}
      <div className="flex-1 relative bg-[#F8F9FA]">
        <ReactFlow
          nodes={nodes.map(n => ({ ...n, selected: n.id === selectedNodeId }))}
          edges={edges}
          nodeTypes={nodeTypes}
          onNodeClick={onNodeClick}
          fitView
          fitViewOptions={{ padding: 0.2 }}
          minZoom={0.5}
          maxZoom={2}
          proOptions={{ hideAttribution: true }}
        >
          <Background color="#E2E8F0" gap={20} size={1} />
          <Controls className="bg-white border-slate-200 fill-slate-700" />
        </ReactFlow>
        
        <GraphLegend />
      </div>

      {/* Side Panel Area */}
      {selectedNodeId && (
        <NodeDetailPanel 
          node={selectedGraphNode} 
          tenderId={tenderId} 
          bidderId={bidderId} 
        />
      )}
    </div>
  );
}

export function BidderStarGraph(props: BidderStarGraphProps) {
  return (
    <ReactFlowProvider>
      <StarGraphInternal {...props} />
    </ReactFlowProvider>
  );
}
