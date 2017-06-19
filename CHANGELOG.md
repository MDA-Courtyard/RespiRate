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
