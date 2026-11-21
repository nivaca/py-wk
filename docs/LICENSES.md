Open-source software in py-wtk
==============================

py-wtk is free software, under the GNU General Public License, version 3
or later (the file `LICENSE`).  Its own code uses only the standard
library of Python, so what other software comes with it depends on how it
is installed: the zip and the RPM bring nothing but the program, and the
AppImage brings a whole Python.  This list gives each piece of software,
what it is used for, and its licence (with its SPDX identifier).

The text of the entries is not software: it comes from the English
Wiktionary and its authors, under the licence CC BY-SA 4.0
(<https://creativecommons.org/licenses/by-sa/4.0/>).  py-wtk only shows it.


What the program uses
---------------------

These are needed by every form of py-wtk.  With the zip they are the
user's own; with the RPM, Fedora's; with the AppImage, those inside it.

| Software | Used for | Licence |
|---|---|---|
| Python 3.15, with its standard library | the whole program | Python Software Foundation License (`Python-2.0.1`) |
| Tcl/Tk (Tk 8.6 in the AppImage, Tk 9 in Fedora) | the window, through `tkinter` | Tcl/Tk licence (`TCL`) |
| ncurses | the terminal interface, through `curses` | X11 licence (`MIT-open-group`) |


The AppImage
------------

The AppImage carries a Python of its own: a relocatable build of Python
3.15 made by the python-appimage project
(<https://github.com/niess/python-appimage>, whose build scripts are under
`GPL-3.0`).  Besides Python, that build has these libraries, which are in
the AppImage as they come:

| Library | Version | Used by | Licence |
|---|---|---|---|
| Tcl and Tk | 8.6.18 | `tkinter` (the window) | `TCL` |
| Xft, Xrender | | Tk, to draw the text | `HPND-sell-variant` |
| ncurses (`ncursesw`, `panelw`, `tinfo`) | 5 | `curses` (the terminal interface) | `MIT-open-group` |
| OpenSSL | 3 | `ssl` (HTTPS to Wiktionary) | `Apache-2.0` |
| GNU Readline | 6.2 | `readline` (line editing in `py-wtk -i`) | `GPL-3.0-or-later` |
| GNU dbm | 1.10 | `dbm` (not used by py-wtk) | `GPL-3.0-or-later` |
| SQLite | 3.54.1 | `sqlite3` (not used by py-wtk) | public domain (`blessing`) |
| bzip2 | 1.0.6 | `bz2` (not used by py-wtk) | `bzip2-1.0.6` |
| XZ Utils (liblzma) | 5.2.2 | `lzma` (not used by py-wtk) | public domain |
| Zstandard | 1.5.7 | `compression.zstd` (not used by py-wtk) | `BSD-3-Clause OR GPL-2.0-only` |
| libffi | | `ctypes` (to read the X resources) | `MIT` |
| mpdecimal | 4.0.1 | `decimal` (not used by py-wtk) | `BSD-2-Clause` |

The same build has a few Python packages, of which py-wtk uses only
certifi:

| Package | Used for | Licence |
|---|---|---|
| certifi | the certificates for HTTPS (the AppImage points `SSL_CERT_FILE` to them) | `MPL-2.0` |
| pip, build, pyproject_hooks | nothing (they come with the Python) | `MIT` |
| packaging | nothing (it comes with the Python) | `Apache-2.0 OR BSD-2-Clause` |

And two more things go into the AppImage:

| Software | Used for | Licence |
|---|---|---|
| The terminal descriptions of ncurses (terminfo) | so that the terminal interface starts on any system; made with `infocmp` and `tic` from the builder's ncurses | `MIT-open-group` |
| The AppImage runtime (type2-runtime) | starting the AppImage; appimagetool puts it in | `MIT` |


The RPM
-------

The RPM brings only the program.  It runs on the Python and Tk of Fedora,
which it installs as dependencies:

| Fedora package | Licence (as Fedora gives it) |
|---|---|
| `python3`, `python3-tkinter` | `Python-2.0.1` (`python3-libs` adds parts under `MIT`, `BSD-3-Clause`, `Apache-2.0` and other permissive licences) |
| `tk`, `tcl` | `TCL` (with small parts under other licences) |
| `ncurses-libs` | `MIT-open-group` |
| `hicolor-icon-theme` | `GPL-2.0-or-later` |


Tools used to make it
---------------------

These are used to build, test and publish py-wtk.  None of them goes into
what is distributed.

| Tool | Used for | Licence |
|---|---|---|
| Git | the history of the code | `GPL-2.0-only` |
| appimagetool | making the AppImage | `MIT` |
| RPM (`rpmbuild`, `rpmsign`), rpmdevtools | building and signing the RPM | `GPL-2.0-or-later` |
| desktop-file-utils | checking the menu entries in the RPM | `GPL-2.0-or-later` |
| GnuPG | signing the RPM | `GPL-3.0-or-later` (with parts under other licences) |
| copr-cli | sending the RPM to Copr | `GPL-2.0-or-later` |
| GitHub CLI (`gh`) | publishing the releases on GitHub | `MIT` |
| tea | publishing the releases on Codeberg | `MIT` |
| Inkscape | drawing the icons from the SVG (`tools/icons.py`) | `GPL-2.0-or-later` |
| Pillow | making the `.ico` and `.icns` icons | `MIT-CMU` |
| Xvfb (X.Org) | a hidden display for the screenshots | `MIT` |
| ImageMagick | taking the screenshots of the window | `ImageMagick` |
| tmux | a hidden terminal for the screenshots of the terminal programs | `ISC` |
| Chromium | turning those terminals into images (Google Chrome can be used instead, but it is not open source) | `BSD-3-Clause` |
