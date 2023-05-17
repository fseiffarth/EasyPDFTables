# EasyPDFTables
*Create your own [pdf files](Example.pdf) (with text and **tables**) using python and the fpdf package:*

* automatic line and table break
* automatic positioning of tables and text in the pdf (also custom positioning is possible)
* tables are very easy customizable (cell widths, cell borders, font size, font style)

There are only two main functions:

* **make_line(...)** generates some *single row table* consisting only of text

* **make_table(...)** generates some table using the given parameters

**See the [main.py](main.py) for a simple example with [this output](Example.pdf)**

## Install

* Clone this repository ```git clone git@github.com:fseiffarth/EasyPDFTables.git```

## Usages
* Generate nice pdf documents with numbers and information from Excel files
* Generate nice pdf documents using entries from a SQL database
* Create custom forms that include some data which can be easily accessed using python
