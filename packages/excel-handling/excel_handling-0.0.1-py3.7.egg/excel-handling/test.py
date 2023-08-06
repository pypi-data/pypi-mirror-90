from __init__ import *

file = File('./excel.xlsx')
w, s = file.read_excel_sheet()
file.write_excel_sheet(w, s, 'A2', s['B2'].value, mode='w')
file.write_excel_sheet(w, s, 'A3', s['B3'].value, mode='a')
file.write_excel_sheet(w, s, 'A4', s['B4'].value + s['C4'].value, mode='a')
file.write_excel_sheet(w, s, 'A5', ' ' + s['B5'].value + ' ' + s['C5'].value, mode='a')
