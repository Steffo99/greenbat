"""
:mod:`pytest` global configuration.

Fixtures defined here will be available everywhere in the package.
"""

import typing as t
import pytest
import fastapi
import fastapi.testclient
import sqlalchemy.orm

from greenbat.app import app
from greenbat.database.engine import Session as DatabaseSession


@pytest.fixture(scope="package", autouse=True)
def fastapi_test_client() -> fastapi.testclient.TestClient:
    return fastapi.testclient.TestClient(app)


@pytest.fixture(scope="function")
def database_session() -> sqlalchemy.orm.Session:
    with DatabaseSession() as session:
        yield session
