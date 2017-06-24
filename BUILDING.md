Instructions for building standalone executables for Windows. These
instructions expect Python 3.6 (Anaconda is recommended).

Please note that these are not requirements for installing or running RespiRate
from our prebuilt installers, which require no additional software inside
Windows. These instructions only apply to building a standalone Windows
executable yourself.

### Prerequisites
 - Python 3.6.  
 It is possible to build a standalone Windows executable with earlier versions
 of Python 3, but you may need to adjust these instructions.

 Python 2 is **not** supported.

 - matplotlib, numpy, pyqt5, qt5, requests, scipy, subprocess, and tkinter:  
 `conda install matplotlib, numpy, pyqt=5, qt=5, scipy, tkinter`

 - xlutils:  
 `pip install xlutils`

 - The current development version of PyInstaller:  
`pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip`  
 We require the development version since the stable releases do not support
 Python 3.6. If you are using an earlier version of Python 3, you can use the
 stable version of pyinstaller:  
 `pip install PyInstaller`

 - OpenCV compiled with ffmpeg support.  
 Download from http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv.  
 For 64-bit computers, download opencv_python‑3.2.0‑cp36‑cp36m‑win_amd64.whl.  
 For 32-bit, download opencv_python‑3.2.0‑cp36‑cp36m‑win32.whl.  
 Navigate to your downloaded file, hold Shift and right-click, and choose "Open
 a command window here."  
 For 64-bit computers, use  
 `pip install .\opencv_python-3.2.0-cp36-cp36m-win_amd64.whl`  
 For 32-bit computers, use  
 `pip install .\opencv_python‑3.2.0‑cp36‑cp36m‑win32.whl`  

 - This program's source code. You may either download the source to the latest
 stable release, available at  
 https://github.com/MDA-Courtyard/RespiRate/releases/latest,  
 or the development source, available at  
 https://github.com/MDA-Courtyard/RespiRate/archive/master.zip

### Building
 Inside this program's source directory, open a command prompt window and run
 'python setup_win.py'.

 Once the executable has been built, it will be in the dist\RespiRate
 folder. You can run it from there and/or copy the entire RespiRate folder to
 any location; however, the executable will fail to run if you move it outside
 the RespiRate folder.
