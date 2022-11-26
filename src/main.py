#!/usr/bin/env python3

""" CLI command to switch Genshin Impact Accounts """

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

try:
    from . import genshin, config
except ImportError:
    import genshin
    import config


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

    config_dir = config.get_config_directory()

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
    parser_register.add_argument("--name", "-n", type=str, default=None)
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

    parser_setname = subparsers.add_parser(
        "set-name",
        help="Set the name for an account"
    )
    parser_setname.add_argument("uid", type=int)
    parser_setname.add_argument("name", type=str)
    parser_setname.set_defaults(func=setname_command)

    args = parser.parse_args(sys.argv[1:])
    if "func" not in args:
        parser.print_help()
        sys.exit(0)
    args.func(args)


def register_command(args: Namespace):
    """ The command responsible for registering accounts"""
    uid = genshin.get_uid()

    if uid is None:
        print("ERROR: Could not determine UID, did you log into the game yet?")
        sys.exit(1)

    user_reg_data = genshin.read_user_registry()

    if user_reg_data is None:
        print("ERROR: Could not read registry entry, "
              "did you log into the game yet?")
        sys.exit(1)

    config.set_user_registry(uid, user_reg_data)

    if args.name is not None:
        config.set_account_name(uid, args.name)
        print(f"Successfully registered account '{uid}' under the8"
              f" name '{args.name}'.")
        sys.exit(0)

    print(f"Successfully registered account '{uid}'.")


def switch_command(args: Namespace):
    """ The command responsible for switching accounts"""
    uid = args.uid

    accounts_dir = Path(config.get_config_directory(), "accounts")

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
            uid = file.name
            print(f"* [{index}] {format_uid(uid)} {check_if_selected(uid)}")
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
            print(f"* [{index}] {format_uid(str(acc))} "
                  f"{check_if_selected(str(acc))}")
        sys.exit(1)

    user_reg_data = config.get_user_registry(uid)

    if user_reg_data is None:
        print(f"ERROR: User Registry for {format_uid(uid)} does not exist.")
        sys.exit(1)

    backup_current_account_if_possible()

    genshin.write_uid(uid)
    genshin.write_user_registry(user_reg_data)

    print(f"Successfully switched to account {format_uid(uid)}")


def current_command(_args: Namespace):
    """ Shows your currently selected uid """
    uid = genshin.get_uid()

    if uid is None:
        print("No account could be found, have you logged into the game yet?")
        sys.exit(0)

    print(f"Currently selected account: {format_uid(uid)}")


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


def setname_command(args: Namespace):
    """ Allows you to set account alias names via CLI """
    if not config.is_account_registered(str(args.uid)):
        print(f"ERROR: Unknown account uid '{args.uid}', "
              "did you already register it?")
        sys.exit(1)
    config.set_account_name(str(args.uid), args.name)
    print(f"Successfully saved {format_uid(str(args.uid))}")


def format_uid(uid: str) -> str:
    """ Displays the account name if available otherwise just the uid"""
    name = config.get_account_name(uid)
    if name is None:
        return f"'{uid}'"
    return f"{name} ({uid})"


def check_if_selected(uid: str) -> str:
    """ Renders a check if the uid is selected right now """
    return "✔️" if uid == str(genshin.get_uid()) else ""


if __name__ == "__main__":
    main()
