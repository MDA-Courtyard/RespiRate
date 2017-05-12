Instructions for building standalone executeables for Windows. These
instructions expect Python 3.6 (Anaconda is recommended).

### Prerequisites
 - Python 3.6.
 It is possible to build a standalone Windows executable with earlier versions
 of Python 3, but you will need to adjust the instructions accordingly and edit
 `setup_win.py` so that it calls pyinstaller as a globally installed program,
 not as a python script.

 Python 2 is NOT supported.

 - matplotlib, numpy, pyqt5, qt5, scipy, subprocess, and tkinter:
 `conda install matplotlib, numpy, pyqt=5, qt=5, scipy, tkinter`

 - xlutils:
 `pip install xlutils`

 - the current development version of PyInstaller:
 Download from https://github.com/pyinstaller/pyinstaller/zipball/develop.
 We require the development version since the stable releases do not support
 Python 3.6. If you are willing to edit setup_win.py as required, you could
 probably generate a successful build with an earlier version of Python 3 and
 the stable release of PyInstaller.

 - opencv compiled with ffmpeg support.
 Download from http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv. For 64-bit
 computers, download opencv_python‑3.2.0‑cp36‑cp36m‑win_amd64.whl. For 32-bit,
 download opencv_python‑3.2.0‑cp36‑cp36m‑win32.whl.
 Navigate to your downloaded file, hold Shift and right-click, and choose "Open
 a command window here."
 For 64-bit computers, use
 `pip install .\opencv_python-3.2.0-cp36-cp36m-win_amd64.whl`
 For 32-bit computers, use
 'pip install .\opencv_python‑3.2.0‑cp36‑cp36m‑win32.whl'

 - This program's source code. If you're reading this, you probably already have
 it.

### Building
 Inside this program's source directory, open a command prompt window and run
 'python setup_win.py'.

 You will be prompted to enter the location of the pyinstaller development code.
 You may use either relative or absolution paths. For example, if it is in
 C:\Users\<your_user_name>\pyinstaller\, and the command prompt is being run
 from C:\Users\<your_user_name>\, you could type
 `C:\Users\<your_user_name>\pyinstaller\`
 or simply
 `pyinstaller\`
Be sure to type a final trailing backslash ("\").

 Once the executable has been built, it will be in the dist\RespiRate
 folder. You can run it from there and/or copy the entire RespiRate folder to
 any location; however, the executable will fail to run if you move it outside
 the RespiRate folder.
