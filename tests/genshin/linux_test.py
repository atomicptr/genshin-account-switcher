import shutil
import tempfile
import time
from getpass import getuser
from pathlib import Path
from unittest.mock import patch

import pytest
from src import genshin

_test_location = Path(
    tempfile.gettempdir(),
    f"genshin-account-switcher-test-{time.time()}",
)
_uid_file = "drive_c/users/%s/AppData/LocalLow/miHoYo/" \
            "Genshin Impact/UidInfo.txt"


@pytest.fixture
def genshin_installation():
    if not _test_location.exists():
        _test_location.mkdir(parents=True)

    Path(_test_location, "user.reg").write_text("This is the users registry")
    uid_file = Path(_test_location, _uid_file % getuser())
    uid_file.parent.mkdir(parents=True)
    uid_file.write_text("999999999\n", encoding="utf8")

    yield

    print(_test_location)
    shutil.rmtree(_test_location)


def test_find_installations(genshin_installation):
    with patch("src.genshin.linux._GENSHIN_LOCATIONS", ["/home/test-user/gi"]):
        assert len(genshin.find_installations()) == 0
    with patch("src.genshin.linux._GENSHIN_LOCATIONS", [_test_location]):
        assert len(genshin.find_installations()) > 0


def test_get_uid(genshin_installation):
    with patch("src.genshin.linux._GENSHIN_LOCATIONS", ["/home/test-user/gi"]):
        assert genshin.get_uid() is None
    with patch("src.genshin.linux._GENSHIN_LOCATIONS", [_test_location]):
        assert genshin.get_uid() == "999999999"


def test_set_uid(genshin_installation):
    with patch("src.genshin.linux._GENSHIN_LOCATIONS", ["/home/test-user/gi"]):
        assert genshin.get_uid() is None
        genshin.write_uid("888888888")
        assert genshin.get_uid() is None
    with patch("src.genshin.linux._GENSHIN_LOCATIONS", [_test_location]):
        assert genshin.get_uid() == "999999999"
        genshin.write_uid("888888888")
        assert genshin.get_uid() == "888888888"


def test_read_user_registry(genshin_installation):
    with patch("src.genshin.linux._GENSHIN_LOCATIONS", ["/home/test-user/gi"]):
        assert genshin.read_user_registry() is None
    with patch("src.genshin.linux._GENSHIN_LOCATIONS", [_test_location]):
        assert genshin.read_user_registry() is not None


def test_write_user_registry(genshin_installation):
    with patch("src.genshin.linux._GENSHIN_LOCATIONS", ["/home/test-user/gi"]):
        assert genshin.read_user_registry() is None
        genshin.write_user_registry(b"Test")
        assert genshin.read_user_registry() is None
    with patch("src.genshin.linux._GENSHIN_LOCATIONS", [_test_location]):
        data = genshin.read_user_registry()
        genshin.write_user_registry(b"Test")
        assert data != genshin.read_user_registry()
