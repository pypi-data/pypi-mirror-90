from openpyxl import load_workbook

class File:
    def __init__(self, filename):
        self.filename = filename

    def read_excel_sheet(self):
        workbook = load_workbook(filename=self.filename)
        sheet = workbook.active
        return workbook, sheet

    def write_excel_sheet(self, workbook, sheet, coordinate, change_info, mode='w'):
        if mode == 'w':
            sheet[coordinate].value = str(change_info)
        elif mode == 'a':
            sheet[coordinate].value = str(sheet[coordinate].value) + change_info
        else:
            raise ValueError(f'mode error: \'{mode}\'')
        workbook.save(filename=self.filename)
        return sheet

