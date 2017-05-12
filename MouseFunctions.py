# -*- coding: utf-8 -*-
# MouseFunctions.py
# Copyright (C) 2017 Ashlar Ruby
# Licensed under the MIT license. See COPYING.md for details.

from os import mkdir, path
import xlrd
from xlutils.copy import copy
import xlwt
import notifiCat

def ListOfLists(lengthOfList):
    allLists = []
    oneList= []
    for i in range(lengthOfList):
        allLists.append([])
    for j in oneList:
        allLists[i].append(j)
    return allLists

def find(stdevs, minstvar):
    for i, pointst in enumerate(stdevs):
        try:
            j = pointst.index(minstvar)
        except ValueError:
            continue
        yield i, j

def xOutput(toPrintList, workBook, sheetName):
    '''Export data to spreadsheet for easy review and analysis.'''
    if workBook == 0 and sheetName == 0:
        errorNotif('Data was not saved to spreadsheet!')
    else:
        try:
            # Check if the target file already exists.
            dir_path = path.join(path.expanduser('~'), 'RespiRate')
            file_path = path.join(dir_path, workBook)
            if path.isfile(file_path) == False:
                q = ('A suitable spreadsheet was not found.\n'
                'Would you like to generate one automatically?')
                new = notifiCat.askQuestion('No spreadsheet.', q)
                if new == 'yes':
                    # Test if the folder exists. It might even if the file does not.
                    if not path.exists(dir_path):
                        mkdir(dir_path)
                    # Set up the spreadsheet
                    book = xlwt.Workbook()
                    sheet1 = book.add_sheet('Sheet1')
                    column0 = 'Video #'
                    column1 = 'Mouse #'
                    column2 = 'Start Time'
                    column3 = 'End Time'
                    column4 = 'Total Time'
                    column5 = 'Best RR'
                    column6 = 'stdev'
                    sheet1.write(0, 0, column0)
                    sheet1.write(0, 1, column1)
                    sheet1.write(0, 2, column2)
                    sheet1.write(0, 3, column3)
                    sheet1.write(0, 4, column4)
                    sheet1.write(0, 5, column5)
                    sheet1.write(0, 6, column6)
                    book.save(file_path)
                    created_msg = ('Spreadsheet was created as `output1.xls` in'
                            ' the RespiRate folder.')
                    notifiCat.infoNotif('Success!', created_msg)
                else:
                    return
            # The file exists (or was just created) - now write output.
            open(file_path, 'r+')
            wb = xlrd.open_workbook(file_path)   #output1.xls
            sheet = wb.sheet_by_name(sheetName)   #Sheet1
            rb = copy(wb)
            ws = rb.get_sheet(0)
            row = 0
            col = 0
            cell = sheet.cell(row, 0)
            try:
                while cell.ctype != 6:
                    row = row + 1
                    cell = sheet.cell(row, 0)
            except IndexError:
                print('index error') #TODO: Why do we get this for every run?
            for i in range(0, len(toPrintList)):
                ws.write(row, col, toPrintList[i])
                col = col + 1
            rb.save(file_path)
        except IOError:
            # If we get this far, the spreadsheet cannot be opened (most likely
            # it is already opened in Excel or another program). Check it, close
            # it, and rerun it. Working now?
            notifiCat.errorNotif('Data cannot be exported!\n'
                    'Please check if the spreadsheet is already opened.')
