#!/usr/bin/env python
# encoding: utf-8
"""
    __auth__: 孟德功
    __require__: 读去Excel
    __version__: 无要求
"""

from xlrd import open_workbook
import sys
from setting import FILES


class get_case():
    def __init__(self, module):
        self.module = module
        # self.path = sys.path[0][:-4]
        self.path = sys.path[0]

    def open_excel(self, module):
        with open_workbook(self.path + '/case/%s.xlsx' % module) as data:
            return data

    def excel_table_sheets(self, data):
        sheet_list = []
        for s in data.sheets():
            table_list = []
            for row_num in range(0, s.nrows):
                case_list = []
                row = s.row_values(row_num)
                if row:
                    for i in range(len(row)):
                        if row[i]:
                            case_list.append(row[i])
                table_list.append(case_list)
            sheet_list.append(table_list)
        return sheet_list

    def excels(self):
        lists = []
        if self.module:
            for m in self.module:
                list = self.excel_table_sheets(self.open_excel(m))
                lists = lists + list
                # with open(self.path + '/case/1.txt', 'a') as a:
                #     a.write(str(lists))
        else:
            print '请在case/setting文件中配置FILES参数!'
        return lists

        # def format_case(self):
        #     lists = []
        #     case_list = []
        #     for sheet in self.excels():
        #         for table in sheet:
        #             if table[0] == 'module':
        #                 case = []
        #                 case.append(table)
        #             case_list.append(table)
        #             print '=======',table
        # lists.append()

# get_case(FILES).format_case()
