# -*- coding: utf-8 -*-
# notifiCat.py
# Copyright (C) 2017 Ashlar Ruby
# Licensed under the MIT license. See COPYING.md for details.
from tkinter import Tk, messagebox
# Meow
'''
Use me to display notifications. I can be used in multiple functions
simultaneously so you don't end up with redundant/conflicting code.
'''

def errorNotif(msg):
    '''Display an error or warning message.'''
    # Used in RespiRate and MouseFunctions
    root = Tk()
    root.withdraw()
    messagebox.showerror('Error', msg)
    root.destroy()

def infoNotif(title, msg):
    '''Display a notification message.'''
    # Used in MouseFunctions
    root = Tk()
    root.withdraw()
    messagebox.showinfo(title, msg)
    root.destroy()

def askQuestion(title, msg):
    '''Ask a question with a yes/no dialog.'''
    # Used in RespiRate and MouseFunctions
    root = Tk()
    root.withdraw()
    ans = messagebox.askquestion(title, msg)
    root.destroy()
    return(ans)
