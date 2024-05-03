# Simple Manga Viewer

## Features

 - Open manga image folders or PDF manga files
 - Switch paging direction from LTR and RTL
 - Built-in image post-processing algorithms (image smoothing, Anime4K upscale, etc.)
 - No installation required (run directly from Python or compile to C executable binary)
 - Touch screen long press and tap to flip support

There would be another smaller version without numpy&opencv stuff, coming _soon_.

## Control

**Page flipping**: Click/touch the left/right half of the screen, mouse wheel, or keyboard arrow keys.

**Show menu**: Click/touch and hold anywhere on the screen for 2 seconds.

(Does not support touch swipe gestures; does not support saving image post-processing preferences)

## How to use

Tested on Windows11 21H2 and Debian 12 (GNOME Wayland), both touchscreen and keyboard.

### Use precomplied binary

WIP

### Run from source

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
cd .\src
python -m SimpleMangaViewer.py
```

### Compile from source

Step 1:
 
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install nuitka
cd .\src
nuitka --standalone --show-progress --disable-console --include-package=pyanime4k --plugin-enable=pyside6 --windows-icon-from-ico="path_to_icon-512.ico" --output-dir=build_output SimpleMangaViewer.py
```

Step 2: Copy the `pyanime4K` folder from `Lib\site-packages` into `SimpleMangaViewer.dist` folder. Copy `icon-512.png` into the same folder as well.

Step 3: Run the `.exe` file in folder `SimpleMangaViewer.dist`.
