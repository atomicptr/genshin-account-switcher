#!/usr/bin/env python3

""" CLI command to switch Genshin Impact Accounts """

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from appdirs import user_config_dir

try:
    from . import genshin
except ImportError:
    import genshin


def main():
    """ Main function implementing the CLI command """
    dirs = genshin.find_installations()

    if len(dirs) == 0:
        print("ERROR: No Genshin Installation could be found.")
        sys.exit(1)

    if len(dirs) > 1:
        print("ERROR: More than one Genshin Installation was found,"
              "this is currently unsupported.\n* " + "\n* ".join(dirs))
        sys.exit(1)

    config_dir = Path(user_config_dir("genshin-account-switcher"))

    if not config_dir.exists():
        config_dir.mkdir()

    parser = ArgumentParser(
        description="Quick and easy Genshin Impact Account Switcher",
        add_help=True,
    )

    subparsers = parser.add_subparsers()

    parser_register = subparsers.add_parser(
        "register",
        help="Register a new Genshin account",
    )
    parser_register.set_defaults(func=register_command)

    parser_switch = subparsers.add_parser(
        "switch",
        help="Switch account",
    )
    parser_switch.add_argument("uid", nargs="?", type=int, default=None)
    parser_switch.set_defaults(func=switch_command, cmd=parser_switch)

    parser_current = subparsers.add_parser(
        "current",
        help="Show current account",
    )
    parser_current.set_defaults(func=current_command)

    args = parser.parse_args(sys.argv[1:])
    if "func" not in args:
        parser.print_help()
        sys.exit(0)
    args.func(args, config_dir)


def register_command(_args: Namespace, config_dir: str):
    """ The command responsible for registering accounts"""
    uid = genshin.get_uid()

    if uid is None:
        print("ERROR: Could not determine UID, did you log into the game yet?")
        sys.exit(1)

    account_dir = Path(config_dir, "accounts", uid)

    if not account_dir.exists():
        account_dir.mkdir(parents=True)

    user_reg_data = genshin.read_user_registry()

    if user_reg_data is None:
        print("ERROR: Could not find user.reg, did you log into the game yet?")
        sys.exit(1)

    user_reg_path = Path(account_dir, "user.reg")
    user_reg_path.write_bytes(user_reg_data)

    print(f"Successfully registered account '{uid}'.")


def switch_command(args: Namespace, config_dir: str):
    """ The command responsible for switching accounts"""
    uid = args.uid

    accounts_dir = Path(config_dir, "accounts")

    if not accounts_dir.exists():
        accounts_dir.mkdir()

    registered_account_paths = list(accounts_dir.glob("*"))

    if uid is None:
        if len(registered_account_paths) == 0:
            print("ERROR: Could not find any registered accounts, did you run"
                  "the register command already?")
            sys.exit(1)

        args.cmd.print_help()

        print("\nAvailable UIDs:")

        for index, file in enumerate(registered_account_paths):
            if not file.is_dir():
                continue
            check = " ✔️" if file.name == str(genshin.get_uid()) else ""
            print(f"* [{index}] {file.name}{check}")
        sys.exit(0)

    # user probably picked an enumerated option
    if 0 <= uid < len(registered_account_paths):
        uid = int(registered_account_paths[uid].name)

    registered_accounts = list(map(
        lambda acc_file: int(acc_file.name),
        registered_account_paths
    ))

    if uid not in registered_accounts:
        print(f"ERROR: Unknown UID '{uid}', available options are:")
        for index, acc in enumerate(registered_accounts):
            print(f"* [{index}] {acc}")
        sys.exit(1)

    user_reg_path = Path(accounts_dir, str(uid), "user.reg")

    if not user_reg_path.exists():
        print(f"ERROR: User Registry for '{uid}' did not exist.")
        sys.exit(1)

    backup_current_account_if_possible(config_dir)

    user_reg_data = user_reg_path.read_bytes()

    genshin.write_uid(uid)
    genshin.write_user_registry(user_reg_data)

    print(f"Successfully switched to account '{uid}'")


def current_command(_args: Namespace, _config_dir: str):
    """ Shows your currently selected uid """
    uid = genshin.get_uid()

    if uid is None:
        print("No account could be found, have you logged into the game yet?")
        sys.exit(0)

    print(f"Currently selected account: '{uid}'")


def backup_current_account_if_possible(config_dir: str) -> bool:
    """ Backup the current account if there is one """
    uid = genshin.get_uid()

    if uid is None:
        return False

    account_dir = Path(config_dir, "accounts", uid)

    if not account_dir.exists():
        account_dir.mkdir(parents=True)

    user_reg_data = genshin.read_user_registry()

    if user_reg_data is None:
        return False

    user_reg_path = Path(account_dir, "user.reg")
    user_reg_path.write_bytes(user_reg_data)
    return True


if __name__ == "__main__":
    main()
