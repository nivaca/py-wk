# Registro de cambios

Los cambios notables de py-wk (llamado py-wtk hasta la 1.15, y py-wkt
antes de la 1.4). Las versiones publicadas, con el zip, la AppImage, el RPM
firmado y (desde la 1.17) el `.deb` firmado, están en [Codeberg](https://codeberg.org/nivaca/py-wk/releases) y
[GitHub](https://github.com/nivaca/py-wk/releases); el RPM
está también en [Copr](https://copr.fedorainfracloud.org/coprs/nivaca/py-wk/)
(hasta la 1.15, en [nivaca/py-wtk](https://copr.fedorainfracloud.org/coprs/nivaca/py-wtk/)).
Cada entrada conserva el nombre que tenía su versión.
La historia de git empieza con la 1.4: las versiones 1.0 a 1.3 se toman de
las notas de versión de `docs/NOTES.md`, que no dan fechas.

## Sin publicar

- `tools/zenodo.py`: la descripción del depósito es ahora el README entero
  de la etiqueta, en HTML. El borrador recibe además el colaborador (el
  director del proyecto), los idiomas, el copyright, el repositorio en
  GitHub, el lenguaje de programación y el estado del desarrollo; estos
  últimos, por la API de registros de Zenodo, porque la de depósitos no los
  admite. El token puede guardarse en el llavero del escritorio
  (`secret-tool store --label="Zenodo token" service zenodo`) en vez de en
  `$ZENODO_TOKEN`; `tools/zenodo.py check-token` dice si hay uno.

- `tools/zenodo.py` prepara el depósito de una versión en Zenodo. `collect`
  deja en `dist/zenodo/` el árbol de la etiqueta como
  `py-wk-VERSIÓN-source.tar.gz`, con su firma, un `SHA256SUMS` del depósito,
  firmado, y la clave pública, y comprueba cada firma con solo esa clave
  (`--packages` añade los archivos de la versión). `upload` lo sube a Zenodo
  como borrador, versión nueva del depósito si ya lo hay, y nunca lo
  publica. `tools/release.py` reúne ahora el depósito después de la etiqueta
  y lo sube como borrador, salvo con `--no-zenodo`. Los metadatos están en
  `.zenodo.json`.

## 1.18 — 2026-11-22

- **Cada versión firmada**: además del RPM, cada archivo publicado (el
  zip, la AppImage, el `.deb`) va con su firma (`.asc`), con
  `SHA256SUMS` y su firma, y con la clave pública (`RPM-GPG-KEY-py-wk`);
  la etiqueta de la versión también va firmada. Cada firma se comprueba
  con la clave publicada antes de publicar nada. El README explica cómo
  comprobar una descarga.
- `tools/release.py` hace ahora siempre el RPM firmado (`--no-rpm` lo
  omite; `--rpm` se sigue aceptando, y no hace nada).

## 1.17 — 2026-11-21

- Un paquete `.deb` para Debian, Ubuntu y sus derivadas
  (`py-wk_1.17-1_all.deb`), con una firma aparte (`.deb.asc`) de la clave
  del RPM; instala los mismos archivos que el RPM y necesita que el
  `python3` del sistema sea 3.15 o posterior.
- Lo genera `packaging/build-deb.py`, solo con la biblioteca estándar de
  Python; `tools/release.py` lo adjunta a las versiones (`--no-deb` lo
  omite).

## 1.16 — 2026-11-21

- **Nuevo nombre, py-wk** (era py-wtk): los comandos `py-wk`, `py-wk-tui`
  y `py-wk-gui`, el instalador `py-wk-install.py`, el paquete RPM, la
  carpeta de ajustes `~/.config/py-wk`, la caché `~/.cache/py-wk`, la
  variable `PY_WK_CONFIG` y los repositorios `nivaca/py-wk`.
- Los ajustes de `~/.config/py-wtk` pasan una vez a la carpeta nueva
  (antes que los de `~/.config/py-wkt`); `PY_WTK_CONFIG` se sigue leyendo.
- `py-wk-install.py` quita los accesos del menú y los iconos que había
  añadido como py-wtk o py-wkt.
- El RPM está en Copr como `nivaca/py-wk`; el paquete reemplaza a py-wtk.

## 1.15 — 2026-11-21

- `docs/LICENCIAS_es.md` y `docs/LICENSES.md` enumeran el software libre
  que py-wtk usa o lleva en la AppImage, con sus licencias, y las
  herramientas con que se hace py-wtk; los README remiten a ellas, y el
  RPM las incluye entre sus documentos.
- Este registro de cambios, en español y en inglés.

## 1.14 — 2026-11-20

- **El texto sigue el escalado de una pantalla de alta resolución.** En
  una pantalla escalada al 200 %, el texto de la ventana podía salir a la
  mitad de su tamaño: Tk 9, que usa el RPM, deja el tamaño de las letras
  en manos de fontconfig, y una regla de la configuración de fontconfig
  del usuario que fijara los DPI (en 96, por ejemplo) se imponía sobre el
  escalado del escritorio. Ahora la ventana le da a fontconfig los DPI del
  escritorio, después de las reglas propias del usuario.
- El tamaño de la ventana se guarda en píxeles a 96 DPI y se escala al
  abrirla, como el ancho del panel de contenidos, así que un tamaño
  guardado al 100 % no queda demasiado pequeño al 200 %.
- La dirección de contacto en los archivos y en el paquete es
  nicolasvaughan@proton.me.
- `packaging/build-rpm.sh` copia también el RPM más reciente en `dist/`,
  en lugar de los anteriores que hubiera allí.

## 1.13 — 2026-11-14

- Se necesita Python 3.15 o posterior (antes, 3.13). La AppImage lleva su
  propio Python 3.15. El RPM se construye para Fedora 45 y posteriores;
  Fedora 44, cuyo Python es el 3.14, ya no se construye en Copr.

## 1.12 — 2026-11-14

- Se necesita Python 3.13 o posterior (antes, 3.11): en la comprobación
  de `version.py`, en el RPM y en los documentos.

## 1.11 — 2026-11-14

- Ya no hay Flatpak: se quitaron `packaging/flatpak/` y
  `tools/bundle-flatpak.py`, y las versiones publicadas vuelven a traer
  solo el zip, la AppImage y el RPM. El Flatpak se retiró también de la
  versión 1.10.
- Los README, las descripciones y los comentarios del código se leen con
  más llaneza, en inglés y en español; el programa es el mismo.

## 1.10 — 2026-11-13

- **Copiar y pegar.** La ventana tiene un menú Edit con Cut, Copy y Paste
  (Ctrl+X, Ctrl+C, Ctrl+V) para la casilla de búsqueda, las lenguas y la
  casilla de buscar en la entrada, y Copy para el texto seleccionado en la
  entrada. En la interfaz de terminal, `y` (o F7) copia la entrada entera
  como texto plano, mediante el programa de portapapeles del sistema o, si
  no lo hay, mediante la propia terminal (OSC 52).
- Un Flatpak, adjunto a la versión publicada (retirado de nuevo en la
  1.11).
- Las filas del panel de contenidos son tan altas como su texto, así que
  ya no se solapan con un texto más grande (Ctrl++) ni en una pantalla
  escalada.

## 1.9 — 2026-11-13

- La interfaz de terminal arranca en la AppImage. Su Python no podía leer
  cómo se describen a sí mismas la mayoría de las terminales (las de 256
  colores), y `py-wtk-tui` se detenía con "setupterm: could not find
  terminal". La AppImage lleva ahora esas descripciones en una forma que
  puede leer.

## 1.8 — 2026-11-12

- **Un icono nuevo**: la `pW` entre corchetes, dibujada con formas en
  lugar de con una fuente, en blanco y crema sobre un cuadro verde
  azulado, con una marca de acento ámbar. Ejecute de nuevo
  `py-wtk-install.py` para tenerlo en el menú de aplicaciones.
- **Una nueva clave para firmar el RPM**: `8187 0643 CA22 1AF9 0C30 554E
  BE68 32CD 3599 4948` (ed25519, hasta 2029), fijada en `build-rpm.sh`,
  con su clave pública en `packaging/RPM-GPG-KEY-py-wtk` y en cada versión
  publicada. Un RPM anterior descargado de una versión publicada necesita
  `sudo rpm --import RPM-GPG-KEY-py-wtk` una vez; el paquete de Copr no se
  ve afectado.

## 1.7 — 2026-11-11

- **La ventana sigue el escalado del escritorio en pantallas de alta
  resolución.** La ventana de la AppImage salía muy pequeña con el
  escritorio escalado (al 200 % en Plasma, por ejemplo), porque su Tk no
  tenía en cuenta `Xft.dpi`. Ahora lo lee, y el texto y la ventana crecen
  con él.
- **Un paquete para Fedora**: un RPM que usa el Python y el Tk del
  sistema y añade los tres programas al `PATH` y al menú de aplicaciones.
  Está en Copr (`sudo dnf copr enable nivaca/py-wtk && sudo dnf install
  py-wtk`), y las versiones publicadas también lo traen, firmado.
  `tools/release.py --rpm` lo adjunta.

## 1.6 — 2026-11-06

- `py-wtk-install.py --uninstall` quita del menú de aplicaciones solo los
  archivos `.desktop` y los iconos que hizo el instalador; una entrada con
  el mismo nombre que él no escribió se deja en paz, y los enlaces
  también. `--only-gui` sigue la misma regla.
- Con un paginador distinto de `less` (por ejemplo `PAGER=most`), los
  enlaces de una entrada larga aparecían como caracteres sueltos, como
  `^[]8;;`. Con cualquier otro paginador la entrada se muestra ahora sin
  enlaces, con sus colores.
- Capturas de pantalla nuevas, y los documentos de descripción
  `DESCRIPTION.md` y `DESCRIPCIÓN_es.md`, con la estructura de py-words.

## 1.5 — 2026-11-05

- Un enlace a otra entrada la abre por arriba, con todas las lenguas del
  filtro, en la ventana y en la interfaz de terminal. Antes saltaba a la
  lengua del enlace (`rosa#Latin` bajaba hasta el latín), y parecía que
  la lengua hubiera cambiado. Un enlace a otra parte de la misma entrada
  sigue llevando allí.

## 1.4 — 2026-11-05

- `py-wtk --set NAME=VALUE` y `py-wtk --unset NAME` fallaban con un error
  en lugar de cambiar el ajuste. Vuelven a funcionar, y un nombre
  equivocado o ambiguo (`--set links=false` coincide con `cli.links` y con
  `gui.links`) se señala con claridad.
- Los tres programas muestran los mismos mensajes: el tamaño de la caché
  en disco ("2 pages, 192.7 KB"), una lengua que la página no tiene. En la
  ventana, "Open in browser" y "Clear disk cache" dicen en la línea de
  estado lo que hicieron; en la línea de comandos, un error de red al
  buscar (`-s`) da un mensaje claro.
- `py-wtk-install.py --only-gui` añade al menú de aplicaciones solo la
  ventana, y quita las entradas de los otros dos si una ejecución anterior
  las añadió.
- El código que cada programa tenía por su cuenta (historial, enlaces,
  mensajes, caché en disco, opciones comunes) está ahora en
  `pywtk/common.py`.
- Los scripts que arman los paquetes están en `tools/`
  (`bundle-zip.py`, `bundle-appimage.py`), y `tools/icons.py` vuelve a
  hacer todos los iconos a partir de `icons/py-wtk.svg`.

## 1.3

- El icono tiene fondo blanco, y las letras están mejor centradas. Los
  iconos de todos los tamaños se hacen de nuevo a partir de él, y las
  capturas de pantalla del README están al día.

## 1.2

- **Enlaces en los que se puede hacer clic** en los tres programas. Un
  enlace a otra entrada la abre en el programa; los demás enlaces
  (Wikipedia, los apéndices del Wiktionary, otros diccionarios) se abren
  en el navegador. En la ventana se subrayan bajo el ratón (ajuste
  `gui.links`); en la interfaz de terminal un clic los abre y `L` los
  lista; en la línea de comandos son hipervínculos OSC 8 (ajuste
  `cli.links`).
- **Línea de comandos interactiva**: `py-wtk -i` pide una palabra tras
  otra; Ctrl-D o Ctrl-C la terminan.
- `py-wtk-install.py` añade también `py-wtk (CLI)` al menú de
  aplicaciones, que abre `py-wtk -i` en una terminal; las entradas están
  solo en las categorías Office y Dictionary.
- `py-wtk-tui` iniciado sin terminal lo dice, en lugar de fallar con un
  error de curses.

## 1.0

- Primera versión del nuevo py-wtk, un programa para leer el Wiktionary en
  inglés sin navegador: la entrada entera (etimología, pronunciación,
  definiciones, tablas de flexión, traducciones y lo demás), para todas
  las lenguas de la página o solo para las elegidas. Viene como línea de
  comandos (`py-wtk`), interfaz de terminal (`py-wtk-tui`) y ventana
  (`py-wtk-gui`), con ajustes compartidos entre ellos, una caché en disco,
  un zip y una AppImage, y `py-wtk-install.py` para añadir los programas
  al menú de aplicaciones.
