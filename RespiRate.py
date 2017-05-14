# -*- coding: utf-8 -*-
# RespiRate.py
# Copyright (C) 2017 Ashlar Ruby
# Licensed under the MIT license. See COPYING.md for details.
import ctypes
import itertools
from os import path
import re
from platform import platform, system
from subprocess import call
import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
import requests
from RespiRateUI import Ui_MainWindow
import MouseVideo as mv
import MouseFunctions as mf
import peakdetect as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from tkinter import Tk, Label, Entry, Button, mainloop
from notifiCat import errorNotif, askQuestion, infoNotif

class Gui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.videoFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.actionOpen_video.triggered.connect(self.openNew)
        self.ui.actionOpen_spreadsheet.triggered.connect(self.openOutput)
        self.ui.actionQuit.triggered.connect(self.closeAll)
        self.ui.actionCheck_for_Update.triggered.connect(self.updateCheck)
        self.ui.actionAbout.triggered.connect(self.About)
        self.ui.actionAbout_Qt.triggered.connect(self.AboutQt)
        self.slide = self.ui.horizontalSlider
        self.slide.valueChanged.connect(self.slider_value_change)
        self.ui.pushButton_Play.clicked.connect(self.playPressed)
        self.ui.pushButton_Pause.clicked.connect(self.pausePressed)
        self.ui.pushButton_SelectST.clicked.connect(self.enterStartT)
        self.ui.pushButton_Contour.clicked.connect(self.contourPressed)
        self.ui.pushButton_Clear.clicked.connect(self.ui.textBrowser_Output.clear)
        self.ui.lineEdit_mouseID.textChanged.connect(self.enableButton)
        self.ui.lineEdit_startT.textChanged.connect(self.enableButton2)
        self.ui.lineEdit_lenMeasure.textChanged.connect(self.enableButton3)
        self.ui.pushButton_Contour.setEnabled(False)
        self.ui.textBrowser_Output.setReadOnly(True)
        self.cont = 0
        self.enableCount = 0
        self.enableCount2 = 0
        self.enableCount3 = 0
        rcParams['figure.figsize'] = 14, 2
        self.filename = 0
        self.capture = 0
        self.length = 0
        self.currentFrame = 0
        self.endTimemsec = 0
        self.img = 0
        self.sliderVal = 0
        self.timeInSec = 0
        self.displayTime = 0
        self.totalCount = 0
        self.lenOfMeas = 0
        self.startTimemsec = 0
        self.firstframe = 0
        self.lastframe = 0
        self.length = 0
        self.numberOfMice = 0
        self.version = '0.0.2~development'
        self._timer = QtCore.QTimer(self)
        if self.cont == 0:
            self._timer.timeout.connect(self.captureNextFrame)
        else:
            self._timer.timeout.connect(self.opticalFlowTrack)
        self.update()


    def closeAll(self):
        '''Shut down cleanly when Quit is clicked.'''
        if isinstance(self.capture, int) == False:
            self.capture.release()
        cv2.destroyAllWindows()
        self._timer.stop()
        sys.exit(0)


    def updateCheck(self):
        '''Check for updates.'''
        resp = requests.get('https://github.com/MDA-Courtyard/RespiRate/releases/')
        data = str(resp.text)
        index = data.find('RespiRate/releases/tag/v')
        upstream_ver =  data[index + 32] + data[index + 33] + data[index + 34] + data[index + 35] + data[index + 36]
        if upstream_ver > self.version:
            msg_up = ('Version '+upstream_ver+' has been released.\n'
            'Download it from https://github.com/MDA-Courtyard/RespiRate/releases.\n')
            infoNotif('RespiRate', msg_up)
        else:
            msg_up = 'You have the latest available version of RespiRate.'
            infoNotif('RespiRate', msg_up)


    def About(self):
        '''Brief description of the program.'''
        title = 'About'
        msg = ('<p><br><b>RespiRate v'+self.version+'</b></br>'
                '<br>Copyright (C) 2017 Ashlar Ruby</br>'
                '<br>Licensed under the MIT license.</br></p>'
                '<p>This program uses opencv_ffmpeg320 libraries, released'
                '<br>and copyrighted 2001 under the LGPL by Fabrice Bellard,</br>'
                '<br>and the PyQt5 and Tkinter graphical toolkits.</br></p>'
                '<p><a href="https://github.com/MDA-Courtyard/RespiRate">Home Page</a>'
                '<br><a href="https://github.com/MDA-Courtyard/RespiRate/releases">Releases</a></br>'
                '<br><a href="https://github.com/MDA-Courtyard/RespiRate/blob/master/COPYING.md">Contributors and License</a></br></p>')
        QtWidgets.QMessageBox.about(self, title, msg)


    def AboutQt(self):
        '''Show a message box about Qt (useful for debugging).'''
        QtWidgets.QMessageBox.aboutQt(self)


    def openNew(self):
        '''
        Select and open a video file from the system file manager for analysis.
        '''

        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Video')
        self.filename = str(self.filename[0])
        # We get a zero division error on self.length if the filename is empty.
        try:
            # Don't even try if user pressed 'Cancel' in file dialog
            if not self.filename == '':
                print(self.filename+'\n')
                self.capture = cv2.VideoCapture(self.filename)
                self.capture.open(self.filename)
                self.currentFrame = np.array([])
                self.length = int(self.capture.get(7) / self.capture.get(5))
                self.endTimemsec = self.length * 1000
                self.slide.setMinimum(0)
                self.slide.setMaximum(self.length)
                self.slide.setTracking(0)
                self.ui.lcdNumber.setNumDigits(8)
                self.ui.lcdNumber.display('00:00:00')
                self.slide.setSliderPosition(0)
                self.cont = 0
                self.captureNextFrame()

        except ZeroDivisionError:
            errorNotif('Not a recognized video format.')
            self.filename = 0

    def openOutput(self):
        '''Open the spreadsheet to which mouse data is exported.'''
        location = path.join(path.expanduser('~'), 'RespiRate')
        ssheet = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', location)[0]
        ssheet = str(ssheet)
        if not ssheet == '':
            print('Opening %r' % ssheet)
            if system() == 'Windows':
                call(['start', ssheet], shell=True)
            elif system() == 'Darwin':
                call(['open', ssheet], shell=True)
            elif system() =='Linux':
                call(['xdg-open', ssheet])


    def captureNextFrame(self):
        '''capture frame and reverse RGB BGR and return opencv image'''
        if self.cont == 0:
            ret, readFrame = self.capture.read()
            self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)
            height,width = self.currentFrame.shape[:2]
            self.img = QtGui.QImage(self.currentFrame,
                              width,
                              height,
                              QtGui.QImage.Format_RGB888)
            self.img = QtGui.QPixmap(self.img)
            self.ui.videoFrame.setPixmap(self.img.scaled(self.ui.videoFrame.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self._timer.timeout.connect(self.tick)
            self._timer.start()

        elif self.cont == 1:
            ret, readFrame = self.capture.read()
            self.currentFrame = cv2.cvtColor(readFrame,cv2.COLOR_BGR2RGB)
            height,width = self.currentFrame.shape[:2]
            self.img = QtGui.QImage(self.currentFrame,
                              width,
                              height,
                              QtGui.QImage.Format_RGB888)
            self.img = QtGui.QPixmap(self.img)
            self.ui.videoFrame.setPixmap(self.img.scaled(self.ui.videoFrame.size(),
                QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            if self.capture.get(0) >= self.endTimemsec:
                self.capture.set(0, self.startTimemsec)
            self._timer.timeout.connect(self.tick)
            self._timer.start()

        elif self.cont == 2:
            self._timer.stop()


    def slider_value_change(self, value):
        '''If the slide is moved manually, skip the video to the corresponding time.'''
        self.sliderVal = value * 1000
        self.capture.set(0, self.sliderVal)


    def tick(self):
        timecv = self.capture.get(0)
        self.timeInSec = timecv / 1000
        self.displayTime = QtCore.QTime((timecv / 3600000) % 60, (timecv / 60000) % 60, (timecv / 1000) % 60)
        self.ui.lcdNumber.display(self.displayTime.toString('hh:mm:ss'))
        # TEST
        self.slide.setSliderPosition(self.timeInSec)
        # self.moveSlide()


    # def moveSlide(self):
    #     '''Keep the main window slide moving.'''
    #     timecv = self.capture.get(0)
    #     self.timeInSec = timecv / 1000
    #     self.slide.setSliderPosition(self.timeInSec)


    def pausePressed(self):
        '''Pause the video in the main window.'''
        self._timer.stop()


    def playPressed(self):
        '''Play the video in the main window.'''
        self._timer.start()


    def enterStartT(self):
        '''Select the current video time as start time of measurement.'''
        self.ui.lineEdit_startT.setText(self.displayTime.toString('hh:mm:ss'))


    def enableButton(self):
        '''Enables the Contour button when all three fields are filled.'''
        self.enableCount = 1
        self.totalCount = self.enableCount + self.enableCount2 + self.enableCount3
        if self.totalCount == 3:
            self.ui.pushButton_Contour.setEnabled(True)


    def enableButton2(self):
        '''Enables the Contour button when all three fields are filled.'''
        self.enableCount2 = 1
        self.totalCount = self.enableCount + self.enableCount2 + self.enableCount3
        if self.totalCount == 3:
            self.ui.pushButton_Contour.setEnabled(True)


    def enableButton3(self):
        '''Enables the Contour button when all three fields are filled.'''
        self.enableCount3 = 1
        self.totalCount = self.enableCount + self.enableCount2 + self.enableCount3
        if self.totalCount == 3:
            self.ui.pushButton_Contour.setEnabled(True)


    def contourPressed(self):
        '''Contour button has been pressed - begin analysis.'''
        self.cont = 1
        # Get the number of mice, start time, and length of measurement.
        mice = self.ui.lineEdit_mouseID.text()
        tsec = self.ui.lineEdit_startT.text()
        self.lenOFMeas = self.ui.lineEdit_lenMeasure.text()

        # Do a quick scan for errors and halt execution if necessary.
        error_check = self.errorCheck(tsec)
        if error_check == 'error':
            return

        # Number of mice we are using.
        self.numberOfMice = len([int(x) for x in mice.split(',')])
        startTimehhmmss = [int(x) for x in tsec.split(':')]
        # Time (in seconds) that we begin the measurement
        startTimeSec = (3600 * startTimehhmmss[0]) + (60 * startTimehhmmss[1]) + startTimehhmmss[2]
        self.startTimemsec = startTimeSec * 1000    # start-time in miliseconds
        lenOfMeasmsec = int(self.lenOFMeas) * 1000
        self.endTimemsec = self.startTimemsec + lenOfMeasmsec # ending time
        endTime = self.endTimemsec
        self.capture.set(0, self.endTimemsec)
        self.lastframe = self.capture.get(1)
        self.capture.set(0, self.startTimemsec)
        self.firstframe = self.capture.get(1)
        self.length = int(self.lenOFMeas)
        # Reset slide to show length of analysis time.
        self.slide.setMinimum(startTimeSec)
        self.slide.setMaximum(self.length + startTimeSec)
        self.slide.setSliderPosition(startTimeSec)
        self.captureNextFrame()
        self._timer.start()


        incontours = []
        mouseNumList = []
        respRates = []
        bRespRates = []
        minstdevs = []
        # Get a unique mouse ID for each mouse.
        for numba in range(0, self.numberOfMice):
            vid = mv.frameReader(self.filename)
            img = vid.getFrame(self.firstframe)
            conty = mv.contour(img)

            def WhichMouse(entry=None):
                global mouseNum
                mouseNum = e1.get()
                master.destroy()

            master = Tk()
            master.title('Please enter the mouse ID')
            master.minsize(325,25)
            Label(master, text='Mouse #').grid(row=0)
            e1 = Entry(master)
            e1.grid(row=0, column=1)
            e1.focus_force()
            button = Button(master, text='OK', command=WhichMouse)
            button.grid(row=0, column=3, sticky='W', pady=4)
            master.bind ('<Return>', WhichMouse)
            mainloop()
            mouseNumList.append(mouseNum)
            inconty = mv.insideContour(conty, img)
            incontours.append(inconty)

        self.cont = 2
        # Parameters for Shi-Tomasi corner detection
        feature_params = dict( maxCorners = 10,
                          qualityLevel = 0.3,
                          minDistance = 7,
                          blockSize = 7)
        # Parameters for Lucas-Kanade optical flow
        lk_params = dict( winSize  = (15, 15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # Create some random colors
        color = np.random.randint(0, 255, (100, 3))
        self.capture.set(1, self.firstframe)

        # Take first frame and find corners in it
        ret, old_frame = self.capture.read()
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0s = mf.ListOfLists(self.numberOfMice)
        for numba in range(0, self.numberOfMice):
            p0s[numba] = cv2.goodFeaturesToTrack(old_gray, mask = incontours[numba], **feature_params)

        # Create a mask image for drawing purposes
        mask = np.zeros_like(old_frame)
        xPoints = mf.ListOfLists(self.numberOfMice)
        yPoints = mf.ListOfLists(self.numberOfMice)
        p1s = mf.ListOfLists(self.numberOfMice)
        sts = mf.ListOfLists(self.numberOfMice)
        errs = mf.ListOfLists(self.numberOfMice)
        good_news = mf.ListOfLists(self.numberOfMice)
        good_olds = mf.ListOfLists(self.numberOfMice)
        dists = mf.ListOfLists(self.numberOfMice)
        pointPos = mf.ListOfLists(self.numberOfMice)
        peakPos = mf.ListOfLists(self.numberOfMice)

        for numba in range(0, self.numberOfMice):
            for i in range(len(p0s[numba])):
                xPoints[numba].append([])
                yPoints[numba].append([])

        l=0

        for num in range(np.int(self.firstframe), np.int(self.lastframe + 1)):
            ret,frame = self.capture.read()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            stzeros = []
            for numba in range(0,self.numberOfMice):
                stzeros.append(np.array([]))
            for numba in range(0,self.numberOfMice):
                # Calculate optical flow
                p1s[numba], sts[numba], errs[numba] = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0s[numba], None, **lk_params)
                # Select good points
                if np.any(sts[numba]) == 0:
                    break
                good_news[numba] = p1s[numba][sts[numba] == 1]
                good_olds[numba] = p0s[numba][sts[numba] == 1]
                if (len(p0s[numba]) != len(good_olds[numba])):
                    stzeros[numba] = np.where(sts[numba] == 0)[0]
                    for j in stzeros[numba][::-1]:
                        for i in range(len(p0s[numba])):
                            if i == j:
                                del xPoints[numba][i]
                                del yPoints[numba][i]

                # Draw the tracks
                for i,(new,old) in enumerate(list(zip(good_news[numba],good_olds[numba]))):
                    a,b = new.ravel()
                    c,d = old.ravel()
                    xPoints[numba][i].append([])
                    yPoints[numba][i].append([])
                    xPoints[numba][i][l].append(c)
                    yPoints[numba][i][l].append(d)
                    mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
                    frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
                p0s[numba] = good_news[numba].reshape(-1,1,2) # Update the previous points
            if np.any(sts[numba]) == 0:
                    endTime = self.capture.get(0)
                    break
            img = cv2.add(frame, mask)
            cv2.imshow('flow', img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                endTime = self.capture.get(0)
                break

            # Now update the previous frame
            old_gray = frame_gray.copy()
            l = l + 1

        # If the measurement field on the mouse is out of focus or the mouse
        # moves too much, the program crashes with a division by zero error
        # starting at avgs[i].append(sum(distBTpeaksxt[i]) / len(distBTpeaksxt[i]))
        try:
            for numba in range(0, self.numberOfMice):
                pointx = mf.ListOfLists(len(p0s[numba]))
                pointy = mf.ListOfLists(len(p0s[numba]))
                peaksx = mf.ListOfLists(len(p0s[numba]))
                peaksy = mf.ListOfLists(len(p0s[numba]))
                distBTpeaksxt = mf.ListOfLists(len(p0s[numba]))
                distBTpeaksxb = mf.ListOfLists(len(p0s[numba]))
                distBTpeaksyt = mf.ListOfLists(len(p0s[numba]))
                distBTpeaksyb = mf.ListOfLists(len(p0s[numba]))
                avgs = mf.ListOfLists(len(p0s[numba]))
                stdevs = mf.ListOfLists(len(p0s[numba]))

                for i in range(len(p0s[numba])):
                    pointx[i] = xPoints[numba][i]
                    peaksx[i] = pd.peakdetect(pointx[i], None, 4, 0) #3 for mice, 20 for human
                    pointy[i] = yPoints[numba][i]
                    peaksy[i] = pd.peakdetect(pointy[i], None, 4, 0)

                for ii in range(len(p0s[numba])):
                    for i in range(len(peaksx[ii][0]) - 1):
                        distBTpeaksxt[ii].append(peaksx[ii][0][i + 1][0] - peaksx[ii][0][i][0])
                    for i in range(len(peaksx[ii][1]) - 1):
                        distBTpeaksxb[ii].append(peaksx[ii][1][i + 1][0] - peaksx[ii][1][i][0])
                    for i in range(len(peaksy[ii][0]) - 1):
                        distBTpeaksyt[ii].append(peaksy[ii][0][i + 1][0] - peaksy[ii][0][i][0])
                    for i in range(len(peaksy[ii][1]) - 1):
                        distBTpeaksyb[ii].append(peaksy[ii][1][i + 1][0] - peaksy[ii][1][i][0])

                for i in range(len(p0s[numba])):
                    avgs[i].append(sum(distBTpeaksxt[i]) / len(distBTpeaksxt[i])) #xtop
                    stdevs[i].append(np.std(distBTpeaksxt[i]) / avgs[i][0]) #xtop
                    avgs[i].append(sum(distBTpeaksxb[i]) / len(distBTpeaksxb[i])) #xbottom
                    stdevs[i].append(np.std(distBTpeaksxb[i]) / avgs[i][1]) #xbottom
                    avgs[i].append(sum(distBTpeaksyt[i]) / len(distBTpeaksyt[i])) #ytop
                    stdevs[i].append(np.std(distBTpeaksyt[i]) / avgs[i][2]) #ytop
                    avgs[i].append(sum(distBTpeaksyb[i]) / len(distBTpeaksyb[i])) #ybottom
                    stdevs[i].append(np.std(distBTpeaksyb[i]) / avgs[i][3]) #ybottom

                merged = list(itertools.chain.from_iterable(stdevs))
                minst = min(merged)
                matches = [match for match in mf.find(stdevs, minst)]
                bestPoints = list(zip(*matches))[0]
                distInd = list(zip(*matches))[1]
                best = mf.ListOfLists(len(p0s[numba]))
                beststdev = mf.ListOfLists(len(p0s[numba]))
                for ii in range(len(p0s[numba])):
                    minimummy = min(stdevs[ii])
                    mins = [i for i, j in enumerate(stdevs[ii]) if j == minimummy]
                    for i in range(len(mins)):
                        best[ii] = avgs[ii][mins[i]]
                        beststdev[ii] = stdevs[ii][mins[i]]

                minstdev = min(beststdev)
                indMinStdev = [i for i, j in enumerate(beststdev) if j == minstdev]
                bavg = [best[i] for i in indMinStdev]
                avgOfbest = sum(best) / len(best)
                avgOfbavg = sum(bavg) / len(bavg)

                font = {'family': 'sans-serif',
                        'color':  'black',
                        'weight': 'normal',
                        'size': 12}

                # Plotting
                print('distInd', distInd)
                xaxis = range(0, len(pointx[numba]))
                xaxisYtop = list(zip(*peaksy[numba][0]))[0]
                xaxisYbottom = list(zip(*peaksy[numba][1]))[0]
                xaxisT = [x / 30 for x in xaxis]
                xaxisYtopT = [x / 30 for x in xaxisYtop]
                xaxisYbottomT = [x / 30 for x in xaxisYbottom]
                plt.ion() # cosmetic, QCoreApplication error without this
                plt.figure('Mouse %s' % mouseNumList[numba]) # Window name
                plt.plot(xaxisT, pointy[numba], color='#3399FF') # Curve
                plt.plot(xaxisYtopT, list(zip(*peaksy[numba][0]))[1], 'o', color='red', markersize=4) # Peak
                plt.plot(xaxisYbottomT, list(zip(*peaksy[numba][1]))[1], 'o', color='#FF9966', markersize=4) # Valley
                plt.title('Mouse '+str(mouseNumList[numba]), fontdict=font)

                pointPos[numba].append(pointy[numba])
                peakPos[numba].append(peaksy[numba])
                plt.xlabel('Time (s)', fontdict=font)
                frame1 = plt.gca()
                frame1.axes.get_yaxis().set_ticks([])
                plt.tight_layout() # Don't cut off the title and x-label
                plt.show()

                print('Best: ' + str([round(elem, 3) for elem in best]) + '\n')
                print('Best Stdev: ' + str([round(elem, 4) for elem in beststdev]) + '\n')

                respRate = (60 * 30) / avgOfbest
                bRespRate = (60 * 30) / avgOfbavg
                respRates.append(respRate)
                bRespRates.append(bRespRate)
                minstdevs.append(minstdev)
                for i,(bp,ind) in enumerate(list(zip(bestPoints, distInd))):
                    if ind == 0:
                        dists[numba].append(distBTpeaksxt[bp])
                    if ind == 1:
                        dists[numba].append(distBTpeaksxb[bp])
                    if ind == 2:
                        dists[numba].append(distBTpeaksyt[bp])
                    if ind == 3:
                        dists[numba].append(distBTpeaksyb[bp])

            # Show results in GUI display box
            for numba in range(0, self.numberOfMice):
                toPrint1 = mouseNumList[numba]
                toPrint2 = round(bRespRates[numba], 2)
                toPrint3 = round(minstdevs[numba], 4)
                out = ' {:<18}  {:^21.2f}  {:>21.4f} '.format(toPrint1, toPrint2, toPrint3)
                self.ui.textBrowser_Output.append(out)

            # Measurement terminated before full run time
            if endTime != self.endTimemsec:
                errorNotif('Measurement did not run for entire set length.')

            # Ask if we want to export data to a spreadsheet
            export = askQuestion('RespiRate', 'Export data to spreadsheet?')
            if export == 'yes':
                for numba in range(0, self.numberOfMice):
                    # videoNum = re.search('Video (.*)\.', self.filename).group(1)
                    videoNum = path.splitext(path.basename(self.filename))[0]
                    toPrintList = [str(videoNum), str(mouseNumList[numba]),
                        str(startTimeSec), str(endTime / 1000),
                        str((endTime / 1000) - (startTimeSec)),
                        str(round(bRespRates[numba], 2)),
                        str(round(minstdevs[numba], 4))]
                    workBook = 'output1.xls'
                    sheetName = 'Sheet1'
                    mf.xOutput(toPrintList, workBook, sheetName)

        except ZeroDivisionError:
            msg = ('The selected region on '+ str(mouseNumList[numba])+
                ' is not suitable for respiration measurements')
            errorNotif(msg)

        # Close the secondary windows.
        cv2.destroyAllWindows()


    def errorCheck(self, tsec):
        '''Check for common mistakes and return a notification.'''
        msg_video = 'You have not selected a video!'
        msg_time = 'Time must be in hh:mm:ss format.'
        msg_len = 'The given length of measurement cannot be understood.'
        tsec = str(tsec)
        time_check = tsec.split(':')
        len_measure = str(self.lenOFMeas)

        # A video hasn't been selected. Note that this doesn't detect if the
        # selected file is actually a video, but only if a file (any type) has
        # been chosen.
        if self.filename == 0 or self.filename == u'':
            errorNotif(msg_video)
            return 'error'

        # Check if measurement length makes sense
        elif len_measure.isdigit() == False:
            errorNotif(msg_len)
            return 'error'

        # Check the following:
        # - Start time is in correct format (hh:mm:ss)
        # - Second and minute input don't go above 59
        # - Start time input is only integers (no letters or special characters)
        elif len(tsec) != 8:
            errorNotif(msg_time)
            return 'error'
        elif tsec[2] != ':' or tsec[5] != ':':
            errorNotif(msg_time)
            return 'error'
        elif 1 == 1: # Bit of a ugly hack
            for num in time_check:
                if num.isdigit() == False:
                    errorNotif(msg_time)
                    return 'error'
        elif int(time_check[-1]) > 59 or int(time_check[-2]) > 59:
            errorNotif(msg_time)
            return 'error'



def main():

    if system() == 'Windows': # Needed to display the icon in the taskbar
        if not 'Vista' in platform(): # Vista doesn't recognize this but works anyway.
            myappid = 'RespiRate'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app=QtWidgets.QApplication.instance()

    if not app:
        app = QtWidgets.QApplication(sys.argv)

    ex1 = Gui()
    ex1.setWindowTitle('RespiRate')
    ex1.setWindowIcon(QtGui.QIcon('RespiRate.ico'))
    ex1.raise_()
    ex1.show()
    ex1.activateWindow()
    app.exec_()
    ex1._timer.stop()
    sys.exit(0)


if __name__ == '__main__':
    main()
