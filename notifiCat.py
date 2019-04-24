# -*- coding: utf-8 -*-
# notifiCat.py
# Copyright (C) 2017 Ashlar Ruby
# Licensed under the MIT license. See COPYING.md for details.
from PyQt5.QtWidgets import QWidget, QMessageBox
# Meow
"""
Use me to display notifications. I can be used in multiple functions
simultaneously so you don't end up with redundant/conflicting code.
"""


def errorNotif(self, msg):
    """Display an error or warning message."""
    # Used in RespiRate and MouseFunctions
    if self == 'noself':
        self = QWidget()
    QMessageBox.warning(self, 'Error', '\n' + msg + '\n')


def infoNotif(self, title, msg):
    """Display a notification message."""
    # Used in RespiRate and MouseFunctions
    if self == 'noself':
        self = QWidget()
    QMessageBox.information(self, title, '\n' + msg + '\n')


def askQuestion(self, title, msg):
    """Ask a question with a yes/no dialog."""
    # Used in RespiRate and MouseFunctions
    # We can't use QMessageBox.question because it creates a modal dialog (i.e
    # it blocks viewing/interacting with other RespiRate windows). This means
    # that a user would not be able to check the data graphs until after
    # choosing whether to export the data.
    if self == 'noself':
        self = QWidget()
    ask = QMessageBox(self)
    ask.setWindowTitle(title)
    ask.setText(msg)
    ask.setIcon(QMessageBox.Question)
    ask.setDefaultButton(QMessageBox.Yes)
    ask.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    ask.setWindowModality(0)
    ask.activateWindow()
    ask.show()
    retval = ask.exec_()

    if retval == QMessageBox.Yes:
        ans = 'yes'
    else:
        ans = 'no'

    return ans
