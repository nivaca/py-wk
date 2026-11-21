# py-wk 1.17: descripción

*[Read in English](DESCRIPTION.md)*

## Análisis

py-wk es un programa pequeño para consultar el Wiktionary en inglés (https://en.wiktionary.org) sin abrir el navegador. Se le da una palabra o una expresión de cualquier lengua y muestra la entrada completa del Wiktionary, con un formato limpio, en la terminal o en una ventana de escritorio. Se llamó primero *py-wkt* y, de la 1.4 a la 1.15, *py-wtk*; los dos nombres solo diferían en el orden de dos letras y se confundían con facilidad (había a la vez una carpeta `~/.config/py-wkt` y otra `~/.config/py-wtk`), de modo que en la 1.16 pasó a llamarse *py-wk*. py-wk es software libre, bajo la Licencia Pública General de GNU, versión 3 o posterior. El contenido de las entradas procede del Wiktionary y de sus colaboradores, bajo la licencia CC BY-SA 4.0; py-wk solo lo muestra, y no es un proyecto oficial del Wiktionary ni de la Fundación Wikimedia. Usa Python y su biblioteca estándar (bajo la licencia de la Python Software Foundation), con Tcl/Tk y ncurses (bajo licencias permisivas); el AppImage lleva además las bibliotecas de su propio Python. `docs/LICENCIAS_es.md` las enumera todas, con las herramientas con que se hace py-wk y sus licencias.

Está pensado para quienes consultan palabras a menudo: estudiantes y profesores de lenguas (latín, griego, español, inglés…), traductores, filólogos y, en general, cualquiera que quiera la información del Wiktionary sin el desorden ni la lentitud de la página web. De ahí salieron los requisitos. Lo primero era mostrar la entrada entera, no solo las definiciones: etimología, pronunciación, definiciones con ejemplos y citas fechadas, notas de uso, tablas de flexión (declinaciones y conjugaciones, bien alineadas), sinónimos, términos derivados y relacionados, descendientes, traducciones, referencias y lecturas adicionales. Lo segundo, poder quedarse solo con lo que interesa: unas lenguas, unas secciones o una vista breve con solo las definiciones.

También tenía que servirle a cualquiera: desde la línea de comandos, para una consulta rápida o para otros programas; a pantalla completa en la terminal, para leer entradas largas, y en una ventana, para el uso diario con el ratón. Las tres formas debían mostrar lo mismo y compartir los ajustes, recordar la configuración de una sesión a otra y no depender de paquetes externos. Por último, el programa tenía que ser respetuoso con los servidores del Wiktionary: no volver a descargar una página que acaba de consultar y esperar cuando el Wiktionary pide que se esperen.

## Diseño

El programa está dividido en capas, cada una con un solo trabajo. `api.py` descarga las páginas, busca títulos y guarda la caché; `dom.py` lee el HTML en un árbol pequeño; `text.py` limpia el texto, mide el ancho de cada carácter en la terminal y pone los colores; `entry.py` reparte la página en lenguas y secciones y aplica los filtros y las opciones.

`render.py` convierte una entrada en texto o en JSON, y es el mismo para los tres programas, de modo que una entrada se ve igual, y contiene lo mismo, en todos ellos. `common.py` reúne lo demás que comparten: las opciones comunes, los mensajes, el historial de atrás y adelante, los enlaces y la caché en disco. La configuración vive en `settings.py`, que dice en un solo lugar qué es cada ajuste, su tipo y su valor por omisión, y en `config.py`, que lee y escribe el archivo.

Sobre esa base hay tres interfaces: la línea de comandos (`cli.py`, que se abre con `py-wk`), la pantalla completa en la terminal (`tui.py`, con `py-wk-tui`) y la ventana (`gui.py`, con `py-wk-gui`), con su aspecto claro y oscuro (`gui_theme.py`) y sus fuentes (`gui_fonts.py`). `version.py` da el nombre, la versión, el commit del que se hizo el programa y el Python que necesita. Completan el conjunto tres lanzadores pequeños, un instalador de accesos en el menú del sistema (`py-wk-install.py`) y los iconos.

No hay datos propios: las páginas se descargan en HTML desde la API REST del Wiktionary (`/api/rest_v1/page/html/…`). Las páginas descargadas se guardan comprimidas en la carpeta de caché habitual de cada sistema durante un día (ajuste `general.cache_days`), de modo que volver a consultar una palabra es instantáneo. La configuración del usuario queda en un archivo TOML legible, `config.toml`, en la carpeta de configuración habitual de cada sistema.

## Implementación

Está escrito en Python 3.15 o superior y usa solo la biblioteca estándar, sin paquetes externos: `urllib`, `html.parser`, `textwrap`, `curses`, `tkinter` y `tomllib`. El paquete `pywk/` tiene 16 módulos, unas 5200 líneas.

La línea de comandos usa `argparse`. Escribe la entrada con colores, la pasa a un paginador cuando es larga y tiene un modo interactivo (`-i`) que pide una palabra tras otra; con `--json` da la entrada en JSON estructurado. La pantalla completa para la terminal usa `curses`, y la ventana, Tkinter. Las dos tienen un índice por lenguas y secciones, búsqueda dentro de la página, historial con atrás y adelante, recarga y una pantalla o ventana de ajustes con todas las opciones. En la ventana, además, se sugieren palabras mientras se escribe y un doble clic en cualquier palabra la busca. Si una palabra no existe, se proponen otras parecidas.

Los tres programas comparten el archivo `config.toml`, que se puede modificar desde la línea de comandos (`--set`, `--unset`), desde los ajustes de la terminal o de la ventana, o a mano. Cada programa escribe solo los ajustes que se cambian, sobre el archivo tal como está en ese momento, así que si la ventana y la terminal están abiertas a la vez, una no deshace los cambios de la otra. Los ajustes de las versiones llamadas *py-wtk* y *py-wkt* pasan una sola vez a la nueva carpeta (primero los de py-wtk), y el archivo viejo se renombra `*.old`; las variables `PY_WTK_CONFIG` y `PY_WKT_CONFIG` se siguen leyendo. El instalador quita también los accesos e iconos que había puesto con los nombres viejos, y el paquete RPM declara que reemplaza a py-wtk, de modo que `dnf` cambia uno por otro.

Cuando el Wiktionary responde «Too Many Requests» o está ocupado un momento, el programa espera (lo que diga la respuesta, si lo dice) y vuelve a intentarlo por sí solo. Las entradas grandes cuyas traducciones están en una página aparte (como *house/translations*) descargan también esa página, y las traducciones se colocan en su sitio.

### Enlaces

Desde la versión 1.2, los enlaces de una entrada funcionan en los tres programas. Un enlace a otra entrada la abre en el programa, arriba y con todas las lenguas del filtro; los demás (Wikipedia, los apéndices del Wiktionary, otros diccionarios) se abren en el navegador. En la terminal un clic los abre y la tecla `L` los lista. En la línea de comandos son hipervínculos de la terminal (OSC 8), que solo se escriben con colores, así que `--json`, `--no-color` y la salida hacia otros programas no cambian. Como solo `less` sabe mostrarlos, con cualquier otro paginador la entrada se muestra sin ellos, con sus colores.

### Distribución

El programa se distribuye como un zip (o un clon del repositorio) para cualquier sistema con Python 3.15 o posterior, con tres lanzadores que se enlazan en el `PATH`; como un AppImage para Linux, que lleva su propio Python, y, desde la 1.7, como un paquete RPM para Fedora, en Copr y, firmado, con cada versión publicada, que usa el Python y el Tk del sistema, y, desde la 1.17, como un `.deb` para Debian y Ubuntu, que instala lo mismo. El zip y el AppImage llevan el commit del que se hicieron, que muestran `--version` y *About*.

Los guiones de `tools/` generan el zip y el AppImage, publican las versiones, toman las capturas del README y regeneran los iconos a partir de un único SVG. `tools/release.py` publica cada versión en GitHub y en Codeberg, con el zip, el AppImage y el `.deb` y el RPM firmados (que genera `packaging/`); el RPM va también a Copr.

### El paquete .deb

En Fedora, donde se hace todo, no hay `dpkg-deb`. Como un `.deb` no es más que un archivo `ar` con una línea de versión y dos tar comprimidos, `packaging/build-deb.py` lo escribe con la biblioteca estándar, con los archivos que conoce git, el `copyright` y el registro de cambios que pide Debian; compila los módulos al instalar y los borra al desinstalar. La firma va aparte (`.deb.asc`), con la clave del RPM.

## Validación

El programa se probó con Python 3.15, la versión mínima, en Linux. `tools/screenshots.py` maneja los tres programas como lo haría un usuario (la ventana en modo claro y oscuro), con ajustes y caché propios, para no tocar los del usuario; de ahí salen las capturas del README, que se revisaron a ojo y se volvieron a tomar en la 1.6. Con un Python demasiado viejo, el programa da un mensaje claro en lugar de un error. El `.deb` se comprobó en un contenedor de Debian inestable: `dpkg` lo lee y lo instala (forzando la dependencia de Python), los enlaces de `/usr/bin` llevan a los lanzadores, los módulos quedan compilados, el lanzador da su mensaje sobre el Python viejo y el paquete se quita sin dejar nada; lintian solo da avisos menores, como la falta de páginas de manual. Todavía no tiene pruebas automáticas.

## Plataforma

Funciona en Linux, Windows y macOS, y usa las carpetas habituales de ajustes y de caché de cada sistema. Necesita Python 3.15 o superior; para la ventana hace falta Tkinter, que viene en los instaladores de python.org y que en algunas distribuciones de Linux es un paquete aparte, como `python3-tkinter` o `python3-tk`. El AppImage para Linux no necesita nada más. El RPM es para Fedora 45 o posterior; el `.deb`, para un Debian o un Ubuntu cuyo `python3` sea 3.15 o posterior.

En pantallas de alta resolución, la ventana sigue la escala del escritorio (`Xft.dpi`); desde la 1.7, también con el Tk 8.6 del AppImage, que no la lee y dejaba la ventana muy pequeña. Desde la 1.14 lo hace también cuando la configuración de fontconfig fija otra resolución para las fuentes, como 96 DPI, que dejaba el texto del RPM a la mitad de su tamaño en una pantalla al 200 %; el tamaño de la ventana se guarda en píxeles a 96 DPI y se escala al abrirla.

Necesita conexión a internet para descargar las páginas, aunque las que ya están en la caché se muestran sin volver a pedirlas.

## Ambiente

Fue desarrollado en Fedora Linux 45 con KDE Plasma, con Python 3.15, y con git, con repositorios en GitHub y Codeberg (`nivaca/py-wk`; las direcciones viejas, `nivaca/py-wtk`, llevan allí). El RPM se publica en Copr, en el proyecto `nivaca/py-wk` (hasta la 1.15, `nivaca/py-wtk`, pues Copr no permite renombrar un proyecto).

Para usarlo no hay que instalar nada: se descarga el AppImage y se ejecuta, o se descomprime el zip y se ejecutan sus lanzadores (`py-wk`, `py-wk-tui`, `py-wk-gui`). Si se quiere, `python3 py-wk-install.py` añade accesos al menú de aplicaciones, con su icono y sin permisos de administrador. Los ajustes quedan en la carpeta de configuración del usuario (`~/.config/py-wk/config.toml` en Linux) y la caché en su carpeta de caché (`~/.cache/py-wk` en Linux).

Las instrucciones completas de instalación y de uso están en el [README](../README.es.md); los cambios de cada versión, en [NOTES.es.md](NOTES.es.md).
