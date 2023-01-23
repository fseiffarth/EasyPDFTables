# This is an example to demonstrate the usage of the class EasyFPDFTables.
from EasyPDFTables import EasyPDFTables


def main():
    font_type = 'Times'
    margins = [20.0, 25.0, 20.0]
    font = [font_type, '', 10]
    # Initialize the pdf file defining the margins and the font
    pdf = EasyPDFTables(margins, font)

    # Make some lines
    pdf.make_line(0.0, pdf.t_margin, text="Easy PDF Tables", align='C', font_style='B', font_size=20)
    pdf.make_line(0.0, pdf.y_step(8.0), text="an example for easily generating nice pdf tables with python. You only "
                                             "need the package fpdf", align='C', font_style='I', font_size=15)
    pdf.make_line(0.0, pdf.y_step(8.0), text="Here we start with some examples:", font_size=12)

    # A table where all borders are included
    data = [['This', 'sentence', 'can', 'be', 'replaced', 'by', 'your', 'data', '.'],
            ['And', 'more', 'and', 'more', 'and', 'more', 'and', 'more', 'data']]
    pdf.make_table(data=data, border_type='all', title='Table with a bold title and all borders',
                   title_size=10, title_style='B', font_size=8)

    # A box table
    data = [['This', 'sentence', 'can', 'be', 'replaced', 'by', 'your', 'data', '.'],
            ['And', 'more', 'and', 'more', 'and', 'more', 'and', 'more', 'data']]
    pdf.make_table(0.0, pdf.y_step(10), data, border_type='box',
                   title='You can also generate a table with only a box as border and normal title',
                   title_size=10, title_style='', font_size=8)

    # A box table
    data = [['This', 'sentence', 'can', 'be', 'replaced', 'by', 'your', 'data', '.'],
            ['And', 'more', 'and', 'more', 'and', 'more', 'and', 'more', 'data']]
    pdf.make_table(0.0, pdf.y_step(10), data, border_type='horizontal',
                   title='A table with horizontal borders and italic title',
                   title_size=10, title_style='I', font_size=8)

    # A box table
    data = [['This', 'sentence', 'can', 'be', 'replaced', 'by', 'your', 'data', '.'],
            ['And', 'more', 'and', 'more', 'and', 'more', 'and', 'more', 'data']]
    pdf.make_table(0.0, pdf.y_step(10), data, border_type='vertical',
                   title='A table with vertical borders and customized column widths',
                   title_size=10, title_style='B', font_size=8,
                   col_widths=[0.07, 0.11, 0.29, 0.05, 0.1, 0.1, 0.1, 0.1, 0.08])

    # Customized table
    data = [['This', 'sentence', 'can', 'be', 'replaced', 'by', 'your', 'data', '.'],
            ['And', 'more', 'and', 'more', 'and', 'more', 'and', 'more', 'data']]
    align = ['R', 'C', 'L', 'C', 'L', 'C', 'L', 'C', 'R']
    font_style = ['B', 'I', '', '', 'B', 'I', '', 'I', 'B']
    font_size = [[8, 10, 8, 4, 6, 8, 6, 9, 8],
                 [8, 6, 8, 4, 8, 3, 6, 10, 6]]
    cell_borders = [['', 'LBR', 'T', 'B', '', 'RL', '', '', 'TR'], ['', 'LBR', 'T', 'B', '', 'RL', '', '', 'TR']]
    pdf.make_table(0.0, pdf.y_step(10), data, align=align,
                   title='Or make a fully customized table with different borders, alignments, font styles and font sizes',
                   title_size=10, title_style='B', font_size=font_size, font_style=font_style,
                   cell_borders=cell_borders,
                   col_widths=[0.07, 0.11, 0.29, 0.05, 0.1, 0.1, 0.1, 0.1, 0.08])

    row = [str(i) for i in range(10)]
    data = [row for _ in range(25)]
    pdf.make_table(0.0, pdf.y_step(10), data, border_type='all',
                   title='The class automatically breaks large tables',
                   title_size=10, title_style='B', font_size=8)

    row = [str(i) for i in range(10)]
    data = [row for _ in range(25)]
    pdf.make_table(0.0, pdf.y_step(10), data, border_type='all',
                   title='Or the class automatically shifts a table to the next page if you do not want to break the table into pieces',
                   title_size=10, title_style='B', font_size=8, page_break=True)

    pdf.output('Example.pdf')


if __name__ == '__main__':
    main()
