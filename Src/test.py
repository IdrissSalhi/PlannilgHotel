import pathlib
import printfactory
from pychromepdf import ChromePDF
import pdfkit

content = '''
    <!doctype html>
    <html>
        <head>
            <style>
            @media print {
                @page { margin: 0; }
                body { margin: 1.6cm; }
            }
            </style>
        </head>
        <body>
            <h1>Hello, World</h1>
            <h5> Generated using headless chrome </h5>
        </body>
    </html>
    '''


pdfkit.from_file('C:/Users/idris/Desktop/PlannilgHotel-master/Logs/Factures/FactureSALHI_2023-04-17_2023-05-05.html', 'out.pdf')

"""printer = printfactory.Printer()
print_tool = printfactory.AdobeAcrobat(printer)

file = pathlib.Path("test.pdf")
print_tool.print_file(file)"""