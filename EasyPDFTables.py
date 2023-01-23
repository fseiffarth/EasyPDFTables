from typing import List, Tuple

from fpdf import FPDF


def get_border(i, j, rows, cols, border_type: str = None):
    border = ''
    if type(border_type) == str:
        if border_type == 'all':
            border = 'TBLR'
        elif border_type == 'vertical':
            if j == 0:
                border += 'LR'
            else:
                border += 'R'
        elif border_type == 'horizontal':
            if i == 0:
                border += 'TB'
            else:
                border += 'B'
        elif border_type == 'box':
            if i == 0:
                border += 'T'
            if i == rows - 1:
                border += 'B'
            if j == 0:
                border += 'L'
            if j == cols - 1:
                border += 'R'
    return border


def check_table_parameter(parameter: object, name: str, rows: int, cols: int) -> str:
    input_type = 'string'
    if type(parameter) == list:
        param_rows = 1
        param_columns = 1
        input_type = 'list'
        if type(parameter[0]) == list:
            param_rows = len(parameter)
            param_cols = len(parameter[0])
            input_type = 'array'
        else:
            param_cols = len(parameter)
        if param_rows > 1:
            input_type = "array"
            if param_rows != rows:
                raise IndexError(
                    f'{name} has {param_rows} rows but should have {rows} rows!')
            for i, row in enumerate(parameter):
                if len(row) != cols:
                    raise IndexError(
                        f'Row 0 and row {i} in the table do not have the same number of columns, please fix this!')
                if len(row) != param_cols:
                    raise IndexError(
                        f'Row 0 and row {i} of the parameter do not have the same number of columns, please fix this!')
        elif param_rows == 1:
            if param_cols != cols:
                raise IndexError(
                    f'{name} has {param_cols} number of columns but needs {cols}!')
    return input_type


class EasyPDFTables(FPDF):
    def __init__(self, margins: List[float] = [0, 0, 0], font: List = ['Times', '', 10], orientation=''):
        super().__init__()

        self.set_margins(margins[0], margins[1], margins[2])
        self.set_font(font[0], font[1], font[2])
        self.orientation = orientation
        self.h_box_recursion = False
        self.current_y = 0.0
        self.add_page(self.orientation)
        self.box_splits = []
        self.y_coord = 0

        self.break_table = False

    def __y__(self) -> float:
        """
        Get the last y position in the document
        :return:
        """
        return self.y_coord[-1]

    def y_step(self, y: float = 0.0) -> float:
        """
        Get the new y position in the document
        :param y:
        :return:
        """
        return self.__y__() + y

    def make_line(self, x: float = 0.0, y: float = None, text: str = "", align='L', font_style=None, font_size=None) -> \
    List[
        float]:
        """
        Function for writing text in a pdf file
        :param x: x position of the text
        :param y: y position of the text
        :param text: text string
        :param align: alignment of the text
        :param font_style: font style of the text inside the cells choose from ['B', 'I']
        :param font_size: font size of the text inside the cells
        :return: returns the current y position in the pdf file
        """
        if y is None:
            y = self.y_coord[-1]
        return self.make_table(x=x, y=y, data=[[text]], align=align, font_style=font_style, font_size=font_size)

    def make_table(self, x: float = 0.0, y: float = None, data: List[List[str]] = [[]], border_type=None, align=None,
                   col_widths=None,
                   font_style=None,
                   font_size=None,
                   cell_borders=None, title=None, title_size=None, title_style=None, line_height=None,
                   page_break: bool = False, only_height: bool = False) -> List[float]:
        """
        Function for making pdf tables with text inside. The input data is of type List[List[str]] where the i-th entry is a list of the column values of the i-th table row.
        The parameters x,y define the upper left corner of the table on the pdf. The different parameters such as e.g. align, font, ... can be set globally via single value, columnwise
        via a list of values or for each table entry via a list of lists of values
        :param x: x position of the box
        :param y: y position of the box
        :param data: string data in list[list[]] (table) form, list of data rows
        :param border_type: set border type of the box globally with options {'all', 'vertical', 'horizontal', 'box'} or list of these options for combinations
        :param align: cell alignments choose from ['L', 'R', 'C']
        :param col_widths: width of the columns as single value for all columns or list of values
        :param font_style: font style of the text inside the cells choose from ['B', 'I']
        :param font_size: font size of the text inside the cells
        :param cell_borders: set borders of the cells individually by defining string usind charactest from ["TBLR"] for top, bottom, left and right
        :param title: set table title
        :param title_size: set table title_size
        :param title_style: set table title_style
        :param line_height: set table default line_height
        :param page_break: False normal break in table or True moves whole table to next page
        :param only_height: if true compute only height of the box without printing
        :return: list of bottom y positions of the individual rows
        """
        if y is None:
            y = self.y_coord[-1]
        if title is not None:
            y += 8.0
        row_y_positions = []

        # Check validity of input
        rows = 1
        cols = 1
        if type(data[0]) == list:
            rows = len(data)
            cols = len(data[0])
        else:
            cols = len(data)
        if rows > 1:
            for i, row in enumerate(data):
                if len(row) != cols:
                    raise IndexError(
                        f'Row 0 and row {i} in the table do not have the same number of columns, please fix this!')
        align_type = check_table_parameter(align, "align", rows, cols)
        width_type = check_table_parameter(col_widths, "col_widths", rows, cols)
        font_style_type = check_table_parameter(font_style, "font_style", rows, cols)
        font_size_type = check_table_parameter(font_size, "font_size", rows, cols)
        cell_border_type = check_table_parameter(cell_borders, "cell_borders", rows, cols)

        sum = 0
        if type(col_widths) == list:
            for x in col_widths:
                sum += x
            if sum > 1:
                raise Warning(f'The sum of column widths is {sum} but need to be less or equal to 1')
        elif type(col_widths) == int:
            sum = col_widths * cols
            if sum > 1:
                raise Warning(f'The sum of column widths is {sum} but need to be less or equal to 1')

        # Break to long h_boxes to next page
        if not self.h_box_recursion:
            self.h_box_recursion = True
            # get height of the box
            box_y_values = self.make_table(x, y, data, border_type, align, col_widths, font_style, font_size,
                                           cell_borders, title,
                                           title_size, title_style, line_height, page_break, True)

            if page_break is True and box_y_values[-1] > self.h - self.b_margin - 15:
                self.break_table = True
                self.box_splits.append(0)
            else:
                self.break_table = False
                start_value = 0
                for i, y_value in enumerate(box_y_values):
                    if y_value > self.h - self.b_margin + start_value - 15:
                        self.box_splits.append(i)
                        start_value = box_y_values[i - 1]
            self.h_box_recursion = False

        if line_height is None:
            line_height = self.font_size * 2
        split_line_height = self.font_size * 1.5
        rows = len(data)
        cols = len(data[0])
        if col_widths is None:
            col_widths = [(self.w - 2 * self.l_margin) / cols for _ in range(cols)]  # distribute content evenly
        else:
            col_widths = [(self.w - 2 * self.l_margin) * col_widths[i] for i in range(len(col_widths))]
        self.set_xy(x + self.l_margin, y)

        # Set table title
        if title is not None and not self.break_table and 0 not in self.box_splits:
            fs = self.font_size_pt
            if title_size is not None:
                self.set_font_size(title_size)
            if title_style is not None:
                self.set_font(self.font_family, title_style, self.font_size_pt)
            if not only_height:
                self.text(x + self.l_margin, y - 0.5 * self.font_size, txt=title)
            self.set_font_size(fs)
        y_val = y

        line_splits = []
        original_font_size = self.font_size_pt
        for row_num, row in enumerate(data):
            line_splits.append(1)
            for col_num, text in enumerate(row):

                # Font size
                f_size = self.font_size_pt
                if font_size_type == "string":
                    f_size = font_size
                elif font_size_type == "list":
                    f_size = font_size[col_num]
                elif font_size_type == "array":
                    f_size = font_size[row_num][col_num]

                # Font style
                if font_style is None:
                    self.set_font(self.font_family, '', f_size)
                elif font_style_type == "string":
                    self.set_font(self.font_family, font_style, f_size)
                elif font_style_type == "list":
                    self.set_font(self.font_family, font_style[col_num], f_size)
                elif font_style_type == "array":
                    self.set_font(self.font_family, font_style[row_num][col_num], f_size)

                out = len(self.multi_cell(col_widths[col_num], split_line_height, txt=text, split_only=True))
                line_splits[row_num] = max(line_splits[row_num], out)

        for row_num, row in enumerate(data):
            if row_num in self.box_splits:
                width = self.w
                if self.orientation == ('l' or 'L'):
                    width = self.h
                # self.set_xy(self.l_margin, y_val + 15)
                # self.cell(width, line_height, txt="-- Tabelle wird auf nächster Seite fortgesetzt --", border='', align='c')
                self.add_page(orientation=self.orientation)
                y_val = self.t_margin
                # Set table title
                if title and (self.break_table or 0 in self.box_splits):
                    fs = self.font_size_pt
                    if title_size is not None:
                        self.set_font_size(title_size)
                    if title_style is not None:
                        self.set_font(self.font_family, title_style, self.font_size_pt)
                    if not only_height:
                        self.text(x + self.l_margin, y_val - 0.5 * self.font_size, txt=title)
                    self.set_font_size(fs)
                # self.set_xy(self.l_margin, y_val)
                # self.multi_cell(width, line_height, txt="-- Tabelle wird auf nächster Seite fortgesetzt --", border='', align='C')
                # y_val += 15
            x_val = x + self.l_margin
            for col_num, text in enumerate(row):
                self.set_xy(x_val, y_val)

                # Border of the table
                border = ''
                if border_type is None:
                    border = get_border(row_num, col_num, len(data), len(row), border_type)
                elif cell_border_type == "string":
                    border = get_border(row_num, col_num, len(data), len(row), border_type)
                elif cell_border_type == "list":
                    for b_type in border_type:
                        border += get_border(0, col_num, len(data), len(row), b_type)
                elif cell_border_type == "array":
                    for b_type in border_type:
                        border += get_border(row_num, col_num, len(data), len(row), b_type)

                # Alignment of the text
                alignment = 'J'
                if align is None:
                    pass
                else:
                    if align_type == "string":
                        alignment = align
                    elif align_type == "list":
                        alignment = align[col_num]
                    elif align_type == "array":
                        alignment = align[row_num][col_num]

                # Font size
                f_size = self.font_size_pt
                if font_size_type == "string":
                    f_size = font_size
                elif font_size_type == "list":
                    f_size = font_size[col_num]
                elif font_size_type == "array":
                    f_size = font_size[row_num][col_num]

                # Font style
                if font_style is None:
                    self.set_font(self.font_family, '', f_size)
                elif font_style_type == "string":
                    self.set_font(self.font_family, font_style, f_size)
                elif font_style_type == "list":
                    self.set_font(self.font_family, font_style[col_num], f_size)
                elif font_style_type == "array":
                    self.set_font(self.font_family, font_style[row_num][col_num], f_size)

                if cell_border_type == "list":
                    border += cell_borders[col_num]
                if cell_border_type == "array":
                    border += cell_borders[row_num][col_num]

                splits = len(self.multi_cell(col_widths[col_num], split_line_height, txt=text, split_only=True))
                missing_cells = line_splits[row_num] - splits
                if missing_cells > 0:
                    self.set_xy(x_val, y_val + splits * split_line_height)
                    new_border = border.replace('T', '')
                    self.multi_cell(col_widths[col_num], missing_cells * split_line_height, txt='', border=new_border,
                                    align=alignment, split_only=only_height)
                    self.set_xy(x_val, y_val)
                    new_border = border.replace('B', '')
                    self.multi_cell(col_widths[col_num], split_line_height, txt=text, border=new_border,
                                    align=alignment, split_only=only_height)
                elif splits != 1:
                    self.multi_cell(col_widths[col_num], split_line_height, txt=text, border=border, align=alignment,
                                    split_only=only_height)
                else:
                    self.multi_cell(col_widths[col_num], line_height, txt=text, border=border, align=alignment,
                                    split_only=only_height)

                x_val += col_widths[col_num]
            if line_splits[row_num] == 1:
                y_val += line_splits[row_num] * line_height
            else:
                y_val += line_splits[row_num] * split_line_height
            self.set_xy(x_val, y_val)
            self.set_font(self.font_family, '', original_font_size)
            row_y_positions.append(y_val)
        self.box_splits.clear()
        self.y_coord = row_y_positions
        return row_y_positions
