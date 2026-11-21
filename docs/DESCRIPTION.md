How py-wk was made
==================

*[Leer en español](DESCRIPCIÓN_es.md)*

py-wk is a small program for reading the English Wiktionary
(<https://en.wiktionary.org>) without a web browser.  You give it a word
or an expression in any language, and it shows the whole Wiktionary
entry, cleanly formatted, in the terminal or in a desktop window.
Nicolas Vaughan made it in 2026.  It was called *py-wkt* at first and
*py-wtk* up to 1.15; the current version is 1.17.  Here I explain how it
was made, in eight stages.

It is meant for people who look up words often: students and teachers
of languages (Latin, Greek, Spanish, English ...), translators,
philologists, and anyone who wants the information in Wiktionary without
the clutter and the slowness of the web page.  py-wk is free software,
under the GNU General Public License, version 3 or later.  The content
of the entries comes from Wiktionary and its contributors, under the
CC BY-SA 4.0 licence; py-wk only displays it, and it is not an official
project of Wiktionary or of the Wikimedia Foundation.  The program uses
Python and its standard library (under the Python Software Foundation
License), with Tcl/Tk and ncurses (under permissive licences); the
AppImage also carries the libraries of its own Python.  `docs/LICENSES.md`
lists all of them, and the tools that make py-wk, with their licences.

Nicolas Vaughan is Associate Professor of Literature at the School of Arts
and Humanities of the Universidad de los Andes, Bogotá, Colombia.

1. From HTML to text
--------------------

Wiktionary gives each page in HTML through its REST API
(`/api/rest_v1/page/html/...`).  py-wk downloads that HTML and converts
it to text by itself, with the standard library only: `urllib` for the
download, `html.parser` for reading the page into a small tree
(`dom.py`), and `textwrap` for the lines.  The page is then cut into its
languages and their sections (`entry.py`): etymology, pronunciation,
definitions with examples and dated quotations, usage notes, inflection
tables, synonyms, derived and related terms, descendants, translations,
references and further reading.

The inflection tables (declensions and conjugations) are kept aligned,
with the width that each character actually takes in the terminal
(`text.py`).  The big entries, like *house*, keep their translations in a
separate page (`house/translations`); py-wk downloads that page too and
puts the translations back in their place.

A Wiktionary page usually has many languages.  py-wk shows all of
them by default, but the user can choose only some (`-l la`, or
`-l la,es,it`), put some first, show only some sections
(`-o etymology`), hide others, or ask for a brief view with only the
definitions.

2. Three programs, one renderer
-------------------------------

py-wk comes in three forms: a command line (`py-wk`), a full-screen
terminal interface (`py-wk-tui`, with `curses`), and a desktop window
(`py-wk-gui`, with Tk, from the standard library).  All three turn an
entry into text with the same code (`render.py`), so an entry looks the
same, and contains the same things, in all of them.  The command line
can also give the entry as structured JSON (`--json`), for other
programs, and it has an interactive mode (`-i`) that asks for one word
after another.

The two full-screen programs add what is needed for reading long
entries: a table of contents by language and section, find in the page,
a history with Back and Forward, and reload.  The window has a light and
a dark look (`gui_theme.py`), adjustable fonts (`gui_fonts.py`), and
suggestions while you type; a double click on any word looks it up.  If
a word does not exist, similar words are proposed, and the titles of the
pages can be searched.

3. Settings and cache
---------------------

The three programs share one settings file, `config.toml`, in the usual
settings folder of each system (`~/.config/py-wk/` in Linux).  It can
be edited from the command line (`--set`, `--unset`), from a settings
screen in the terminal interface, from a settings window in the GUI, or
by hand.  `settings.py` says, in one place, what each setting is, its
type and its default value.  The programs write to the file only the
settings that you change, over the file as it is at that moment, so if
the window and the terminal interface are open at the same time, one
does not undo the changes of the other.

The versions called *py-wkt*, and later *py-wtk*, kept their settings
in other folders, first in a `settings.ini` and then in a `config.toml`.
py-wk reads them once, moves them to the new folder and renames the old
file `*.old` (see stage 7).

The downloaded pages are kept compressed in the cache folder of the
system for one day (`general.cache_days`), so looking up the same word
again is instant and puts no load on Wiktionary's servers.  When
Wiktionary answers "Too Many Requests" (or is busy for a moment), the
program waits (as long as the answer asks, if it says) and tries again
by itself.

4. Links
--------

In 1.2 the links of an entry started to work in all three programs.  A
link to another entry opens it in the program; the other links
(Wikipedia, the appendices of Wiktionary, other dictionaries) open in
the web browser.  Links to pages that do not exist yet, footnotes and
edit links are not clickable.

In the window the links have the link colour and get underlined
under the mouse, and dragging over one selects the text without opening
it.  In the terminal interface they are blue, a click opens them, and
the key `L` lists the links on the screen, to open one with the
keyboard.  In the command line they are terminal hyperlinks (OSC 8),
which most modern terminals and `less` make clickable; they are written
only along with colours, so `--json`, `--no-color` and the output to other
programs do not change.

Two corrections came later.  In 1.5, a link to another entry opens it
at the top, with all the languages of the filter: before, it jumped to
the language of the link, and the filter seemed to have changed.
In 1.6, a long entry opened in a pager other than `less` (for example
`PAGER=most`) showed its links as stray characters such as `^[]8;;`.
Only `less` can show these links, so with any other pager the entry is
now shown without them, keeping its colours.

5. Distribution
---------------

py-wk needs Python 3.15 or later and nothing else, so
it can be used from a zip or a clone of the repository, with three small
launchers to link into the `PATH`.  For Linux there is also an AppImage,
which carries its own Python: download, make it executable, run.  Since
1.7 there is an RPM for Fedora as well, on Copr and, signed, with the
releases: it uses the Python and Tk of the system, and puts the three
programs in the `PATH` and the applications menu.  The AppImage's Tk is
older (8.6) and ignores the scaling that the desktop gives to X11
programs (`Xft.dpi`), so on a scaled hi-res display its window came out
very small; since 1.7 the window reads that scaling itself.  The RPM's
Tk (9) reads it, but it leaves the sizes of the fonts to fontconfig, and
on one of my laptops, at 200%, a rule in my own fontconfig settings fixed
its DPI at 96: the window and its controls were scaled, and the text in
them was not.  Since 1.14 the window starts fontconfig with the usual
configuration plus one rule that sets the DPI of the desktop, and keeps
its size in pixels at 96 DPI, like the contents pane.  1.10 also
came as a Flatpak, for any Linux (its runtime's Python has no Tk, so
Tcl/Tk and Python's `_tkinter` were built into it), which was dropped
afterwards.  A small module, `version.py`, is read before the rest of
the program, and it stays readable by old versions of Python, so a
Python that is too old gets a clear message instead of an error.

`py-wk-install.py` adds the programs, with their icon, to the
applications menu in Linux, the Start menu in Windows or
`~/Applications` in macOS, writing only to the user's folders, so
no administrator rights are needed.  `--only-gui` adds only the window,
and `--uninstall` removes the entries and the icons that the installer
made, and nothing else.

The scripts in `tools/` make the zip and the AppImage, publish the
releases on GitHub and Codeberg (with the RPM, which `packaging/`
builds, and which goes to Copr too), take the screenshots of the
README, and make all the icons again from one SVG (since 1.8 the
bracketed `pW`, drawn with shapes rather than a font, on a teal tile).
The zip and the AppImage carry the commit they were made from, which
`--version` and *About* show.

6. One place for what is shared
-------------------------------

At first each program had its own copy of several things: the history
of Back and Forward, the handling of the links, the messages, the disk
cache, the common options.  In 1.4 they moved into one module,
`common.py`, so the three programs say the same thing in the same way
("2 pages, 192.7 KB" everywhere, the same message for a language that
the page does not have, the same message for a network error).  The
entries are shown exactly as before.

The package `pywk/` now has 16 modules, organised in layers:
downloading and cache (`api.py`), HTML parsing (`dom.py`), text and
colours (`text.py`), languages and sections (`entry.py`), rendering to
text or JSON (`render.py`), settings (`config.py`, `settings.py`), what
the three programs share (`common.py`), and one module for each
interface (`cli.py`, `tui.py`, `gui.py`, with `gui_theme.py` and
`gui_fonts.py`).  In total, around 5,200 lines of Python.

7. A new name
-------------

The program was first called *py-wkt*, and in 1.4 *py-wtk*, for
"Wiktionary toolkit".  The two names differed only in the order of two
letters, and the folder of my own clone kept the first one, so I mixed
them up myself: in the end there were a `~/.config/py-wkt` and a
`~/.config/py-wtk`, and it was not obvious which one the program used.
In 1.16 it became *py-wk*, which cannot be confused with either.

The new name reaches everything: the commands, the package `pywk/`, the
installer, the RPM, the settings and cache folders, the variable
`PY_WK_CONFIG`, the repositories on Codeberg and GitHub (renamed, so the
old addresses lead to the new ones) and the KRunner runner, now
*krunner-py-wk*.  Nobody should have to do anything by hand.  The
settings move by themselves, those of py-wtk before those of py-wkt; the
old variables are still read; the installer removes the menu entries and
icons it had added under the old names; and the RPM package declares
that it replaces py-wtk, so `dnf` changes one for the other.  Copr cannot
rename a project, so the RPM goes to a new one, `nivaca/py-wk`.  The
release notes and the changelog keep, for each version, the name it had.

8. A package for Debian and Ubuntu
----------------------------------

The RPM served Fedora, and the AppImage everyone else, but on Debian and
Ubuntu the natural thing is a `.deb`, so since 1.17 the releases have one
as well.  I build everything on Fedora, where there is no `dpkg-deb`, and
I did not want a tool more for one file.  A `.deb` is a simple thing: an
`ar` archive with a version line and two compressed tar files, one with
the control data and one with the files to install.  So
`packaging/build-deb.py` writes it with the standard library only
(`tarfile`, and a few lines for `ar`), from the same files that git knows
and that the RPM takes.  It installs the same as the RPM: the launchers
and `pywk/` in `/usr/share/py-wk`, links to them in `/usr/bin`, the menu
entries, the icons and the documents, plus the `copyright` file and the
compressed changelog that Debian expects.  The modules are compiled when
the package is installed, and the compiled files are removed with it.
All the files take the time of the commit, so one commit always gives
the same package.

Debian has no signature inside the package, as the RPM has, so the
`.deb` goes with a detached one (`.deb.asc`), made by the same key.
`tools/release.py` builds and attaches both to every release, unless it
is given `--no-deb`.

The one real problem is Python.  The package depends on `python3 (>=
3.15)`, the version py-wk needs, and today neither Debian (not even its
unstable branch, which has 3.14) nor Ubuntu has it, so `apt` refuses to
install it there.  I preferred an honest dependency to a package that
installs and then stops with a message; until those systems have Python
3.15, the AppImage is the way to use py-wk on them.

Testing
-------

The program was tested with Python 3.15, the oldest it supports, in
Linux.  `tools/screenshots.py` runs the three
programs as a user does (the window in light and dark mode), with
settings and a cache of their own, and the screenshots of the README
come from it; they were checked by eye, and in 1.6 they were taken
again.  The `.deb` was checked in a Debian container (unstable): `dpkg`
reads and installs it (forcing the Python dependency), the links in
`/usr/bin` lead to the launchers, the modules are compiled, the launcher
gives its message about the old Python, and the package is removed
without leaving anything; lintian finds only minor warnings (no manual
pages, for instance).  There are no automated tests yet.

For installation and full usage instructions, see the
[README](../README.md); the changes of each version are in
[NOTES.md](NOTES.md).
