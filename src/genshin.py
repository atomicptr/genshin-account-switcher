from pathlib import Path
from typing import List, Optional
from os import getlogin

_GENSHIN_LOCATIONS = [
    # Anime Game Launcher
    f"~/.local/share/anime-game-launcher/game",
    # Anime Game Launcher GTK
    f"~/.local/share/anime-game-launcher-gtk/game",
    # Anime Game Launcher GTK - Flatpak
    "~/.var/app/moe.launcher.an-anime-game-launcher-gtk/data/"
    "anime-game-launcher/game",
    # Anime Game Launcher - Flatpak
    "~/.var/app/com.gitlab.KRypt0n_.an-anime-game-launcher/data/"
    "anime-game-launcher/game",
]

_USER_REG_PATH = "user.reg"
_UID_INFO_FILE = "drive_c/users/%s/AppData/LocalLow/miHoYo/Genshin Impact/UidInfo.txt"


def find_installations() -> List[str]:
    dirs = []
    for location in _GENSHIN_LOCATIONS:
        location = Path(location).expanduser()
        if not location.exists():
            continue
        dirs.append(location.__str__())
    return dirs


def _get_install_dir() -> Optional[str]:
    install_dir = find_installations()

    if len(install_dir) == 0 or len(install_dir) > 1:
        return None

    return install_dir[0]


def get_uid() -> Optional[str]:
    install_dir = _get_install_dir()

    if install_dir is None:
        return None

    uid_path = Path(install_dir, _UID_INFO_FILE % getlogin())

    if not uid_path.exists():
        return None

    return uid_path.read_text(encoding="utf8").strip()


def write_uid(uid: str) -> None:
    install_dir = _get_install_dir()

    if install_dir is None:
        return

    uid_path = Path(install_dir, _UID_INFO_FILE % getlogin())
    uid_path.write_text(f"{uid}\n", encoding="utf8")


def read_user_registry() -> Optional[bytes]:
    install_dir = _get_install_dir()

    if install_dir is None:
        return None

    user_reg_path = Path(install_dir, _USER_REG_PATH)

    if not user_reg_path.exists():
        return None

    return user_reg_path.read_bytes()


def write_user_registry(data: bytes) -> None:
    install_dir = _get_install_dir()

    if install_dir is None:
        return

    user_reg_path = Path(install_dir, _USER_REG_PATH)
    user_reg_path.write_bytes(data)

