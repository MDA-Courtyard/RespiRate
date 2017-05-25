## 0.0.3 (development)
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
