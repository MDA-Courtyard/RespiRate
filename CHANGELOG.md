# 0.0.7 (12/20/2017)
 * Code cleanup and style improvements with flake8 linter.
 * Removed unused import 're' from RespiRate.py
 * (Bundled .exe files) Downgrade to Python 3.5 and PyInstaller 3.2.1 to build
 .exe files since PyInstaller 3.6 currently has some problems with Qt programs -
 see https://github.com/pyinstaller/pyinstaller/issues/2659

# 0.0.6 (09/12/2017)
 * Correct notification when generating a csv file from an existing xls file.
 * Code cleanup.
 * The spreadsheet header is cleaner. Multiple words are joined with an
    underscore for easier indexing.
 * Best respiratory rate for each mouse is returned to the console (when running
    from source.)

## 0.0.5 (07/07/2017)
 * Bugfix: stop the internal timer when opening a new file. This prevents a
    crash when loading a non-video file, after having already loaded a video.
 * Make sure loaded file is a video when 'Contour' is pressed.
 * Better, more logical handling of 'Tab' key.
 * Bugfix: don't attempt to play a video if one is not loaded.
 * Add notification that when declining to create a new spreadsheet (if needed),
    the data was not exported even if the user previously selected 'Yes'.
 * Add option to easily convert the output1.xls spreadsheet to csv file.

## 0.0.4 (06/19/2017)
 * Open file dialog for selecting videos in the same location as the last run,
    rather than in the present working directory. For the first run, the
    behavior is unchanged.
 * Remove unnecessary code from binary installer
 * Better handling of sys.exit()
 * Show current video name and location in titlebar: i.e. "RespiRate - sample.mp4"
 * Bugfix: allow mouse ID to be a non-integer (previously exited with error)
 * The error check functionality has been promoted to a class so we can call
     certain aspects as needed.
 * Greatly improved detection and rejection of non-video files
 * Disable 'Select Start Time' button if a video is not loaded

## 0.0.3 (05.25.2017)
 * Don't restart video when current frame is also the last (useable) frame.
 * Overwrite existing graph(s) instead of appending - prevents formatting errors
 * All user input windows are provided by Qt5.
 * Automatically close contour window when user clicks 'Cancel' instead of
    providing the mouse ID, instead of requiring the user to close it.
 * Fix condition where an image file is loaded and not rejected like other
    non-video files
 * Call system commands through QProcess instead of subprocess - keeps main
    window from freezing while commands are executed

## 0.0.2 (05.18.2017)
 * Show hyperlinks in dialog windows instead of plain text
 * Move all functions in notifiCat from Tkinter to Qt
 * Fix OpenCV Error when video is at final frame
 * Don't crash on index error
 * Better handling of exceptions
 * add 'noself' option to notifiCat when modules have no QApplication (not currently used)

## 0.0.1 (05.12.2017)
 * Initial release
