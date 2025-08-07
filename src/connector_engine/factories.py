from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from dependency_injector.providers import Provider

from .datasources.base import DataSource
from .exceptions import UnknownConnectorError


@dataclass
class ConnectorFactory:
    """Factory that resolves connectors by name."""

    backends: Dict[str, Provider[DataSource]]

    def get(self, name: str) -> DataSource:
        try:
            provider = self.backends[name]
        except KeyError as exc:
            raise UnknownConnectorError(name) from exc
        return provider()

