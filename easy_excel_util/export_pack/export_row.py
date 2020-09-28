# !user/bin/env python3
# -*- coding: utf-8 -*-
# Author: ChaoqiYin
from .export_cell import ExportCell


class ExportRow(object):
    def __init__(self, export_sheet, row_num, row_data):
        '''
        init
        :param export_sheet: ExportSheet实例
        :param row_num: 当前行数，从0开始
        :param row_data: 当前行数据
        '''
        self.export_sheet = export_sheet
        self.row_num = row_num
        self.row_data = row_data

    @property
    def sheet(self):
        return self.export_sheet.work_sheet

    @property
    def parse_map(self):
        '''
        获取解析字段的map映射
        :return:
        '''
        return self.export_sheet.parse_map

    def set_row_height(self):
        '''
        设置行高
        :param row_num:
        :return:
        '''
        row_height_base = self.export_sheet.sheet_map.row_height or 40
        self.sheet.row(self.row_num).height_mismatch = True
        self.sheet.row(self.row_num).height = 20 * row_height_base  # 20为基准数，默认40高

    def write_title(self):
        '''
        写入title数据
        :return:
        '''
        self.set_row_height()
        for export_field_name, export_field in self.parse_map.items():
            ExportCell(self, export_field.name, export_field).write_title_cell()

    def write_row(self):
        '''
        写入行数据, 合并相同单元格
        :return:
        '''
        self.set_row_height()
        for export_field_name, export_field in self.parse_map.items():
            # 取值，分为对象或字典
            value = None
            if hasattr(self.row_data, export_field_name):
                value = getattr(self.row_data, export_field_name)
            elif isinstance(self.row_data, dict) and self.row_data.__contains__(export_field_name):
                value = self.row_data.get(export_field_name)
            if value is not None:
                cell = ExportCell(self, value, export_field).write_cell()
                if export_field.merge_same is True:
                    # 获取该列索引，查找相邻且数据相同的值
                    index = export_field.index
                    self.export_sheet.add_col_data_to_map(index, self.row_num, cell['value'], cell['style'])