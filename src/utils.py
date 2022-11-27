""" Utility functions """
try:
    from . import genshin, config
except ImportError:
    import genshin
    import config


def backup_current_account_if_possible() -> bool:
    """ Backup the current account if there is one """
    uid = genshin.get_uid()

    if uid is None:
        return False

    user_reg_data = genshin.read_user_registry()

    if user_reg_data is None:
        return False

    config.set_user_registry(uid, user_reg_data)
    return True


def format_uid(uid: str) -> str:
    """ Displays the account name if available otherwise just the uid"""
    name = config.get_account_name(uid)
    if name is None:
        return f"'{uid}'"
    return f"{name} ({uid})"


def check_if_selected(uid: str) -> str:
    """ Renders a check if the uid is selected right now """
    return "✔️" if uid == str(genshin.get_uid()) else ""
