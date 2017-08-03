# -*- coding: utf-8 -*-
# MouseFunctions.py
# Copyright (C) 2017 Ashlar Ruby
# Licensed under the MIT license. See COPYING.md for details.

from os import mkdir, path
import csv
import xlrd
from xlutils.copy import copy
import xlwt
import notifiCat

def ListOfLists(lengthOfList):
    allLists = []
    oneList = []
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

def xOutput(self, toPrintList, workBook, sheetName):
    '''Export data to spreadsheet for easy review and analysis.'''
    if workBook == 0 and sheetName == 0:
        notifiCat.errorNotif(self, '<br>Data was not saved to spreadsheet!</br>')
    else:
        try:
            # Check if the target file already exists.
            dir_path = path.join(path.expanduser('~'), 'RespiRate')
            file_path = path.join(dir_path, workBook)
            if path.isfile(file_path) == False:
                q = ('<p>A suitable spreadsheet was not found.'
                '<br>Would you like to generate one automatically?</br></p>')
                new = notifiCat.askQuestion(self, 'No spreadsheet.', q)
                if new == 'yes':
                    # Test if the folder exists. It might even if the file does not.
                    if not path.exists(dir_path):
                        mkdir(dir_path)
                    # Set up the spreadsheet
                    book = xlwt.Workbook()
                    sheet1 = book.add_sheet('Sheet1')
                    sheet1.write(0, 0, 'Video')
                    sheet1.write(0, 1, 'Mouse')
                    sheet1.write(0, 2, 'Start_Time')
                    sheet1.write(0, 3, 'End_Time')
                    sheet1.write(0, 4, 'Total_Time')
                    sheet1.write(0, 5, 'Best_RR')
                    sheet1.write(0, 6, 'stdev')
                    book.save(file_path)
                    created_msg = ('Spreadsheet was created as `output1.xls` in'
                            ' the RespiRate folder.')
                    notifiCat.infoNotif(self, 'Success!', created_msg)
                else:
                    noexpt_msg = 'Data was not exported to a spreadsheet.'
                    notifiCat.infoNotif(self, 'Not Exported', noexpt_msg)
                    return
            # The file exists (or was just created) - now write output.
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
            err_msg = ('Data cannot be exported!'
                        '<br>Please check if the spreadsheet is already opened.</br>')
            notifiCat.errorNotif(self,err_msg)

def convertCSV(self, target_dir, workBook):
    '''Convert the current output1.xls to a .csv file.'''
    try:
        # Get the file name from the path and then drop the extension
        name = workBook.split('/')[-1].split('.')[0]
        wbook = xlrd.open_workbook(workBook)
        sheet = wbook.sheet_by_name('Sheet1')
        # We need newline='' or extra rows are added to the csv file
        csv_file = open(path.join(target_dir, name+'.csv'), 'w', newline='')
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for rownum in range(sheet.nrows):
            writer.writerow(sheet.row_values(rownum))
        csv_file.close()
    except xlrd.biffh.XLRDError:
        notifiCat.errorNotif(self, 'Not a supported file type!')
