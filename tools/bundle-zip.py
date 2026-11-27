#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Nicolas Vaughan <nicolasvaughan@proton.me>
# This file is part of py-wk. See the LICENSE file for details.
"""Hace un zip del programa, para distribuirlo: python3 tools/bundle-zip.py

El zip es build/release/py-wk-v.VERSION.zip (la versión de
pywk/__init__.py; build/release se crea en la carpeta del programa si hace falta,
y --output da otra carpeta), con el programa en una carpeta del mismo nombre. Trae los tres
lanzadores, el paquete pywk, los iconos, los documentos y la licencia, pero
ningún archivo ni carpeta oculta (.git ...), nada de lo que se genera mientras el
programa corre o se edita (__pycache__, archivos .bak y .tmp ...) y nada de lo
que está en su carpeta sin ser parte de él (los paquetes de build/ y dist/,
tools/, con los scripts que los hacen y los publican, y tests/). Los lanzadores
conservan el permiso de ejecución. Trae también COMMIT, el commit del que salió
(para --version y "About").
"""

import os
import sys

#  (the program's folder, above tools/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pywk.version import check_python  # noqa: E402

check_python()          # (before the modules that need it)

import argparse  # noqa: E402
import fnmatch  # noqa: E402
import zipfile  # noqa: E402

from pywk.version import COMMIT_FILE, NAME, VERSION, commit  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # (above tools/)
#  Adónde va el zip, salvo que --output diga otra cosa (no a dist/, que solo
#  guarda el RPM)
DIST = os.path.join(HERE, "build", "release")

#  What is made while the program runs or is edited (as in .gitignore), and
#  earlier bundles
LEFT_OUT = ("__pycache__", "*.pyc", "*.bak", "*.tmp", "*.old", "*~",
            f"{NAME}-v*.zip", "*.AppImage", COMMIT_FILE)
#  What is in the program's folder but not part of it: the bundles, and
#  the tools that make them, publish releases and make the screenshots and
#  icons (not needed to run the program), their tests, and the RPM made
#  in build/
NOT_PART = ("dist", "tools", "tests", "build")


def name() -> str:
    """The name of the zip, without .zip: py-wk-v.1.0."""
    return f"{NAME}-v.{VERSION}"


def files() -> list[str]:
    """The files of the distribution, relative to the program's folder."""
    out = []
    for folder, dirs, names in os.walk(HERE):
        dirs[:] = sorted(d for d in dirs if not _left_out(d) and
                         (folder != HERE or d not in NOT_PART))
        for n in sorted(names):
            if not _left_out(n) and (folder != HERE or n not in NOT_PART):
                out.append(os.path.relpath(os.path.join(folder, n), HERE))
    return out


def _left_out(n: str) -> bool:
    return n.startswith(".") or any(fnmatch.fnmatch(n, p) for p in LEFT_OUT)


def built_from() -> str | None:
    """The commit the bundle is made from: that of GitHub Actions
    ($GITHUB_SHA), or else the program's."""
    return os.environ.get("GITHUB_SHA") or commit(HERE)


def bundle(folder: str) -> str:
    """Writes the zip into FOLDER; returns its path."""
    path = os.path.join(folder, name() + ".zip")
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files():
            #  (ZipFile.write keeps the file's permissions: the launchers
            #  can still be run after unzipping)
            z.write(os.path.join(HERE, f), name() + "/" + f.replace(os.sep, "/"))
        hash_ = built_from()
        if hash_:
            z.writestr(name() + "/" + COMMIT_FILE, hash_ + "\n")
    os.replace(tmp, path)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="tools/bundle-zip.py",
        description=f"Make a zip of the program, to distribute it: {name()}.zip, "
                    "without hidden files.")
    parser.add_argument("-o", "--output", metavar="FOLDER", default=None,
                        help="the folder to write it in (default: build/release, in the "
                             "program's folder)")
    parser.add_argument("-l", "--list", action="store_true",
                        help="only list the files it would have")
    args = parser.parse_args(argv)
    if args.list:
        print("\n".join(files()))
        return
    if args.output is None:
        args.output = DIST
        os.makedirs(DIST, exist_ok=True)
    elif not os.path.isdir(args.output):
        sys.exit(f"bundle-zip.py: there is no folder {args.output}")
    try:
        path = bundle(args.output)
    except OSError as e:
        sys.exit(f"bundle-zip.py: {e}")
    with zipfile.ZipFile(path) as z:
        count = len(z.namelist())
    print(f"Wrote {path} ({count} files, {os.path.getsize(path) / 1e6:.1f} MB).")


if __name__ == "__main__":
    main()
