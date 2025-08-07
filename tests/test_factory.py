import pytest
from dependency_injector import providers

from connector_engine.factories import ConnectorFactory
from connector_engine.datasources.base import DataSource
from connector_engine.exceptions import UnknownConnectorError


class Dummy(DataSource):
    async def execute_one(self, sql, params=None):  # pragma: no cover
        return {}

    async def execute_all(self, sql, params=None):  # pragma: no cover
        return []

    async def execute_df(self, sql, params=None):  # pragma: no cover
        import pandas as pd
        return pd.DataFrame()

    async def execute_write(self, sql, params=None):  # pragma: no cover
        return 0

    async def call_procedure(self, name, params=None):  # pragma: no cover
        return []

    def get_session(self):  # pragma: no cover
        raise NotImplementedError

    def begin_uow(self):  # pragma: no cover
        raise NotImplementedError


def test_factory_get_unknown():
    factory = ConnectorFactory(backends={})
    with pytest.raises(UnknownConnectorError):
        factory.get("missing")


def test_factory_returns_instance():
    dummy_provider = providers.Factory(Dummy)
    factory = ConnectorFactory(backends={"dummy": dummy_provider})
    obj = factory.get("dummy")
    assert isinstance(obj, Dummy)
