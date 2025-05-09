import io
import json
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen.canvas import Canvas
from reportingcomponent.table.table_generator import TableGenerator

packet = io.BytesIO()
canvas = Canvas(packet, pagesize = LETTER)

configfile = 'config/temp.json'
with open(configfile) as config:
    config_data = json.load(config)

    New = TableGenerator(canvas = canvas,config = config_data)
    New.draw_table()
    y_position = New.end_points()[1]
configfile = 'config/temp_1.json'
with open(configfile) as config:
    config_data = json.load(config)
    new_config = config_data
    new_config['start_position'] = {
        'start_position_y' : y_position,
        'start_position_x' : 10
    }
    New_1 = TableGenerator(canvas = canvas,config = new_config)
    New_1.draw_table()
    y_position = New_1.end_points()[1]
configfile = 'config/temp_2.json'
with open(configfile) as config:
    config_data = json.load(config)
    new_config = config_data

    new_config['start_position'] = {
        'start_position_y' : y_position,
        'start_position_x' : 10
    }
    New_2 = TableGenerator(canvas = canvas,config = new_config)
    New_2.draw_table()
    y_position = New_2.end_points()[1]
configfile = 'config/temp_3.json'
with open(configfile) as config:
    config_data = json.load(config)
    new_config = config_data

    new_config['start_position'] = {
        'start_position_y' : y_position,
        'start_position_x' : 10
    }
    New_3 = TableGenerator(canvas = canvas,config = new_config)
    New_3.draw_table()
canvas.save()
packet.seek(0)
new_pdf = PdfReader(packet)
existing_pdf = PdfReader(
    open('reports/monthly.pdf',"rb"))
output = PdfWriter()
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
output_stream = open(os.path.join('reports/monthly_2.pdf'),"wb")
output.write(output_stream)
output_stream.close()
