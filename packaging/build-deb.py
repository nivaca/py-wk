#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Nicolas Vaughan <nicolasvaughan@proton.me>
# This file is part of py-wk. See the LICENSE file for details.
"""Hace el paquete .deb de py-wk (Debian, Ubuntu y derivados) a partir de
esta copia del repositorio, en build/deb/, y copia el más reciente a dist/,
junto al zip, el AppImage y el RPM.

    python3 packaging/build-deb.py [--sign[=CLAVE]]

El paquete instala lo mismo que el RPM (packaging/py-wk.spec): los tres
lanzadores y el paquete pywk en /usr/share/py-wk, enlaces a ellos en
/usr/bin (py-wk, py-wk-tui, py-wk-gui), las tres entradas del menú, los
íconos y la documentación.  No necesita dpkg: un .deb es un archivo ar con
dos tar (control y datos), y aquí se arman con la biblioteca estándar, así
que se puede hacer en Fedora.

Los archivos son los que git conoce, confirmados o no, como en
build-rpm.sh; el commit de HEAD va dentro como COMMIT.  --sign firma el
paquete con OpenPGP (una firma aparte, .deb.asc) con la clave del
proyecto, la misma del RPM (packaging/RPM-GPG-KEY-py-wk).
"""

import argparse
import gzip
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, DIR)
from pywk.version import MIN_PYTHON, NAME, VERSION  # noqa: E402

REVISION = "1"                  # la del paquete, no la del programa
MAINTAINER = "Nicolas Vaughan <nicolasvaughan@proton.me>"
PREFIX = f"/usr/share/{NAME}"
OUT = os.path.join(DIR, "build", "deb")
DIST = os.path.join(DIR, "dist")
PROGRAMS = ("py-wk", "py-wk-tui", "py-wk-gui")

HELP = ("Build the .deb package of py-wk (Debian, Ubuntu) into build/deb/, "
        "and copy it to dist/.")

CONTROL = f"""\
Package: {NAME}
Version: {{version}}
Architecture: all
Maintainer: {MAINTAINER}
Installed-Size: {{size}}
Depends: python3 (>= {'.'.join(map(str, MIN_PYTHON))}), python3-tk
Recommends: hicolor-icon-theme
Section: utils
Priority: optional
Homepage: https://github.com/nivaca/py-wk
Description: Look up words in the English Wiktionary
 py-wk looks up words in the English Wiktionary and shows their entries
 (definitions, etymology, pronunciation, inflection tables, quotations ...)
 for any language, with the sections and languages you choose.
 .
 It comes as three programs: a command line (py-wk), a full-screen
 terminal interface (py-wk-tui) and a window (py-wk-gui). Only the
 Python standard library is used; it needs a connection to the Internet.
"""

#  Los módulos se compilan al instalar (los usuarios no pueden escribir
#  junto a ellos, y Python los compilaría en cada arranque) y se borran
#  al desinstalar
POSTINST = f"""\
#!/bin/sh
set -e
if [ "$1" = configure ] && command -v python3 >/dev/null 2>&1; then
    python3 -m compileall -q {PREFIX}/pywk >/dev/null 2>&1 || true
fi
"""
PRERM = f"""\
#!/bin/sh
set -e
find {PREFIX} -name __pycache__ -type d -prune -exec rm -rf {{}} + 2>/dev/null || true
"""

COPYRIGHT = f"""\
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: {NAME}
Upstream-Contact: {MAINTAINER}
Source: https://github.com/nivaca/py-wk

Files: *
Copyright: 2026 Nicolas Vaughan <nicolasvaughan@proton.me>
License: GPL-3.0+

License: GPL-3.0+
 This program is free software: you can redistribute it and/or modify it
 under the terms of the GNU General Public License as published by the Free
 Software Foundation, either version 3 of the License, or (at your option)
 any later version.
 .
 On Debian systems, the complete text of the GNU General Public License
 version 3 can be found in "/usr/share/common-licenses/GPL-3".
"""

# The documentation in /usr/share/doc/py-wk (the %doc of the RPM)
DOCS = ("README.md", "README.es.md", "CHANGELOG.md", "CHANGELOG_es.md",
        "docs/NOTES.md", "docs/NOTES.es.md", "docs/DESCRIPTION.md",
        "docs/DESCRIPCIÓN_es.md", "docs/LICENSES.md", "docs/LICENCIAS_es.md")

#  Un miembro del tar: (bytes, modo) o, si es un enlace, (destino, None)
Member = tuple[bytes | str, int | None]


def die(message: str):
    sys.exit(f"build-deb: {message}")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", DIR, *args], check=True,
                          capture_output=True, text=True).stdout


def known_files() -> list[str]:
    """The files git knows about, committed or not, that exist."""
    #  -z: sin él, git cita los nombres con letras no ASCII
    #  ("docs/DESCRIPCI\303\223N_es.md") y no se encuentran
    out = git("ls-files", "-z", "--cached", "--others", "--exclude-standard")
    return [f for f in out.split("\0") if f and os.path.isfile(os.path.join(DIR, f))]


def contents(files: list[str], commit: str) -> dict[str, Member]:
    """{path in the package: member}: what the package installs."""
    out: dict[str, Member] = {}

    def add(path, data, mode=0o644):
        out[path] = (data, mode)

    def copy(src, path, mode=0o644):
        with open(os.path.join(DIR, src), "rb") as f:
            add(path, f.read(), mode)

    #  el programa: los lanzadores, el paquete pywk y los íconos (la ventana
    #  los lee); py-wk-install.py no, porque el paquete trae sus entradas
    share = f"usr/share/{NAME}"
    for f in files:
        if f in PROGRAMS:
            copy(f, f"{share}/{f}", 0o755)
        elif re.fullmatch(r"pywk/[^/]+\.py", f) or f == "icons/py-wk.svg" \
                or f.startswith("icons/linux/hicolor/"):
            copy(f, f"{share}/{f}")
    add(f"{share}/COMMIT", (commit + "\n").encode())
    # The launchers find pywk next to their real path, so /usr/bin has links.
    for p in PROGRAMS:
        if p not in files:
            die(f"{p} is missing")
        out[f"usr/bin/{p}"] = (f"../share/{NAME}/{p}", None)
    for f in files:
        if f.startswith("packaging/") and f.endswith(".desktop"):
            copy(f, f"usr/share/applications/{os.path.basename(f)}")
        elif f.startswith("icons/linux/hicolor/"):
            copy(f, "usr/share/icons/" + f[len("icons/linux/"):])
    #  la documentación, con el copyright y el changelog que pide Debian
    doc = f"usr/share/doc/{NAME}"
    for f in DOCS:
        if f not in files:
            die(f"{f} is missing")
        copy(f, f"{doc}/{os.path.basename(f)}")
    add(f"{doc}/copyright", COPYRIGHT.encode())
    add(f"{doc}/changelog.Debian.gz", gzip.compress(changelog().encode(), mtime=0))
    return out


def changelog() -> str:
    """A Debian changelog entry for this version (the changes are in
    CHANGELOG.md)."""
    date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(epoch()))
    return (f"{NAME} ({VERSION}-{REVISION}) unstable; urgency=medium\n\n"
            f"  * Version {VERSION}; see /usr/share/doc/{NAME}/CHANGELOG.md.\n\n"
            f" -- {MAINTAINER}  {date}\n")


def epoch() -> int:
    """The time of the files: that of the commit, so the same commit makes
    the same package ($SOURCE_DATE_EPOCH, if set, comes first)."""
    if os.environ.get("SOURCE_DATE_EPOCH"):
        return int(os.environ["SOURCE_DATE_EPOCH"])
    return int(git("log", "-1", "--format=%ct").strip())


def tar(members: dict[str, Member], mtime: int) -> bytes:
    """A tar.xz of MEMBERS, owned by root, with their folders."""
    folders = set()
    for path in members:
        parts = path.split("/")[:-1]
        for i in range(1, len(parts) + 1):
            folders.add("/".join(parts[:i]))
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:xz", format=tarfile.GNU_FORMAT) as t:
        def info(name, mode, kind=tarfile.REGTYPE, size=0):
            i = tarfile.TarInfo("./" + name if name else "./")
            i.type, i.mode, i.size, i.mtime = kind, mode, size, mtime
            i.uid = i.gid = 0
            i.uname = i.gname = "root"
            return i
        t.addfile(info("", 0o755, tarfile.DIRTYPE))
        for d in sorted(folders):
            t.addfile(info(d + "/", 0o755, tarfile.DIRTYPE))
        for path in sorted(members):
            data, mode = members[path]
            if mode is None:            # un enlace simbólico
                link = info(path, 0o777, tarfile.SYMTYPE)
                link.linkname = data
                t.addfile(link)
            else:
                t.addfile(info(path, mode, size=len(data)), io.BytesIO(data))
    return buffer.getvalue()


def ar(members: list[tuple[str, bytes]], mtime: int) -> bytes:
    """An ar archive (the format of a .deb) of MEMBERS."""
    out = [b"!<arch>\n"]
    for name, data in members:
        header = (f"{name:<16}{mtime:<12}{0:<6}{0:<6}{0o100644:<8o}"
                  f"{len(data):<10}`\n").encode()
        assert len(header) == 60
        out += [header, data, b"\n" if len(data) % 2 else b""]
    return b"".join(out)


def build(sign: str | None) -> str:
    files = known_files()
    if git("status", "--porcelain").strip():
        print("note: the tree has uncommitted changes; they go into this build.")
    commit = git("rev-parse", "HEAD").strip()
    mtime = epoch()
    data = contents(files, commit)
    version = f"{VERSION}-{REVISION}"
    regular = {p: d for p, (d, m) in data.items() if m is not None}
    size = sum((len(d) + 1023) // 1024 for d in regular.values())
    control = {
        "control": (CONTROL.format(version=version, size=size).encode(), 0o644),
        #  los enlaces no van en md5sums, como hace dh_md5sums
        "md5sums": ("".join(f"{hashlib.md5(d).hexdigest()}  {p}\n"
                            for p, d in sorted(regular.items())).encode(), 0o644),
        "postinst": (POSTINST.encode(), 0o755),
        "prerm": (PRERM.encode(), 0o755),
    }
    deb = ar([("debian-binary", b"2.0\n"),
              ("control.tar.xz", tar(control, mtime)),
              ("data.tar.xz", tar(data, mtime))], mtime)
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    path = os.path.join(OUT, f"{NAME}_{version}_all.deb")
    with open(path, "wb") as f:
        f.write(deb)
    print(f"Wrote {os.path.relpath(path, DIR)} ({len(deb) // 1024} KiB, "
          f"{len(data)} files)")
    made = [path]
    if sign:
        subprocess.run(["gpg", "--batch", "--yes", "--armor", "--local-user", sign,
                        "--detach-sign", path], check=True)
        made.append(path + ".asc")
        print(f"Signed: {os.path.relpath(path, DIR)}.asc")
    # The newest .deb also goes into dist/, replacing the older ones there.
    os.makedirs(DIST, exist_ok=True)
    for old in os.listdir(DIST):
        if old.startswith(f"{NAME}_") and old.endswith((".deb", ".deb.asc")):
            os.remove(os.path.join(DIST, old))
    for f in made:
        shutil.copy2(f, DIST)
    print("Copied to dist/: " + " ".join(os.path.basename(f) for f in made))
    return path


def signing_key() -> str:
    """The project's signing key, as packaging/build-rpm.sh pins it."""
    with open(os.path.join(DIR, "packaging", "build-rpm.sh"), encoding="utf-8") as f:
        m = re.search(r'SIGNING_KEY="\$\{SIGNING_KEY:-([0-9A-F]{40})\}"', f.read())
    if not m:
        die("no SIGNING_KEY in packaging/build-rpm.sh")
    return m.group(1)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="packaging/build-deb.py", description=HELP)
    parser.add_argument("--sign", nargs="?", const="", metavar="KEY",
                        help="also sign it (a detached OpenPGP signature, .deb.asc) "
                             "with the project's key, or KEY")
    args = parser.parse_args(argv)
    sign = args.sign
    if sign == "":
        sign = signing_key()
    build(sign)


if __name__ == "__main__":
    main()
