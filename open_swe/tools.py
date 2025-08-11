"""Simple tools used by the agents.

Tools are represented as callables taking a string and returning a string.  The
module defines a very small set of built-in tools that mirror the planning and
coding steps in the real `open-swe` project.
"""

from __future__ import annotations

from typing import Callable


Tool = Callable[[str], str]


def planner(prompt: str) -> str:
    """Return a basic plan for the given ``prompt``."""

    return f"Plan: break down '{prompt}' into smaller tasks."


def coder(prompt: str) -> str:
    """Return a mock implementation suggestion for ``prompt``."""

    return f"Code suggestion for '{prompt}': ..."


def create_default_tools() -> dict[str, Tool]:
    """Factory returning the default toolset used by the app."""

    return {"plan": planner, "code": coder}
