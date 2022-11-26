""" Configuration files per account """
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

from appdirs import user_config_dir


@dataclass
class AccountConfiguration:
    """ Representation of an account configuration file """
    uid: str
    name: str

    def to_dict(self):
        """ Converts the configuration into a dictionary """
        return {k: str(v) for k, v in asdict(self).items()}


def get_config_directory() -> Path:
    """ Get the config directory """
    return Path(user_config_dir("genshin-account-switcher"))


def get_account_directory(uid: str) -> Path:
    """ Get the account config directory """
    return Path(get_config_directory(), "accounts", uid)


def get_account_config(uid: str) -> Optional[AccountConfiguration]:
    """ Get the account configuration or None if there is none """
    config_file = Path(get_account_directory(uid), "config.json")

    if not config_file.exists():
        return None

    data = json.loads(config_file.read_text(encoding="utf8"))
    return AccountConfiguration(uid=data["uid"], name=data["name"])


def set_account_config(uid: str, config: AccountConfiguration) -> None:
    """ Set account configuration """
    config_file = Path(get_account_directory(uid), "config.json")
    config_file.write_text(
        json.dumps(config.to_dict(), indent=4),
        encoding="utf8"
    )


def set_account_name(uid: str, name: str) -> None:
    """ Set account name alias"""
    config = get_account_config(uid)

    if not config:
        config = AccountConfiguration(uid=uid, name=name)

    config.name = name
    set_account_config(uid, config)


def get_account_name(uid: str) -> Optional[str]:
    """ Get account name alias or None if non exists """
    config = get_account_config(uid)

    if not config:
        return None

    return config.name


def is_account_registered(uid: str) -> bool:
    """ Is there an account registered under this uid? """
    account_dir = get_account_directory(uid)
    return account_dir.exists()
