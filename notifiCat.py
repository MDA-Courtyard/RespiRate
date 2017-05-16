# -*- coding: utf-8 -*-
# notifiCat.py
# Copyright (C) 2017 Ashlar Ruby
# Licensed under the MIT license. See COPYING.md for details.
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtCore
from tkinter import Tk, messagebox
# Meow
'''
Use me to display notifications. I can be used in multiple functions
simultaneously so you don't end up with redundant/conflicting code.
'''

def errorNotif(self, msg):
    '''Display an error or warning message.'''
    # Used in RespiRate and MouseFunctions
    if self == 'noself':
        self = QWidget()
    QMessageBox.warning(self, 'Error', '\n'+msg+'\n')

#
def infoNotif(self, title, msg):
    '''Display a notification message.'''
    # Used in RespiRate and MouseFunctions
    if self == 'noself':
        self = QWidget()
    QMessageBox.information(self, title, '\n'+msg+'\n')

def askQuestion(title, msg):
    '''Ask a question with a yes/no dialog.'''
    # Used in RespiRate and MouseFunctions
    root = Tk()
    root.withdraw()
    ans = messagebox.askquestion(title, msg)
    root.destroy()
    return(ans)
