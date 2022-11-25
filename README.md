# genshin-account-switcher

Simple CLI based account switcher for Genshin Impact on Linux.

## Installation

You need to have Python 3.10+ installed.

```bash
$ pip install genshin-account-switcher
```

## Usage

### Registering an account:

```bash
$ genshin-account-switcher register
Successfully registered account '999999999'.
```

### Switching between accounts:

```bash
# No argument -> shows list of registered accounts
$ genshin-account-switcher switch  
usage: main.py switch [-h] [uid]

positional arguments:
  uid

options:
  -h, --help  show this help message and exit

Available UIDs:
* [0] 888888888
* [1] 999999999

# Pick one via the UID itself or the shortcut
$ genshin-account-switcher switch 888888888
Successfully switched to account '888888888'

$ genshin-account-switcher switch 1
Successfully switched to account '999999999'
```

## License

GNU General Public License v3

![](https://www.gnu.org/graphics/gplv3-127x51.png)