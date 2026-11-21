# py-wk

*[Leer en español](README.es.md)*

py-wk is a small program for consulting the
[English Wiktionary](https://en.wiktionary.org) without opening the web browser. It
comes in three flavours, and all of them use the same code inside:

| Program      | What it is                                                   |
|--------------|--------------------------------------------------------------|
| `py-wk`      | command-line tool, it prints the entry in the terminal       |
| `py-wk-tui`  | full-screen terminal interface (curses)                      |
| `py-wk-gui`  | desktop window (Tkinter)                                     |

It shows the complete entry, not only the definitions: etymology, pronunciation,
definitions with examples and quotations, usage notes, inflection tables (declensions,
conjugations), synonyms, derived and related terms, descendants, translations, references
and further reading. By default it shows **all the languages** of the page, but you can
choose only the ones you need, for example only Latin, or Latin and Spanish.

py-wk was called **py-wtk** up to version 1.15, and **py-wkt** before 1.4. The new name
changes the commands, the settings folder and the repositories; the settings of the old
names move to the new folder by themselves (see [Settings](#settings)).

I am Nicolás Vaughan (<nicolasvaughan@proton.me>), and I wrote
it in 2026.

[Nicolas Vaughan](https://artehum.uniandes.edu.co/profesores/nicolas-vaughan/) is Associate
Professor of Literature at the School of Arts and Humanities of the Universidad de los
Andes, Bogotá, Colombia.

## Screenshots

Here is the same word, *rosa* (only its Latin entry, with `-l la`), in the window
(`py-wk-gui`, here in dark mode):

![The window, in dark mode](docs/img/gui_dark.png)

the window in light mode:

![The window, in light mode](docs/img/gui_light.png)

in the command line (`py-wk`, here brief, with `-b`):

![The command line](docs/img/cli.png)

and in the terminal, in full screen (`py-wk-tui`):

![The terminal, full screen](docs/img/tui.png)

These four pictures are made by `python3 tools/screenshots.py`, which runs each program
out of sight, with settings of its own, and writes them to `docs/img/` (see
[For developers](#for-developers)).

## Requirements

- Python 3.15 or newer.
- Nothing more for `py-wk` and `py-wk-tui`: only the standard library is used; there are
  no packages to install with pip.
- For `py-wk-gui` you need Tkinter. In many Linux distributions it comes in a separate
  package: `python3-tkinter` in Fedora, `python3-tk` in Debian and Ubuntu.
- Of course, an Internet connection.

## Installation

**The easy way, in Linux:** download the AppImage of the latest release
(`py-wk-v.VERSION-x86_64.AppImage`), make it executable and run it. It has its own Python
inside, so you don't need to install anything:

```sh
chmod +x py-wk-v.*-x86_64.AppImage
./py-wk-v.*-x86_64.AppImage            # the window
./py-wk-v.*-x86_64.AppImage cli rosa   # the command line (also: tui; help lists them)
```

A link to the AppImage named `py-wk`, `py-wk-tui` or `py-wk-gui` starts that program.

**In Fedora:** install the RPM package, which uses the Python and Tk of the system and adds
the three programs to the `PATH` and to the applications menu, with their icon. The easiest
way is from [Copr](https://copr.fedorainfracloud.org/coprs/nivaca/py-wk/), so
`dnf upgrade` brings each new version:

```sh
sudo dnf copr enable nivaca/py-wk
sudo dnf install py-wk
```

If you had installed py-wtk from Copr, change the repository; the package py-wk replaces
the package py-wtk:

```sh
sudo dnf copr disable nivaca/py-wtk
sudo dnf copr enable nivaca/py-wk
sudo dnf install py-wk
```

The releases also have the RPM (`py-wk-VERSION-1.fcNN.noarch.rpm`), signed, with its
public key (`RPM-GPG-KEY-py-wk`, to import once): `sudo rpm --import RPM-GPG-KEY-py-wk`
and then `sudo dnf install ./py-wk-*.noarch.rpm`. It works in any Fedora with Python 3.15
or newer, whatever the `fc` number. Or build it from the folder of the program (a git clone):

```sh
sudo dnf install rpm-build python3-devel desktop-file-utils python3-tkinter
packaging/build-rpm.sh
sudo dnf install build/rpm/RPMS/noarch/py-wk-*.rpm
```

The program goes into `/usr/share/py-wk`, with links in `/usr/bin`.

**In Debian, Ubuntu and their derivatives:** the releases also have a `.deb` package
(`py-wk_VERSION-1_all.deb`), which uses the Python and Tk of the system and adds the three
programs to the `PATH` and to the applications menu, like the RPM. It needs Python 3.15 or
newer as the system's `python3`, so for now it installs only where the distribution has
it; elsewhere, use the AppImage. The package is signed apart (`py-wk_VERSION-1_all.deb.asc`)
with the same key as the RPM; check it, if you want, and install it with `apt`:

```sh
gpg --import RPM-GPG-KEY-py-wk
gpg --verify py-wk_*_all.deb.asc py-wk_*_all.deb
sudo apt install ./py-wk_*_all.deb
```

Or build it from the folder of the program, in any Linux (it needs only Python and git):
`python3 packaging/build-deb.py` writes it into `build/deb/` and copies it to `dist/`.

**With your own Python** (any system): download the zip of the latest release
(`py-wk-v.VERSION.zip`), or clone the repository, put the folder wherever you want, and
make links to the three launchers in a directory that is in your `PATH`:

```sh
ln -s ~/py-wk/py-wk      ~/.local/bin/
ln -s ~/py-wk/py-wk-tui  ~/.local/bin/
ln -s ~/py-wk/py-wk-gui  ~/.local/bin/
```

The launchers find the `pywk` package next to them, even when you call them through a
link. You can also run the command-line tool with `python3 -m pywk WORD` from inside the
folder.

**In the applications menu:** `py-wk-install.py` adds the window, the terminal version and
the command line (`py-wk (GUI)`, `py-wk (TUI)` and `py-wk (CLI)`, the last one with
`-i`, which asks for one word after another), with their icon, to the applications menu in
Linux, the Start menu in Windows, or `~/Applications` in macOS. It writes only to your own
folders, so no administrator rights are needed:

```sh
python3 py-wk-install.py               # add them
python3 py-wk-install.py --only-gui    # add only the window
python3 py-wk-install.py --uninstall   # remove them
```

With `--only-gui`, if an earlier run added the terminal version and the command line, their
entries are removed.

The entries start the program from its folder, so if you move the folder, run it again.

## Command line: `py-wk`

```sh
py-wk rosa                       # full entry, all languages
py-wk rosa -l la                 # only Latin
py-wk rosa -l Latin              # the same, with the name of the language
py-wk rosa -l la,es,it           # several languages
py-wk rosa -b                    # brief: only the definitions
py-wk rosa -l la -o etymology    # only some sections
py-wk house -x translations,quotations,tables   # hide some sections
py-wk hablar -l es -o conjugation
py-wk ice cream                  # expressions of several words, no quotes needed
py-wk -s recei                   # search page titles
py-wk house --json               # structured JSON, for use in other programs
py-wk -i                         # asks for one word after another (also: rosa -l la)
```

Options:

| Option                  | Meaning                                                          |
|----------------------------|------------------------------------------------------------------|
| `-l`, `--lang`          | languages, by code (`la`, `grc`) or name (`Latin`); `all` is the default |
| `-o`, `--only`          | show only these sections (separated by commas)                   |
| `-x`, `--exclude`       | hide these sections; `quotations` and `tables` are also accepted |
| `-b`, `--brief`         | only the definitions, without etymology, quotations, tables…     |
| `-s`, `--search`        | search page titles instead of showing an entry                   |
| `-F`, `--full`          | full entry, also when the setting `cli.brief` is on              |
| `-n`, `--limit`         | how many results for `--search` (default 10)                     |
| `-i`, `--interactive`   | then ask for more words, one per line, with options if you want; `Ctrl-D` ends |
| `--json`                | output in JSON                                                   |
| `--no-color`            | without colours (also respected: the `NO_COLOR` variable)        |
| `--no-pager`            | don't use `less` for the long entries                            |
| `--refresh`             | download the page again, without using the disk cache            |

The options for the settings (see [Settings](#settings) below): `--settings`,
`--configure`, `--set`, `--unset`, `--edit-settings` and `--clear-cache`.

Section names are compared ignoring capital letters and numbers, so `etymology` matches
"Etymology 1" and "Etymology 2". When the word doesn't exist, the program suggests similar
words. When the entry is longer than the screen, it is opened in `less`
(or in your `$PAGER`).

The links of the entry are hyperlinks: in the terminals that support them (most modern
ones, and `less`) you can click them, usually with `Ctrl` pressed. Other pagers (such as
`most` or `more`) can't show them, so in those the entry is shown without links. If your
terminal shows them as stray characters, turn off the setting `cli.links`.

The exit code is `0` if all is fine, `1` if nothing was found and `2` for network errors.

## Terminal interface: `py-wk-tui`

```sh
py-wk-tui            # starts with an empty screen; press / for search
py-wk-tui rosa       # opens directly the word
py-wk-tui rosa -l la
```

On the left there is a table of contents with the languages and the sections, on the right
the entry. Main keys (press `?` inside the program for the complete list):

| Key                  | Action                                          |
|----------------------|-------------------------------------------------|
| `/`                  | look up a word (in the prompt, `Tab` gives suggestions) |
| `j` `k`, arrows      | scroll                                          |
| `Space`, `PgDn` `PgUp` | scroll a page                                 |
| `[` `]`              | previous / next section                         |
| `{` `}`              | previous / next language                        |
| `c` or `Tab`         | go to the contents pane                         |
| `t`                  | show / hide the contents pane                   |
| `f`, `n` `N`         | find in the page, next / previous match         |
| `l`                  | change the languages                            |
| `b` `B`              | back / forward in the history                   |
| `L`                  | list of the links on the screen, to open one    |
| `x` `T`              | show / hide quotations, tables                  |
| `o`                  | open the page in the web browser                |
| `y` or `F7`          | copy the whole entry, as plain text             |
| `S`                  | settings                                        |
| `q`                  | quit                                            |

The mouse wheel also works, and you can click on the contents and on the links (in blue).

`y` copies the entry through the system's clipboard program (`wl-copy` in Wayland,
`xclip` or `xsel` in X11, `pbcopy` in macOS, `clip` in Windows); if there is none, it asks
the terminal to do it (OSC 52, also inside tmux when it allows it), which many terminals do.
The links to other entries open in the program, at the top of the entry; the others
(Wikipedia, the appendices of Wiktionary, other dictionaries…) in the web browser.

## Desktop window: `py-wk-gui`

```sh
py-wk-gui
py-wk-gui rosa -l la
py-wk-gui rosa --dark --size 13       # dark and bigger only this time (--light also exists)
```

- Search box with suggestions while you write (arrow down to choose one).
- **Click a link to open it.** The links to other entries open in the window, at the
  top of the entry and with the languages of the filter; the others (Wikipedia, the
  appendices of Wiktionary, other dictionaries…) in the web browser. The status line
  says where a link goes.
- **Double-click any word of the entry to look it up.** The right button gives a menu with
  "Look up", "Copy" and "Select all".
- An *Edit* menu with Cut, Copy and Paste (`Ctrl+X`, `Ctrl+C`, `Ctrl+V`): they act on the
  search box, the languages and the find box, and Copy also on the text selected in the
  entry. What can't be done at the moment is greyed out.
- Contents tree: click a section to go there; it follows you when you scroll.
- Language selector with the languages of the current page; you can also write `en,la`.
- Checkboxes to show or hide quotations and tables.
- Find in the page (`Ctrl+F`, then `F3` / `Shift+F3`), with all the matches highlighted.
- Back and forward (`Alt+←`, `Alt+→`), reload (`F5`), open in the browser.
- Light and dark mode for the whole window: the moon ☾ at the bottom right makes it dark,
  the sun ☀ makes it light again (also *View → Dark mode*). The choice is remembered.
- Bigger and smaller text with `Ctrl++` and `Ctrl+-` (all the text of the window, not only
  the entry), and `Ctrl+0` for the usual size.
- Settings window (`Ctrl+,`, the "⚙ Settings" button or *File → Settings…*).
- The pages are loaded in the background, so the window doesn't freeze.

The text uses a monospace font, so that the tables of declensions and conjugations stay
well aligned.

## Settings

The three programs share one settings file, `config.toml`, in the usual settings folder of
the system:

| System  | File                                                       |
|---------|------------------------------------------------------------|
| Linux   | `~/.config/py-wk/config.toml` (or `$XDG_CONFIG_HOME/py-wk/`) |
| macOS   | `~/Library/Application Support/py-wk/config.toml`          |
| Windows | `%APPDATA%\py-wk\config.toml`                              |

With the variable `PY_WK_CONFIG` you can name another folder. The file is
[TOML](https://toml.io), divided into sections: `[general]`, `[cli]`, `[tui]`, `[gui]`,
`[fonts]` and `[appearance]`. Each setting can be left out, and then it has its usual
value; in the file, the ones left out appear commented, with their usual value, and each
setting has a comment that explains it. So you can also edit it by hand. If some value is
not valid, the program tells you and uses the usual one.

The programs write to the file only the settings that you change, over the file as it is
at that moment: if the window and the terminal interface are open at the same time, one
doesn't undo the changes of the other. Restoring the usual value of a setting removes it
from the file. When the file is written again, your own comments are not kept.

(Earlier versions were called **py-wtk** and, before them, **py-wkt**. If you used them,
their settings move once to the new folder: the `config.toml` of `~/.config/py-wtk/` or, if
there is none, of `~/.config/py-wkt/` (or its older `settings.ini`); the old file is
renamed `*.old`. The variables `PY_WTK_CONFIG` and `PY_WKT_CONFIG` are still read. The
pages kept in `~/.cache/py-wtk` are not moved; that folder can be deleted.)

What you can change:

| Setting                         | Default | What it does                                     |
|---------------------------------|---------|--------------------------------------------------|
| `general.languages`             | `all`   | languages shown when you don't give `-l`         |
| `general.preferred_languages`   | (empty) | these languages go first, e.g. `la, en`          |
| `general.show_quotations`       | `true`  | the dated quotations under the definitions       |
| `general.show_tables`           | `true`  | declension and conjugation tables                |
| `general.show_translations`     | `true`  | the translations (in big entries they are long)  |
| `general.hidden_sections`       | (empty) | sections never shown, e.g. `anagrams, references`|
| `general.search_results`        | `10`    | number of results and suggestions                |
| `general.max_width`             | `110`   | maximum width of the text, in characters         |
| `general.cache_days`            | `1`     | days that the downloaded pages stay on disk (0 = no cache) |
| `cli.color`                     | `auto`  | `auto`, `always` or `never`                      |
| `cli.pager`                     | `auto`  | `auto`, `always` or `never`                      |
| `cli.pager_command`             | (empty) | pager to use instead of `$PAGER` / `less`        |
| `cli.links`                     | `true`  | clickable links, in the terminals that can       |
| `cli.brief`                     | `false` | brief mode always (then `-F` gives the full entry) |
| `tui.show_contents`             | `true`  | the contents pane                                |
| `tui.contents_width`            | `30`    | its width, in columns                            |
| `tui.colors`                    | `true`  | colours in the terminal interface                |
| `tui.mouse`                     | `true`  | use of the mouse; off to select text as normal   |
| `tui.wheel_lines`               | `3`     | lines for each step of the wheel                 |
| `gui.show_contents`             | `true`  | the contents pane                                |
| `gui.contents_width`            | `250`   | its width, in pixels                             |
| `gui.double_click_lookup`       | `true`  | double-click on a word looks it up               |
| `gui.links`                     | `true`  | the links of the entry can be clicked            |
| `gui.live_suggestions`          | `true`  | suggestions while you write                      |
| `gui.remember_window`           | `true`  | open the window with the last size               |
| `fonts.text_family`             | (empty) | font of the entries (better fixed-width); empty = the usual one |
| `fonts.text_size`               | `11`    | size of the entries                              |
| `fonts.ui_family`               | (empty) | font of the rest of the window; empty = the system's |
| `fonts.ui_size`                 | `0`     | its size; `0` = the system's                     |
| `appearance.dark_mode`          | `false` | dark window (left out of the file: light)        |

Ways to change them:

- **Command line:**
  ```sh
  py-wk --settings                         # list all, with the actual values
  py-wk --configure                        # small interactive menu
  py-wk --set general.languages=la,en      # change one (repeatable)
  py-wk --set preferred_languages=la       # the section can be omitted if not ambiguous
  py-wk --unset general.languages          # back to the default
  py-wk --edit-settings                    # open the file in $VISUAL / $EDITOR
  py-wk --clear-cache                      # delete the pages kept on disk
  ```
- **Terminal interface:** press `S`. Enter changes the selected setting (true/false and
  the choices change directly, the others ask for the value), `d` restores the default,
  `Esc` closes. The changes are saved at once.
- **Window:** *File → Settings…* (`Ctrl+,`, or the "⚙ Settings" button). The tabs are
  Appearance (dark mode and the fonts, with a list of the fixed-width fonts that are
  installed and a preview), Window, General (with a button to clear the disk cache),
  Terminal UI and Command line.

Some things are remembered automatically: in the TUI and the GUI, whether the quotations,
the tables or the contents pane are shown or hidden; in the GUI also the dark mode, the
size of the text (only what differs from the usual is written in `[fonts]`), the width of
the contents pane and the size of the window.

## How it works

The program downloads the page in HTML from the Wiktionary REST API
(`/api/rest_v1/page/html/…`) and converts it to text. Only the Python standard library is
used for this (`urllib`, `html.parser`, `textwrap`, `curses`, `tkinter`). The big entries,
like *house*, have the translations in a separate page (`house/translations`); py-wk
downloads it too and shows the translations in their place.

The downloaded pages are kept compressed in the cache folder of the system
(`~/.cache/py-wk` in Linux, `~/Library/Caches/py-wk` in macOS, `%LOCALAPPDATA%\py-wk\cache`
in Windows) for one day (setting `general.cache_days`), so looking up the same word again
is instantaneous and makes no new requests to Wiktionary. In the TUI and the GUI, *reload*
(`r`, `F5`) downloads the page again; in the command line, `--refresh`.

Organisation of the code:

```
py-wk, py-wk-tui, py-wk-gui   small launchers
pywk/
  api.py      download of pages, search, cache
  dom.py      HTML parsing
  text.py     cleaning of the text, width in the terminal, colours
  entry.py    languages, sections, filters and options
  config.py   reading and writing of config.toml
  settings.py the settings: what they are, their values (shared by the three programs)
  gui_theme.py  light and dark look of the window
  gui_fonts.py  fonts of the window
  render.py   conversion of an entry to text (shared by the three programs), JSON
  common.py   what the three programs share: options, messages, history, links
  cli.py      py-wk
  tui.py      py-wk-tui
  gui.py      py-wk-gui
  version.py  name, version, the commit it was made from, the Python needed
icons/        the icons (Linux, macOS, Windows)
```

## For developers

Five scripts, in `tools/`, make the bundles, publish the releases, take the screenshots and
make the icons. They are not in the bundles.

| Script                     | What it does                                                   |
|----------------------------|----------------------------------------------------------------|
| `tools/bundle-zip.py`      | makes `dist/py-wk-v.VERSION.zip`: the program, the icons and the documents, without hidden files, `__pycache__` or the tools, with a `COMMIT` file (shown by `--version` and *About*). `--list` only lists the files. |
| `tools/bundle-appimage.py` | makes `dist/py-wk-v.VERSION-x86_64.AppImage`, with a Python of its own (from [python-appimage](https://github.com/niess/python-appimage)) and the program as in the zip. The first time it downloads that Python and [appimagetool](https://github.com/AppImage/appimagetool) into `~/.cache/py-wk-build`; `--python` and `--appimagetool` give them instead. |
| `tools/release.py`         | publishes the tag `vVERSION` on GitHub (`gh`) and Codeberg (`tea`) with the zip, the AppImage and the signed `.deb` (`--no-deb` leaves it out): it makes them, tags, pushes and makes or updates the releases. With `--rpm`, also the signed RPM and its key, and it sends the RPM to Copr (`copr-cli`; `--no-copr` does not). It shows the commands and asks first; `--dry-run` only shows them. See `--help`. |
| `tools/screenshots.py`     | takes the screenshots of the three programs into `docs/img/` (the window light and dark), with settings and cache of its own, so yours are not touched. It needs tmux, ImageMagick, Chrome or Chromium, and Xvfb or a display. |
| `tools/icons.py`           | makes all the icons again from `icons/py-wk.svg`: the PNGs, the Linux, macOS and Windows icons. Each size is drawn by Inkscape (also as a Flatpak) from the SVG; the `.icns` and the `.ico` are put together with Pillow. `--dry-run` only shows how Inkscape would be run. |

The RPM is made by `packaging/build-rpm.sh` from `packaging/py-wk.spec`, into `build/rpm/`.
`--sign` signs it with the project's key only (`SIGNING_KEY` in the script; `--sign=KEY` for
another one), and stops if that key is not in the machine's keyring. The releases are all
signed with the author's key, fingerprint `8187 0643 CA22 1AF9 0C30 554E BE68 32CD 3599 4948`; a copy of the public key is in
`packaging/RPM-GPG-KEY-py-wk`; `packaging/COPR.org` explains how it is published on Copr.

The `.deb` is made by `packaging/build-deb.py`, into `build/deb/` (and copied to `dist/`),
with nothing but the Python standard library, so it can be built in Fedora too. It installs
the same files as the RPM. `--sign` adds a detached signature (`.deb.asc`) with the same key.

The version is in `pywk/__init__.py`, and that of the RPM in `packaging/py-wk.spec`
(`rpmdev-bumpspec -n X.Y`).

## Notes

- Wiktionary limits the number of requests. If you make many in a short time you can get a
  "Too Many Requests" error; the program waits and retries a few times automatically, but
  if the error continues, wait a minute. The disk cache helps to avoid this.
- The content of the entries comes from Wiktionary and its authors, under the licence
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). py-wk only shows it;
  please respect this licence if you copy texts from the entries.
- py-wk is not an official project of Wiktionary or of the Wikimedia Foundation.

## Licence

Copyright © 2026 Nicolas Vaughan <nicolasvaughan@proton.me>

This program is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation, either version
3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the [LICENSE](LICENSE) file for more details.

The open-source software that py-wk uses or carries (in the AppImage), and the tools
used to make it, are listed with their licences in [docs/LICENSES.md](docs/LICENSES.md).
