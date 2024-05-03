# Simple Manga Viewer

## Features

 - Open manga image folders or PDF manga files
 - Switch paging direction from LTR and RTL
 - Built-in image post-processing algorithms (image smoothing, Anime4K upscale, etc.)
 - Touch screen long press and tap to flip support

> [!TIP]
> A much smaller LITE version without numpy&opencv upscale stuff is available. See below.

## Control

**Page flipping**: Click/touch the left/right half of the screen, mouse wheel, or keyboard arrow keys.

**Show menu**: Click/touch and hold anywhere on the screen for 2 seconds.

(Does not support touch swipe gestures; does not support saving image post-processing preferences)

## How to use

Tested on Windows11 21H2 and Debian 12 (GNOME Wayland), both touchscreen and keyboard.

### Use precomplied binary

Windows: Full version (313MB) & LITE version (30MB)

Debian/Ubuntu: WIP...

### Run from source

Python 3.10.14 is recommended. X86_64 CPU is required.

Remember to manually remove numpy, opencv-python and pyanime4K from `requirements.txt` if you only need to run/compile a LITE version.

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
cd .\src
python -m SimpleMangaViewer.py
```

and for the LITE version:

```bash
python -m SimpleMangaViewerLITE.py
```

### Compile your own

Step 1:
 
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install nuitka
cd .\src
nuitka --standalone --show-progress --disable-console --include-package=pyanime4k --plugin-enable=pyside6 --windows-icon-from-ico="path_to_icon-512.ico" --output-dir=build_output SimpleMangaViewer.py
```

and for the LITE version:

```bash
nuitka --standalone --show-progress --disable-console --onefile --plugin-enable=pyside6 --windows-icon-from-ico="path_to_icon-512.ico" --output-dir=build_output SimpleMangaViewerLITE.py
```

Check pyanime4K repo for the installation script on linux.

Step 2: Copy the `pyanime4K` folder from `Lib\site-packages` into `SimpleMangaViewer.dist` folder if not LITE version.

Step 3: Copy `icon-512.png` into the same folder as well. (optional)

Step 4: Run the `.exe` file in folder `SimpleMangaViewer.dist`.
