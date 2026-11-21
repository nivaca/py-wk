# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Nicolas Vaughan <nicolasvaughan@proton.me>
# This file is part of py-wk. See the LICENSE file for details.
#
# Build with packaging/build-rpm.sh, which makes the source tarball.

Name:           py-wk
Version:        1.16
Release:        1%{?dist}
Summary:        Look up words in the English Wiktionary

License:        GPL-3.0-or-later
URL:            https://github.com/nivaca/py-wk
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  desktop-file-utils
# For %check, which loads the window's module.
BuildRequires:  python3-tkinter

Requires:       python3 >= 3.15
# The window (py-wk-gui) is Tk.
Requires:       python3-tkinter
Requires:       hicolor-icon-theme

# El paquete se llamaba py-wtk hasta la 1.15: este lo reemplaza al actualizar.
Obsoletes:      py-wtk < 1.16
Provides:       py-wtk = %{version}-%{release}

%description
py-wk looks up words in the English Wiktionary and shows their entries
(definitions, etymology, pronunciation, inflection tables, quotations ...)
for any language, with the sections and languages you choose.

It comes as three programs: a command line (py-wk), a full-screen
terminal interface (py-wk-tui) and a window (py-wk-gui). Only the
Python standard library is used; it needs a connection to the Internet.

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to build: the program is Python.

%install
# The program: the three launchers and the pywk package, with the icons
# (the window reads them), not the tools, docs or py-wk-install.py (the
# package has its own menu entries). The launchers find pywk next to
# their real path, so /usr/bin has links to them.
install -d %{buildroot}%{_datadir}/%{name}
for f in py-wk py-wk-tui py-wk-gui; do
    install -pm 0755 "$f" %{buildroot}%{_datadir}/%{name}/
done
install -d %{buildroot}%{_datadir}/%{name}/pywk
install -pm 0644 pywk/*.py %{buildroot}%{_datadir}/%{name}/pywk/
[ -f COMMIT ] && install -pm 0644 COMMIT %{buildroot}%{_datadir}/%{name}/
install -d %{buildroot}%{_datadir}/%{name}/icons/linux
install -pm 0644 icons/py-wk.svg %{buildroot}%{_datadir}/%{name}/icons/
cp -pr icons/linux/hicolor %{buildroot}%{_datadir}/%{name}/icons/linux/
# Compiled now: users cannot write next to the modules, so Python would
# otherwise compile every module on every start.
%py_byte_compile %{python3} %{buildroot}%{_datadir}/%{name}/pywk

install -d %{buildroot}%{_bindir}
for f in py-wk py-wk-tui py-wk-gui; do
    ln -s ../share/%{name}/"$f" %{buildroot}%{_bindir}/"$f"
done

for f in packaging/*.desktop; do
    desktop-file-install --dir=%{buildroot}%{_datadir}/applications "$f"
done
install -d %{buildroot}%{_datadir}/icons
cp -pr icons/linux/hicolor %{buildroot}%{_datadir}/icons/

%check
for f in %{buildroot}%{_datadir}/applications/*.desktop; do
    desktop-file-validate "$f"
done
# The installed programs start, from their links, with no settings or
# cache of the builder's (and no network: nothing is looked up).
export HOME="$PWD/check-home" XDG_CONFIG_HOME= XDG_CACHE_HOME=
%{buildroot}%{_bindir}/py-wk --version | grep -q '%{version}'
%{buildroot}%{_bindir}/py-wk-tui --help | grep -q '%{version}'
%{buildroot}%{_bindir}/py-wk-gui --help >/dev/null
PYTHONPATH=%{buildroot}%{_datadir}/%{name} %{python3} -c \
    'import pywk.cli, pywk.tui, pywk.gui, pywk.render, pywk.settings'

%files
%license LICENSE
%doc README.md README.es.md docs/NOTES.md docs/NOTES.es.md
%doc docs/DESCRIPTION.md docs/DESCRIPCIÓN_es.md
%doc docs/LICENSES.md docs/LICENCIAS_es.md CHANGELOG.md CHANGELOG_es.md
%{_bindir}/py-wk
%{_bindir}/py-wk-tui
%{_bindir}/py-wk-gui
%{_datadir}/%{name}/
%{_datadir}/applications/py-wk.desktop
%{_datadir}/applications/py-wk.cli.desktop
%{_datadir}/applications/py-wk.tui.desktop
%{_datadir}/icons/hicolor/*/apps/py-wk.*

%changelog
* Sat Nov 21 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.16-1
- Renamed py-wk (it was py-wtk): commands, package, settings folder and
  repositories; the package replaces py-wtk

* Sat Nov 21 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.15-1
- A list of the open-source software used, with its licences (docs/LICENSES.md),
  and a changelog

* Fri Nov 20 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.14-1
- The window's text follows the scaling of a hi-res display even when fontconfig
  fixes a DPI

* Sat Nov 14 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.13-1
- Python 3.15 or later is needed; no longer built for Fedora 44

* Sat Nov 14 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.12-1
- Python 3.13 or later is needed

* Sat Nov 14 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.11-1
- No Flatpak any more; plainer documentation and comments

* Fri Nov 13 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.10-1
- Copying and pasting: an Edit menu in the window, y in the terminal interface

* Fri Nov 13 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.9-1
- The AppImage carries terminal descriptions in the old format, so py-wtk-tui
  starts in it

* Thu Nov 12 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.8-1
- A new icon

* Wed Nov 11 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.7-1
- The window follows the desktop's scaling (Xft.dpi) on hi-res displays

* Wed Nov 11 2026 Nicolas Vaughan <nicolasvaughan@proton.me> - 1.6-1
- First package: runs on the system's Python and Tk; the commands
  py-wtk, py-wtk-tui and py-wtk-gui, with three menu entries
