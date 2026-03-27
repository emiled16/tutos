"""Simple BPMN (Business Process Model and Notation) representation.

Provides start/end events, tasks, gateways (XOR, AND, OR), and
conversion from Petri nets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from process_mining.models.petri_net import Marking, PetriNet


class GatewayType(str, Enum):
    """BPMN gateway types."""

    EXCLUSIVE = "exclusive"   # XOR — exactly one path
    PARALLEL = "parallel"     # AND — all paths concurrently
    INCLUSIVE = "inclusive"    # OR — one or more paths


class NodeType(str, Enum):
    """Types of nodes in a BPMN model."""

    START_EVENT = "start_event"
    END_EVENT = "end_event"
    TASK = "task"
    GATEWAY = "gateway"


@dataclass(frozen=True)
class BPMNNode:
    """A node in a BPMN diagram."""

    id: str
    label: str | None = None
    node_type: NodeType = NodeType.TASK
    gateway_type: GatewayType | None = None


@dataclass(frozen=True)
class BPMNFlow:
    """A sequence flow connecting two BPMN nodes."""

    source_id: str
    target_id: str
    label: str | None = None


@dataclass
class BPMNModel:
    """A simplified BPMN process model.

    Supports start/end events, tasks, and gateways connected by sequence flows.
    """

    name: str = "BPMNModel"
    nodes: dict[str, BPMNNode] = field(default_factory=dict)
    flows: list[BPMNFlow] = field(default_factory=list)

    def add_start_event(self, node_id: str, label: str | None = None) -> BPMNNode:
        """Add a start event to the model.

        Args:
            node_id: Unique identifier for the start event.
            label: Optional display label.

        Returns:
            The created BPMNNode.
        """
        # TODO: Implement — create node with NodeType.START_EVENT, add to self.nodes
        raise NotImplementedError

    def add_end_event(self, node_id: str, label: str | None = None) -> BPMNNode:
        """Add an end event to the model.

        Args:
            node_id: Unique identifier for the end event.
            label: Optional display label.

        Returns:
            The created BPMNNode.
        """
        # TODO: Implement — create node with NodeType.END_EVENT, add to self.nodes
        raise NotImplementedError

    def add_task(self, node_id: str, label: str) -> BPMNNode:
        """Add a task (activity) to the model.

        Args:
            node_id: Unique identifier for the task.
            label: Activity name.

        Returns:
            The created BPMNNode.
        """
        # TODO: Implement — create node with NodeType.TASK, add to self.nodes
        raise NotImplementedError

    def add_gateway(
        self, node_id: str, gateway_type: GatewayType, label: str | None = None
    ) -> BPMNNode:
        """Add a gateway (split/join) to the model.

        Args:
            node_id: Unique identifier for the gateway.
            gateway_type: EXCLUSIVE (XOR), PARALLEL (AND), or INCLUSIVE (OR).
            label: Optional display label.

        Returns:
            The created BPMNNode.
        """
        # TODO: Implement — create node with NodeType.GATEWAY and gateway_type
        raise NotImplementedError

    def add_flow(self, source_id: str, target_id: str, label: str | None = None) -> BPMNFlow:
        """Add a sequence flow between two nodes.

        Args:
            source_id: ID of the source node.
            target_id: ID of the target node.
            label: Optional flow label (e.g., condition).

        Returns:
            The created BPMNFlow.

        Raises:
            ValueError: If source or target node does not exist.
        """
        # TODO: Implement — validate both nodes exist, create BPMNFlow, add to self.flows
        raise NotImplementedError

    @classmethod
    def from_petri_net(
        cls, net: PetriNet, initial_marking: Marking, final_marking: Marking
    ) -> BPMNModel:
        """Convert a Petri net to a BPMN model.

        Maps Petri net structures to BPMN elements:
        - Source place → Start event
        - Sink place → End event
        - Visible transitions → Tasks
        - Places with multiple output transitions → XOR split gateways
        - Transitions with multiple output places → AND split gateways

        Args:
            net: The Petri net to convert.
            initial_marking: Initial marking (identifies the start place).
            final_marking: Final marking (identifies the end place).

        Returns:
            Equivalent BPMNModel.
        """
        # TODO: Implement Petri net to BPMN conversion
        # This is a simplified conversion — full PN-to-BPMN is complex
        # Strategy:
        # 1. Identify source/sink places from markings
        # 2. Map visible transitions to tasks
        # 3. Detect split/join patterns and insert appropriate gateways
        # 4. Handle invisible transitions (tau) as routing elements
        raise NotImplementedError

    def to_graphviz(self) -> Any:
        """Render the BPMN model as a Graphviz Digraph.

        Returns:
            graphviz.Digraph with standard BPMN visual conventions.
        """
        # TODO: Implement Graphviz visualization
        # - Start events as thin circles (green)
        # - End events as bold circles (red)
        # - Tasks as rounded rectangles
        # - Gateways as diamonds with X/+/O markers
        # - Sequence flows as directed edges
        raise NotImplementedError

    def __repr__(self) -> str:
        return (
            f"BPMNModel({self.name!r}, "
            f"nodes={len(self.nodes)}, "
            f"flows={len(self.flows)})"
        )
