"""Public API for constructing the demo Open SWE environment."""

from __future__ import annotations

from .agents import Agent, Team
from .graph import WorkflowGraph
from .tools import create_default_tools


def create_app() -> WorkflowGraph:
    """Create a small agent team wired together in a graph.

    The returned :class:`WorkflowGraph` is ready to run and mirrors the basic
    planning/execution flow of the `open-swe` project while remaining completely
    dependency free.
    """

    tools = create_default_tools()
    planner = Agent("planner", tools)
    coder = Agent("coder", tools)
    team = Team([planner, coder])

    graph = WorkflowGraph(team)
    graph.connect("planner", "coder")
    return graph
