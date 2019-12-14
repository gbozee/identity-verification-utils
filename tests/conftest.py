import asyncio
import base64
import json
import os
import httpx
import pytest
from alembic import command
from alembic.config import Config
from starlette.config import environ
from starlette.testclient import TestClient

from orm.test_utils import *


@pytest.fixture(scope="session")
def monkeysession(request):
    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture
def create_future():
    def _create_future(value):
        dd = asyncio.Future()
        dd.set_result(value)
        return dd

    return _create_future
