"""Module for finding and interacting with the Genshin Impact installation"""
from typing import List, Optional
import platform

try:
    from . import linux
except ImportError:
    import linux


def find_installations() -> List[str]:
    """ Find Genshin Impact installations """
    if platform.system() == "Linux":
        return linux.find_installations()
    raise NotImplementedError(f"Unsupported OS: {platform.system()}")


def get_uid() -> Optional[str]:
    """ Get the UID of the current installation """
    if platform.system() == "Linux":
        return linux.get_uid()
    raise NotImplementedError(f"Unsupported OS: {platform.system()}")


def write_uid(uid: str) -> None:
    """ Write a UID to the UidInfo.txt file """
    if platform.system() == "Linux":
        return linux.write_uid(uid)
    raise NotImplementedError(f"Unsupported OS: {platform.system()}")


def read_user_registry() -> Optional[bytes]:
    """ Read the user registry """
    if platform.system() == "Linux":
        return linux.read_user_registry()
    raise NotImplementedError(f"Unsupported OS: {platform.system()}")


def write_user_registry(data: bytes) -> None:
    """ Write the user registry """
    if platform.system() == "Linux":
        return linux.write_user_registry(data)
    raise NotImplementedError(f"Unsupported OS: {platform.system()}")
