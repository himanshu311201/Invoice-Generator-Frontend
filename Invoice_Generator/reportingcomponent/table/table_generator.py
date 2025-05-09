import copy

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle,Paragraph
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.enums import TA_RIGHT,TA_CENTER,TA_LEFT,TA_JUSTIFY

import re
class TableGenerator:
    write_canvas = True

    def __init__(self, canvas, config):
        self._config = config
        self._canvas = canvas
        self._start_position = dict()
        if 'start_position' in config:
            self._start_position['start_position_x'] = config['start_position']['start_position_x']
            self._start_position['start_position_y'] = config['start_position']['start_position_y']
        else:
            self._start_position['start_position_x'] = 10
            self._start_position['start_position_y'] = 0
        self._formatting = config['formatting'] if 'formatting' in config else None
        self._data = self._config['data']
        for row in range(len(self._data)):
            for column in range(len(self._data[0])):
                    self._data[row][column] = str(self._data[row][column])
        self.formatted_data = copy.deepcopy(self._data)
        if self._formatting is not None:
            self.convert_paragraph()
        for row in range(len(self._data)):
            for column in range(len(self._data[0])):
                if isinstance(self._data[row][column],Paragraph) is False:
                    self._data[row][column] = Paragraph(self._data[row][column])
        self._col_width = None
        if 'column_width' in config:
            self._col_width = config['column_width']
            self._table = Table(
                data=self._data,
                colWidths=self._col_width
                )
        else:
            self._table = Table(
                data=self._data,
            )
        if self._formatting is not None:
            self.merge_cells()
            self.apply_borders()
            if 'general_style' in self._formatting and 'border' in self._formatting['general_style'] and self._formatting['general_style']['border'] ==1:
                self._table.setStyle(
                    TableStyle(
                        [
                            ('LINEBELOW', (0, -1), (-1, -1), 0.5, "#000000"),
                            ('LINEBELOW', (0, 0), (-1, 0), 0.5, "#000000"),
                            ('LINEBELOW', (0, -1), (-1, -1), 0.5,"#000000"),
                            ('LINEAFTER', (0, 0), (-1, -1), 0.5,"#000000"),
                            ('LINEBEFORE', (0, 0), (-1, -1), 0.5, "#000000"),
                            # ('LINEBEFORE', (0, 0), (-1, -1), 0.5,"#000000"),
                            # ('LINEABOVE', (0, 0), (-1, -1), 0.5,"#000000")
                        ]
                    )
                )
        self._table.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (0,0), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 0)
        ]))


    def end_points(self):
        w,h = self._table.wrap(0,0)
        return self._start_position['start_position_x']+ w,h+self._start_position['start_position_y']

    def merge_cells(self):
        merge_config = self._formatting.get('cell_mergers')
        if not merge_config:
            return
        for row_key, mergers in merge_config.items():
            row_index = int(row_key)
            for start_col, end_col in mergers:
                start_cell = (start_col, row_index)
                end_cell = (end_col, row_index)

                # Apply both SPAN and ALIGN styles
                self._table.setStyle(TableStyle([
                    ('SPAN', start_cell, end_cell),
                    ('ALIGN', start_cell, end_cell, 'CENTER'),
                    ('VALIGN',start_cell, end_cell,'MIDDLE'),
                    ('HALIGN',start_cell,end_cell,'CENTER')
                ]))
    def apply_borders(self):
        border_config = self._formatting.get('border')
        if border_config is not None:
            for border in border_config:
                border_type = "LINE" + border["type"]
                border_color = colors.HexColor(border['color'])
                border_width = float(border['width'])
                self._table.setStyle(
                    TableStyle(
                        [
                        (border_type,tuple(border['point_start']),tuple(border['point_end']),border_width,border_color)
                            ]
                    )
                )
    def convert_paragraph(self):
        text_config = self._formatting.get('text_formatting')
        align_config = self._formatting.get('align_column')
        merge_config = self._formatting.get('cell_mergers')
        general_style = self._formatting.get('general_style')

        #providing static configuration
        font_type_general = general_style['fontFamily'] if  general_style is not None and 'fontFamily' in general_style else 'Helvetica'
        font_size_general = float(general_style['fontSize']) if general_style is not None and 'fontSize' in general_style else 10.0
        font_color_general = general_style['fontColor'] if general_style is not None and 'fontColor' in general_style is not None else "#000000"
        background_color_general = general_style['backgroundColor'] if general_style is not None and 'backgroundColor' in general_style else "#ffffff"
        h_align_general = general_style['hAlign'] if general_style is not None and 'hAlign' in general_style else 'LEFT'
        v_align_general = general_style['vAlign'] if general_style is not None and 'vAlign' in general_style else 'BOTTOM'

        if text_config is None:
            return
        #row formatting in text_config
        for text_style in text_config:
            y = text_style['number']
            x_start = text_style['column'][0]
            x_end = text_style['column'][1]
            for x in range(x_start,x_end):
                if len(self._data[y])> x and isinstance(self._data[y][x],Paragraph) is not True and len(self._data[y][x])>=1:
                    self._data[y][x] = '<b>' + self._data[y][x] + '</b>' if 'bold' in text_style and text_style['bold'] == '1' else self._data[y][x]
                    self._data[y][x] = '<u>' + self._data[y][x] + '</u>' if 'underline' in text_style and text_style[
                        'underline'] == '1' else self._data[y][x]
                    self._data[y][x] = '<i>' + self._data[y][x] + '</i>' if 'italic' in text_style and text_style[
                        'italic'] == '1' else self._data[y][x]
                    font_type = text_style['fontType'] if text_style is not None and 'fontType' in text_style else font_type_general
                    font_size = float(text_style['fontSize']) if text_style is not None and 'fontSize' in text_style else font_size_general
                    font_color = text_style['fontColor'] if text_style is not None and 'fontColor' in text_style else font_color_general
                    background_color = text_style[
                        'backgroundColor'] if text_style is not None and 'backgroundColor' in text_style else background_color_general
                    h_align = text_style['hAlign'] if text_style is not None and 'hAlign' in text_style else h_align_general
                    v_align = text_style['vAlign'] if text_style is not None and 'vAlign' in text_style else v_align_general
                    paragraph_style = ParagraphStyle(
                        name = "default",
                        fontName = font_type,
                        fontSize = font_size,
                        alignment = eval('TA_'+str(h_align)),
                        leading = 12,
                        textColor = font_color,
                        backColor = background_color
                    )
                    if isinstance(self._data[y][x],Paragraph) is not True:
                        self._data[y][x] = Paragraph(self._data[y][x],paragraph_style)






    def draw_table(self,column_width=None):
        if column_width != None:
            self._col_width = column_width
            self._table._argW = self._col_width
            self._table._seqCW = self._col_width
        elif self._col_width == None:
            self._col_width = self.get_column_width(True)['column_width']
            self._table._argW = self._col_width
        self._table.wrapOn(self._canvas,550,550)
        w,h = self._table.wrap(550,550)
        self._table.drawOn(self._canvas,self._start_position['start_position_x'],
                          LETTER[1] -h- self._start_position['start_position_y']
                           )
    def get_column_width(self,individual= False):
        column_width = [0 for i in range(len(self._data[0]))]
        max_depth = 1
        max_row_width = self._formatting.get('general_style').get('row_width')
        total_column_width = self._formatting.get('general_style').get('total_width')
        offset = 15
        for columns in range(2,len(self._data[0])):
            column_width[columns] = 0
            for rows in range(0,len(self._data)):
                for text_value in re.split(' ',self.formatted_data[rows][columns]):
                    if text_value is not None and len(text_value)>=1 and isinstance(self._data[rows][columns],Paragraph):
                        column_width[columns] = max(column_width[columns],
                                                    max(
                                                        round(self.calculate_width_of_string(text_value,self._data[rows][columns].style.fontName,self._data[rows][columns].style.fontSize),3)+offset,
                                                            12))
            if column_width[columns]<=0:
                column_width[columns] = 5
        column_width[0] = 42
        column_width[1] = round(total_column_width-sum(column_width))
        if column_width[1] >max_row_width:
            difference = column_width[1] - max_row_width
            for index in range(2,len(column_width)):
                column_width[index] += (difference)/(len(column_width)-2)
                column_width[1] -= (difference)/(len(column_width) -2)
        return {'column_width':column_width}
    @staticmethod
    def calculate_width_of_string(character_list:str,font_name:str,font_size:int):
        width = 0
        width = pdfmetrics.stringWidth(character_list,font_name,font_size)
        return width


