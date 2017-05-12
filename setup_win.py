# -*- coding: utf-8 -*-
# Copyright (C) 2017 Ashlar Ruby
# Licensed under the MIT license. See COPYING.md for details.
'''
Build a standalone Windows executable.
See BUILDING.md for instructions.
'''
import os
import subprocess
import shutil
import platform

pyinst_path = input('Path to pyinstaller: ')
pwd = os.getcwd()

# Remove old build directories
if os.path.exists('__pycache__') == True:
    shutil.rmtree('__pycache__', ignore_errors=True)
if os.path.exists('build') == True:
    shutil.rmtree('build', ignore_errors=True)
if os.path.exists('dist') == True:
    shutil.rmtree('dist', ignore_errors=True)

subprocess.call(['python', pyinst_path+'pyinstaller.py', '--noconsole', '--clean', '--icon=RespiRate.ico', 'RespiRate.py'])

# Copy the icon
shutil.copyfile('RespiRate.ico', pwd+'\dist\RespiRate\RespiRate.ico')

# We require ffmpeg. Pyinstaller fails to build a .dll for it in Windows, so we
# must copy a prebuild .dll to the proper location.
if platform.machine() == 'AMD64'  or 'x86_64' and platform.system() == 'Windows':
    shutil.copyfile('opencv_ffmpeg320_64.dll', pwd+'\dist\RespiRate\opencv_ffmpeg320_64.dll')
elif platform.machine() == 'i386' and platform.system() == 'Windows':
    shutil.copyfile('opencv_ffmpeg320.dll', pwd+'\dist\RespiRate\opencv_ffmpeg320.dll')
