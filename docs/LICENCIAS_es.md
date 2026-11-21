Software libre en py-wk
========================

py-wk es software libre, bajo la Licencia Pública General de GNU, versión
3 o posterior (el archivo `LICENSE`). Su código solo usa la biblioteca
estándar de Python, así que el software que lo acompaña depende de cómo se
instale: el zip y el RPM no traen más que el programa, y el AppImage trae
un Python completo. Esta lista da cada pieza de software, para qué se usa
y su licencia (con su identificador SPDX).

El texto de las entradas no es software: procede del Wiktionary en inglés
y de sus autores, bajo la licencia CC BY-SA 4.0
(<https://creativecommons.org/licenses/by-sa/4.0/deed.es>). py-wk solo lo
muestra.


Lo que usa el programa
----------------------

Lo necesita cualquier forma de py-wk. Con el zip es el del usuario; con
el RPM, el de Fedora; con el AppImage, el que va dentro.

| Software | Para qué | Licencia |
|---|---|---|
| Python 3.15, con su biblioteca estándar | todo el programa | Python Software Foundation License (`Python-2.0.1`) |
| Tcl/Tk (Tk 8.6 en el AppImage, Tk 9 en Fedora) | la ventana, mediante `tkinter` | licencia de Tcl/Tk (`TCL`) |
| ncurses | la interfaz de terminal, mediante `curses` | licencia X11 (`MIT-open-group`) |


El AppImage
-----------

El AppImage lleva su propio Python: una compilación reubicable de Python
3.15 hecha por el proyecto python-appimage
(<https://github.com/niess/python-appimage>, cuyos guiones de compilación
están bajo `GPL-3.0`). Además de Python, esa compilación trae estas
bibliotecas, que van en el AppImage tal como vienen:

| Biblioteca | Versión | La usa | Licencia |
|---|---|---|---|
| Tcl y Tk | 8.6.18 | `tkinter` (la ventana) | `TCL` |
| Xft, Xrender | | Tk, para dibujar el texto | `HPND-sell-variant` |
| ncurses (`ncursesw`, `panelw`, `tinfo`) | 5 | `curses` (la interfaz de terminal) | `MIT-open-group` |
| OpenSSL | 3 | `ssl` (HTTPS con el Wiktionary) | `Apache-2.0` |
| GNU Readline | 6.2 | `readline` (edición de la línea en `py-wk -i`) | `GPL-3.0-or-later` |
| GNU dbm | 1.10 | `dbm` (py-wk no lo usa) | `GPL-3.0-or-later` |
| SQLite | 3.54.1 | `sqlite3` (py-wk no lo usa) | dominio público (`blessing`) |
| bzip2 | 1.0.6 | `bz2` (py-wk no lo usa) | `bzip2-1.0.6` |
| XZ Utils (liblzma) | 5.2.2 | `lzma` (py-wk no lo usa) | dominio público |
| Zstandard | 1.5.7 | `compression.zstd` (py-wk no lo usa) | `BSD-3-Clause OR GPL-2.0-only` |
| libffi | | `ctypes` (para leer los recursos de X) | `MIT` |
| mpdecimal | 4.0.1 | `decimal` (py-wk no lo usa) | `BSD-2-Clause` |

La misma compilación trae unos paquetes de Python, de los que py-wk solo
usa certifi:

| Paquete | Para qué | Licencia |
|---|---|---|
| certifi | los certificados para HTTPS (el AppImage apunta `SSL_CERT_FILE` a ellos) | `MPL-2.0` |
| pip, build, pyproject_hooks | nada (vienen con el Python) | `MIT` |
| packaging | nada (viene con el Python) | `Apache-2.0 OR BSD-2-Clause` |

Y en el AppImage van dos cosas más:

| Software | Para qué | Licencia |
|---|---|---|
| Las descripciones de terminales de ncurses (terminfo) | que la interfaz de terminal arranque en cualquier sistema; se hacen con `infocmp` y `tic`, del ncurses de quien lo construye | `MIT-open-group` |
| El runtime de AppImage (type2-runtime) | arrancar el AppImage; lo pone appimagetool | `MIT` |


El RPM
------

El RPM solo trae el programa. Funciona con el Python y el Tk de Fedora,
que instala como dependencias:

| Paquete de Fedora | Licencia (como la da Fedora) |
|---|---|
| `python3`, `python3-tkinter` | `Python-2.0.1` (`python3-libs` añade partes bajo `MIT`, `BSD-3-Clause`, `Apache-2.0` y otras licencias permisivas) |
| `tk`, `tcl` | `TCL` (con partes pequeñas bajo otras licencias) |
| `ncurses-libs` | `MIT-open-group` |
| `hicolor-icon-theme` | `GPL-2.0-or-later` |


Herramientas para hacerlo
-------------------------

Sirven para construir, probar y publicar py-wk. Ninguna va en lo que se
distribuye.

| Herramienta | Para qué | Licencia |
|---|---|---|
| Git | la historia del código | `GPL-2.0-only` |
| appimagetool | hacer el AppImage | `MIT` |
| RPM (`rpmbuild`, `rpmsign`), rpmdevtools | construir y firmar el RPM | `GPL-2.0-or-later` |
| desktop-file-utils | revisar las entradas de menú del RPM | `GPL-2.0-or-later` |
| GnuPG | firmar el RPM | `GPL-3.0-or-later` (con partes bajo otras licencias) |
| copr-cli | enviar el RPM a Copr | `GPL-2.0-or-later` |
| GitHub CLI (`gh`) | publicar las versiones en GitHub | `MIT` |
| tea | publicar las versiones en Codeberg | `MIT` |
| Inkscape | dibujar los iconos a partir del SVG (`tools/icons.py`) | `GPL-2.0-or-later` |
| Pillow | hacer los iconos `.ico` e `.icns` | `MIT-CMU` |
| Xvfb (X.Org) | una pantalla oculta para las capturas | `MIT` |
| ImageMagick | tomar las capturas de la ventana | `ImageMagick` |
| tmux | una terminal oculta para las capturas de los programas de terminal | `ISC` |
| Chromium | convertir esas terminales en imágenes (se puede usar Google Chrome, pero no es software libre) | `BSD-3-Clause` |
