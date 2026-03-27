"""Petri net model for process mining.

Implements places, transitions, arcs, markings, and firing semantics.
Supports visualization via Graphviz.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ArcDirection(str, Enum):
    """Direction of an arc in the Petri net."""

    PLACE_TO_TRANSITION = "place_to_transition"
    TRANSITION_TO_PLACE = "transition_to_place"


@dataclass(frozen=True)
class Place:
    """A place (condition/state) in a Petri net."""

    name: str
    label: str | None = None

    def __repr__(self) -> str:
        return f"Place({self.name!r})"


@dataclass(frozen=True)
class Transition:
    """A transition (activity/event) in a Petri net.

    Invisible transitions (tau) have is_visible=False and represent
    silent/skip steps with no corresponding log activity.
    """

    name: str
    label: str | None = None
    is_visible: bool = True

    def __repr__(self) -> str:
        prefix = "τ" if not self.is_visible else ""
        return f"Transition({prefix}{self.name!r})"


@dataclass(frozen=True)
class Arc:
    """A directed arc connecting a place to a transition or vice versa."""

    source: Place | Transition
    target: Place | Transition
    weight: int = 1

    @property
    def direction(self) -> ArcDirection:
        """Determine arc direction based on source/target types."""
        if isinstance(self.source, Place) and isinstance(self.target, Transition):
            return ArcDirection.PLACE_TO_TRANSITION
        elif isinstance(self.source, Transition) and isinstance(self.target, Place):
            return ArcDirection.TRANSITION_TO_PLACE
        raise ValueError(
            f"Invalid arc: {type(self.source).__name__} -> {type(self.target).__name__}. "
            "Arcs must connect Place->Transition or Transition->Place."
        )


Marking = dict[Place, int]
"""A marking maps places to their token count."""


@dataclass
class PetriNet:
    """A Petri net with places, transitions, arcs, and marking semantics.

    Represents a workflow net used in process mining to model business processes.
    """

    name: str = "PetriNet"
    places: set[Place] = field(default_factory=set)
    transitions: set[Transition] = field(default_factory=set)
    arcs: set[Arc] = field(default_factory=set)

    def add_place(self, name: str, label: str | None = None) -> Place:
        """Create and add a place to the net.

        Args:
            name: Unique identifier for the place.
            label: Optional display label.

        Returns:
            The created Place.
        """
        # TODO: Implement — create Place, add to self.places, return it
        # Raise ValueError if a place with this name already exists
        raise NotImplementedError

    def add_transition(
        self, name: str, label: str | None = None, is_visible: bool = True
    ) -> Transition:
        """Create and add a transition to the net.

        Args:
            name: Unique identifier for the transition.
            label: Optional display label (activity name).
            is_visible: False for silent/tau transitions.

        Returns:
            The created Transition.
        """
        # TODO: Implement — create Transition, add to self.transitions, return it
        raise NotImplementedError

    def add_arc(self, source: Place | Transition, target: Place | Transition, weight: int = 1) -> Arc:
        """Add a directed arc between a place and a transition.

        Args:
            source: Source node (Place or Transition).
            target: Target node (Place or Transition).
            weight: Arc weight (default 1).

        Returns:
            The created Arc.

        Raises:
            ValueError: If source and target are the same type
                        (place-to-place or transition-to-transition).
        """
        # TODO: Implement — validate direction, create Arc, add to self.arcs
        raise NotImplementedError

    def get_input_places(self, transition: Transition) -> set[Place]:
        """Return all places with arcs leading into the given transition."""
        # TODO: Implement — find all Place->Transition arcs for this transition
        raise NotImplementedError

    def get_output_places(self, transition: Transition) -> set[Place]:
        """Return all places with arcs leading out of the given transition."""
        # TODO: Implement — find all Transition->Place arcs for this transition
        raise NotImplementedError

    def get_input_transitions(self, place: Place) -> set[Transition]:
        """Return all transitions with arcs leading into the given place."""
        # TODO: Implement — find all Transition->Place arcs for this place
        raise NotImplementedError

    def get_output_transitions(self, place: Place) -> set[Transition]:
        """Return all transitions with arcs leading out of the given place."""
        # TODO: Implement — find all Place->Transition arcs for this place
        raise NotImplementedError

    def is_enabled(self, transition: Transition, marking: Marking) -> bool:
        """Check if a transition is enabled under the given marking.

        A transition is enabled when each of its input places has at least
        as many tokens as the weight of the connecting arc.

        Args:
            transition: The transition to check.
            marking: Current token distribution.

        Returns:
            True if the transition can fire.
        """
        # TODO: Implement firing rule check
        # For each input place of the transition, verify marking[place] >= arc.weight
        raise NotImplementedError

    def fire(self, transition: Transition, marking: Marking) -> Marking:
        """Fire a transition, producing a new marking.

        Removes tokens from input places and adds tokens to output places
        according to arc weights.

        Args:
            transition: The transition to fire (must be enabled).
            marking: Current marking.

        Returns:
            New marking after firing.

        Raises:
            ValueError: If the transition is not enabled.
        """
        # TODO: Implement transition firing
        # - Check is_enabled first
        # - Copy marking
        # - Subtract tokens from input places (by arc weight)
        # - Add tokens to output places (by arc weight)
        # - Remove places with zero tokens from the marking dict
        raise NotImplementedError

    def get_enabled_transitions(self, marking: Marking) -> set[Transition]:
        """Return all transitions enabled under the given marking."""
        # TODO: Implement — check is_enabled for each transition
        raise NotImplementedError

    def to_graphviz(self, marking: Marking | None = None) -> Any:
        """Render the Petri net as a Graphviz Digraph.

        Args:
            marking: Optional marking to display token counts on places.

        Returns:
            graphviz.Digraph object for rendering.
        """
        # TODO: Implement Graphviz visualization
        # - Places as circles (with token counts if marking provided)
        # - Transitions as rectangles (filled black for invisible)
        # - Arcs as directed edges with weight labels if > 1
        raise NotImplementedError

    def __repr__(self) -> str:
        return (
            f"PetriNet({self.name!r}, "
            f"places={len(self.places)}, "
            f"transitions={len(self.transitions)}, "
            f"arcs={len(self.arcs)})"
        )
