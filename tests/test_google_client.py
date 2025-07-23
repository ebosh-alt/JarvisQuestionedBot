import json
from datetime import datetime

import pytest

from internal.entities.database import User
from pkg.get_message import get_mes
from pkg.google_client import GoggleClient

TEST_SPREADSHEET = "test"
TEST_SHEET = "users"


@pytest.fixture(scope="module")
def google_client():
    """Создаём реальный клиент Google Sheets."""
    return GoggleClient


# if not data.get(vl.city):
#     data[vl["город"]] = {}
#
# # print(data)
# if not data[vl["город"]].get(vl["команда"]):
#     data[vl["город"]][vl["команда"]] = []
# data[vl["город"]][vl["команда"]].append({"id": vl["id"], "фио": vl["фио"]})
@pytest.mark.asyncio
async def test_get(google_client):

    assert False