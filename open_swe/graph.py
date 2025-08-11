"""Very small workflow graph utilities.

The real Open SWE project uses a graph to orchestrate agents.  Here we provide a
minimal implementation: nodes are agent names and edges represent which agent is
invoked next.  The :class:`WorkflowGraph` can run starting from an entry point and
collect the outputs of each executed agent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .agents import Agent, Team


@dataclass
class WorkflowGraph:
    team: Team
    edges: Dict[str, List[str]] = field(default_factory=dict)

    def connect(self, src: str, dest: str) -> None:
        """Connect ``src`` agent to ``dest`` agent."""

        self.edges.setdefault(src, []).append(dest)

    def run(self, entry_point: str, prompt: str) -> List[Tuple[str, str]]:
        """Execute the graph starting from ``entry_point``.

        Returns a list of ``(agent_name, output)`` tuples in the order they were
        executed.
        """

        outputs: List[Tuple[str, str]] = []
        queue = [(entry_point, prompt)]
        while queue:
            agent_name, current_prompt = queue.pop(0)
            agent = self.team.get(agent_name)
            result = agent.act("plan", current_prompt)
            outputs.append((agent_name, result))
            for child in self.edges.get(agent_name, []):
                queue.append((child, result))
        return outputs
