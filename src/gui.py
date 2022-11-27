""" Graphical user interface for genshin account switcher """
import tkinter
from tkinter import DISABLED, NORMAL

try:
    from . import config, genshin, utils
except ImportError:
    import config
    import genshin
    import utils


def _create_wrapper(func, *args):
    return lambda: func(*args)


class GUI:
    """ Graphical user interface for genshin account switcher """
    def __init__(self):
        self._root = tkinter.Tk()
        self._account_buttons = []

        self._root.title("Genshin Account Switcher")
        self._root.minsize(300, 100)
        self._root.resizable(False, False)

        self._register_button = tkinter.Button(
            self._root,
            text="...",
            state=DISABLED,
            command=self._register_current
        )
        self._register_button.grid(row=0, column=0, columnspan=2, pady=5)

        rowindex = 1

        for uid in config.get_registered_accounts():
            switch_button = tkinter.Button(
                self._root,
                text=f"Switch to {utils.format_uid(uid)}",
                command=_create_wrapper(self._switch_to, uid)
            )
            switch_button.grid(
                row=rowindex,
                column=0,
                pady=(0, 5),
                padx=(5, 2),
                sticky="nsew"
            )
            edit_button = tkinter.Button(
                text="Edit",
                command=_create_wrapper(self._edit_account, uid)
            )
            edit_button.grid(row=rowindex, column=1, pady=(0, 5), padx=(2, 5))

            rowindex += 1

            self._account_buttons.append((uid, switch_button))
        self._update_button_states()

    def _update_button_states(self):
        if genshin.get_uid() not in config.get_registered_accounts():
            self._register_button.config(
                text=f"Register account {genshin.get_uid()}",
                state=NORMAL,
            )
        else:
            self._register_button.config(text="...", state=DISABLED)

        for uid, button in self._account_buttons:
            button.config(text=f"Switch to {utils.format_uid(uid)}")
            if uid == genshin.get_uid():
                button.config(state=DISABLED)
                continue
            button.config(state=NORMAL)

    def _register_current(self):
        uid = genshin.get_uid()

        if uid is None:
            return  # show error?

        user_reg_data = genshin.read_user_registry()

        if user_reg_data is None:
            return  # show error?

        config.set_user_registry(uid, user_reg_data)

        name = _open_input_field(f"name for '{uid}'", "")
        config.set_account_name(uid, name)

        self._update_button_states()

    def _switch_to(self, uid):
        user_reg_data = config.get_user_registry(uid)

        if user_reg_data is None:
            return  # show error?

        utils.backup_current_account_if_possible()

        genshin.write_uid(uid)
        genshin.write_user_registry(user_reg_data)

        self._update_button_states()

    def _edit_account(self, uid):
        current_name = config.get_account_name(f"name for '{uid}'")
        if current_name is None:
            current_name = ""
        new_name = _open_input_field(uid, current_name)
        config.set_account_name(uid, new_name)
        self._update_button_states()

    def quit(self):
        """ Quit the window """
        self._root.quit()

    def run(self):
        """ Run the window """
        self._root.mainloop()


def _open_input_field(field_name: str, current_value: str) -> str:
    value = {"result": ""}

    root = tkinter.Toplevel()
    root.title(f"Edit {field_name}")
    entry = tkinter.Entry(root)
    entry.insert(0, current_value)
    entry.grid(row=0, column=0, columnspan=2)

    def on_ok_selected():
        value["result"] = entry.get()
        root.destroy()

    ok_button = tkinter.Button(
        root,
        text="Ok",
        command=on_ok_selected,
    )
    ok_button.grid(row=0, column=2)
    root.grab_set()
    root.focus_set()
    root.wait_window()
    return value["result"]
