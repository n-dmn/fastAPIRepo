"""Agent implementations for the Open SWE demo.

The design is intentionally small and educational.  Agents own a set of tools
that they can invoke via :meth:`act`.  Each tool is simply a callable that
accepts a text prompt and returns a text response.  The concrete behaviour of an
agent can be customised by providing different tools.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List


Tool = Callable[[str], str]


@dataclass
class Agent:
    """A minimal agent that can call a collection of tools.

    Parameters
    ----------
    name:
        Human friendly name used for debugging and visualisation.
    tools:
        Mapping of tool name to callables.
    """

    name: str
    tools: Dict[str, Tool] = field(default_factory=dict)

    def add_tool(self, name: str, tool: Tool) -> None:
        """Register ``tool`` under ``name``.

        If a tool with the same ``name`` already exists it will be overwritten.
        """

        self.tools[name] = tool

    def act(self, tool_name: str, prompt: str) -> str:
        """Execute one of the agent's tools.

        Raises
        ------
        KeyError
            If ``tool_name`` is not registered.
        """

        try:
            tool = self.tools[tool_name]
        except KeyError as exc:  # pragma: no cover - defensive
            raise KeyError(f"{self.name} has no tool named '{tool_name}'") from exc
        return tool(prompt)


class Team:
    """A light-weight container for working with multiple agents."""

    def __init__(self, agents: Iterable[Agent]):
        self._agents: List[Agent] = list(agents)

    def get(self, name: str) -> Agent:
        for agent in self._agents:
            if agent.name == name:
                return agent
        raise KeyError(f"Unknown agent '{name}'")

    def __iter__(self):
        return iter(self._agents)
