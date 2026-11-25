# Changelog

All notable changes to py-wk (called py-wtk up to 1.15, and py-wkt before
1.4). The releases, with the zip, the AppImage, the signed RPM and (since
1.17) the signed `.deb`, are on
[Codeberg](https://codeberg.org/nivaca/py-wk/releases) and
[GitHub](https://github.com/nivaca/py-wk/releases); the RPM
is also on [Copr](https://copr.fedorainfracloud.org/coprs/nivaca/py-wk/)
(up to 1.15, in [nivaca/py-wtk](https://copr.fedorainfracloud.org/coprs/nivaca/py-wtk/)).
The entries keep the names each version had.
The git history begins with 1.4: versions 1.0 to 1.3 are taken from the
release notes in `docs/NOTES.md`, which give no dates.

## Unreleased

- `tools/zenodo.py`: the description of the deposit is now the whole
  README of the tag, in HTML. The draft also gets the contributor (the
  project leader), the languages, the copyright, the repository on GitHub,
  the programming language and the development status, these last through
  Zenodo's records API (its deposit API doesn't take them). The token can
  be kept in the desktop keyring (`secret-tool store --label="Zenodo
  token" service zenodo`) instead of `$ZENODO_TOKEN`; `tools/zenodo.py
  check-token` says whether there is one.

- `tools/zenodo.py` prepares the deposit of a release for Zenodo. `collect`
  puts in `dist/zenodo/` the tree of the tag as
  `py-wk-VERSION-source.tar.gz`, with its signature, a signed `SHA256SUMS`
  of the deposit and the public key, and checks every signature with only
  that key (`--packages` adds the files of the release). `upload` sends it
  to Zenodo as a draft, a new version of the deposit if there is one
  already, and never publishes it. `tools/release.py` now collects the
  deposit after the tag and uploads it as a draft, unless `--no-zenodo`. The
  metadata are in `.zenodo.json`.

## 1.18 — 2026-11-22

- **Every release signed**: besides the RPM, each file published (the
  zip, the AppImage, the `.deb`) comes with its signature (`.asc`), with
  `SHA256SUMS` and its signature, and with the public key
  (`RPM-GPG-KEY-py-wk`); the tag of the version is signed too. Each
  signature is checked with the published key before anything is
  published. The README says how to check a download.
- `tools/release.py` always makes the signed RPM now (`--no-rpm` leaves
  it out; `--rpm` is still accepted, and does nothing).

## 1.17 — 2026-11-21

- A `.deb` package for Debian, Ubuntu and their derivatives
  (`py-wk_1.17-1_all.deb`), with a detached signature (`.deb.asc`) by the
  key of the RPM; it installs the same files as the RPM and needs the
  system's `python3` to be 3.15 or later.
- `packaging/build-deb.py` makes it, with the Python standard library
  only; `tools/release.py` attaches it to the releases (`--no-deb` does
  not).

## 1.16 — 2026-11-21

- **Renamed py-wk** (it was py-wtk): the commands `py-wk`, `py-wk-tui`
  and `py-wk-gui`, the installer `py-wk-install.py`, the RPM package,
  the settings folder `~/.config/py-wk`, the cache `~/.cache/py-wk`, the
  variable `PY_WK_CONFIG` and the repositories `nivaca/py-wk`.
- The settings of `~/.config/py-wtk` move once to the new folder (before
  those of `~/.config/py-wkt`); `PY_WTK_CONFIG` is still read.
- `py-wk-install.py` removes the menu entries and icons it had added as
  py-wtk or py-wkt.
- The RPM is on Copr as `nivaca/py-wk`; the package replaces py-wtk.

## 1.15 — 2026-11-21

- `docs/LICENSES.md` and `docs/LICENCIAS_es.md` list the open-source
  software that py-wtk uses or carries in the AppImage, with its
  licences, and the tools that make py-wtk; the READMEs point to them,
  and the RPM has them among its documents.
- This changelog, in English and in Spanish.

## 1.14 — 2026-11-20

- **The text follows the scaling of a hi-res display.** On a display
  scaled to 200%, the window's text could come out at half its size:
  Tk 9, which the RPM uses, leaves the sizes of the fonts to fontconfig,
  and a rule in the user's fontconfig settings that fixed the DPI (at 96,
  for instance) won over the desktop's scaling. The window now gives
  fontconfig the desktop's DPI, after the user's own rules.
- The size of the window is kept in pixels at 96 DPI and scaled when it
  opens, like the width of the contents pane, so a size saved at 100% is
  not too small at 200%.
- The contact address in the files and the package is
  nicolasvaughan@proton.me.
- `packaging/build-rpm.sh` copies the newest RPM to `dist/` too, in place
  of the older ones there.

## 1.13 — 2026-11-14

- Python 3.15 or later is needed (it was 3.13). The AppImage carries its
  own Python 3.15. The RPM is built for Fedora 45 and later; Fedora 44,
  whose Python is 3.14, is no longer built on Copr.

## 1.12 — 2026-11-14

- Python 3.13 or later is needed (it was 3.11): the check of
  `version.py`, the RPM and the documents.

## 1.11 — 2026-11-14

- No Flatpak any more: `packaging/flatpak/` and `tools/bundle-flatpak.py`
  are removed, and releases carry again only the zip, the AppImage and
  the RPM. The Flatpak was also taken off the 1.10 release.
- The READMEs, the descriptions and the comments of the code read more
  plainly, in English and in Spanish; the program is the same.

## 1.10 — 2026-11-13

- **Copying and pasting.** The window has an Edit menu with Cut, Copy and
  Paste (Ctrl+X, Ctrl+C, Ctrl+V) for the search box, the languages and
  the find box, and Copy for the text selected in the entry. In the
  terminal interface, `y` (or F7) copies the whole entry as plain text,
  through the clipboard program of the system or, if there is none,
  through the terminal itself (OSC 52).
- A Flatpak, attached to the release (removed again in 1.11).
- The rows of the contents pane are as tall as their text, so they no
  longer overlap with a bigger text (Ctrl++) or on a scaled display.

## 1.9 — 2026-11-13

- The terminal interface starts in the AppImage. Its Python could not
  read how most terminals describe themselves (those with 256 colours),
  and `py-wtk-tui` stopped with "setupterm: could not find terminal". The
  AppImage now carries those descriptions in a form it can read.

## 1.8 — 2026-11-12

- **A new icon**: the bracketed `pW`, drawn with shapes instead of a font,
  in white and cream on a teal tile, with an amber stress mark. Run
  `py-wtk-install.py` again to get it in the applications menu.
- **A new signing key for the RPM**: `8187 0643 CA22 1AF9 0C30 554E BE68
  32CD 3599 4948` (ed25519, until 2029), pinned in `build-rpm.sh`, with
  its public key in `packaging/RPM-GPG-KEY-py-wtk` and in each release.
  An earlier RPM from a release needs `sudo rpm --import
  RPM-GPG-KEY-py-wtk` once; the package from Copr is not affected.

## 1.7 — 2026-11-11

- **The window follows the desktop's scaling on hi-res displays.** The
  window of the AppImage came out very small with the desktop scaled (at
  200% in Plasma, for instance), as its Tk ignored `Xft.dpi`. It now reads
  it, and the text and the window grow with it.
- **A package for Fedora**: an RPM that uses the Python and Tk of the
  system and adds the three programs to the `PATH` and to the
  applications menu. It is on Copr (`sudo dnf copr enable nivaca/py-wtk
  && sudo dnf install py-wtk`), and the releases have it too, signed.
  `tools/release.py --rpm` attaches it.

## 1.6 — 2026-11-06

- `py-wtk-install.py --uninstall` removes from the applications menu only
  the `.desktop` files and icons that the installer made; an entry of the
  same name that it did not write is left alone, and so are links.
  `--only-gui` follows the same rule.
- With a pager other than `less` (for example `PAGER=most`), the links of
  a long entry showed up as stray characters such as `^[]8;;`. With any
  other pager the entry is now shown without links, keeping its colours.
- New screenshots, and the description documents `DESCRIPTION.md` and
  `DESCRIPCIÓN_es.md`, in the structure of py-words.

## 1.5 — 2026-11-05

- A link to another entry opens it at the top, with all the languages of
  the filter, in the window and in the terminal interface. Before, it
  jumped to the language of the link (`rosa#Latin` scrolled to Latin),
  and it seemed that the language had changed. A link to another part of
  the same entry still goes there.

## 1.4 — 2026-11-05

- `py-wtk --set NAME=VALUE` and `py-wtk --unset NAME` failed with an
  error instead of changing the setting. They work again, and a wrong or
  ambiguous name (`--set links=false` matches both `cli.links` and
  `gui.links`) is reported clearly.
- The three programs show the same messages: the size of the disk cache
  ("2 pages, 192.7 KB"), a language that the page does not have. In the
  window, "Open in browser" and "Clear disk cache" say in the status line
  what they did; on the command line, a network error while searching
  (`-s`) gives a clear message.
- `py-wtk-install.py --only-gui` adds only the window to the applications
  menu, and removes the entries of the other two if an earlier run added
  them.
- The code that each program had on its own (history, links, messages,
  disk cache, common options) is now in `pywtk/common.py`.
- The scripts that make the bundles are in `tools/`
  (`bundle-zip.py`, `bundle-appimage.py`), and `tools/icons.py` makes all
  the icons again from `icons/py-wtk.svg`.

## 1.3

- The icon has a white background, and the letters are better centred.
  The icons of every size are made again from it, and the screenshots of
  the README are updated.

## 1.2

- **Clickable links** in all three programs. A link to another entry opens
  it in the program; the other links (Wikipedia, the appendices of
  Wiktionary, other dictionaries) open in the web browser. In the window
  they are underlined under the mouse (setting `gui.links`); in the
  terminal interface a click opens them and `L` lists them; on the command
  line they are OSC 8 hyperlinks (setting `cli.links`).
- **Interactive command line**: `py-wtk -i` asks for one word after
  another; Ctrl-D or Ctrl-C ends it.
- `py-wtk-install.py` also adds `py-wtk (CLI)` to the applications menu,
  which opens `py-wtk -i` in a terminal; the entries are only in the
  categories Office and Dictionary.
- `py-wtk-tui` started without a terminal says so, instead of failing
  with a curses error.

## 1.0

- First version of the new py-wtk, a program for reading the English
  Wiktionary without a web browser: the whole entry (etymology,
  pronunciation, definitions, inflection tables, translations and the
  rest), for all the languages of the page or only those chosen. It comes
  as a command line (`py-wtk`), a terminal interface (`py-wtk-tui`) and a
  window (`py-wtk-gui`), with settings shared between them, a disk cache,
  a zip and an AppImage, and `py-wtk-install.py` to add the programs to
  the applications menu.
