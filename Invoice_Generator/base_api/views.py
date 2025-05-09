from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import io
import json
import os
import sys
import pandas as pd
sys.path.append('/reportingcomponent')
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen.canvas import Canvas
from django.http import FileResponse, HttpResponse
import inflect
from reportingcomponent.table.table_generator import TableGenerator

class InvoiceGeneratorView(APIView):
    def post(self, request):
        api_data = request.data
        data = pd.DataFrame(api_data['items'])
        data.insert(0, 'ID', data.index + 1)
        data['Taxable_Amount'] = round(data['rate'].astype(float)*data['qtyUnit'].astype(float) - data['discount'].astype(float),2)
            # round(float(data['rate']) * float(data['qtyUnit']) - float(data['discount']), 2)
        data['Total_Sale'] = round(data['rate'].astype(float) * data['qtyUnit'].astype(float), 2)
        data['Total_Tax'] = round(data['Taxable_Amount'].astype(float) * (
                    data['cgst'].astype(float) / 100 +  data['igst'].astype(float) / 100 + data['sgst'].astype(float) / 100), 2)
        data['Total_Amount'] = data['Taxable_Amount'] + data['Total_Tax']
        packet = io.BytesIO()
        canvas = Canvas(packet, pagesize=LETTER)

        configfile = 'config/temp.json'
        with open(configfile) as config:
            config_data = json.load(config)
            config_data["data"][1][0] = "Date: "+ api_data['formdata']['date']
            config_data["data"][1][1] = "Invoice No.: "+ api_data['formdata']['invoice_no']
            config_data["data"][3][1] = api_data['formdata']['company_name']
            config_data["data"][4][1] = "Address: " + api_data['formdata']['address']
            config_data["data"][5][1] = "Phone No.: " + api_data['formdata']['phone']
            config_data["data"][6][1] = "GSTIN: " + api_data['formdata']['gstin']
            New = TableGenerator(canvas=canvas, config=config_data)
            New.draw_table()
            y_position = New.end_points()[1]
        configfile = 'config/temp_1.json'
        with open(configfile) as config:
            config_data = json.load(config)
            new_config = config_data
            temp_data = config_data['data'].copy()
            temp_data  = temp_data + data[["ID","description","hsnCode","itemCode","qtyUnit","rate","Total_Sale","discount","Taxable_Amount"]].values.tolist()
            config_data['data'] = temp_data
            print(config_data['data'])
            new_config['start_position'] = {
                'start_position_y': y_position,
                'start_position_x': 10
            }
            New_1 = TableGenerator(canvas=canvas, config=new_config)
            New_1.draw_table()
            y_position = New_1.end_points()[1]
        configfile = 'config/temp_2.json'
        with open(configfile) as config:
            config_data = json.load(config)
            new_config = config_data
            print(data)
            data['cgst'] = round(data['cgst'],2)+ '%'
            data['sgst'] = round(data['sgst'], 2) + '%'
            data['igst'] = round(data['igst'], 2) + '%'
            temp_data = new_config['data'][0:2].copy() + data[["ID","Taxable_Amount","sgst","cgst","igst","Total_Tax","Total_Amount"]].values.tolist() + new_config['data'][-2:].copy()
            new_config['data'] = temp_data
            p = inflect.engine()
            total_bill = sum(data[["Total_Amount"]].values.tolist()[0])
            new_config['data'][-2][0] = "Total: "+f"{total_bill:,}"+ "/-<br/>("+p.number_to_words(total_bill)+" Rupees Only)"
            new_config['start_position'] = {
                'start_position_y': y_position,
                'start_position_x': 10
            }
            New_2 = TableGenerator(canvas=canvas, config=new_config)
            New_2.draw_table()
            y_position = New_2.end_points()[1]
        configfile = 'config/temp_3.json'
        with open(configfile) as config:
            config_data = json.load(config)
            new_config = config_data

            new_config['start_position'] = {
                'start_position_y': y_position,
                'start_position_x': 10
            }
            New_3 = TableGenerator(canvas=canvas, config=new_config)
            New_3.draw_table()
        canvas.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        existing_pdf = PdfReader(
            open('reports/monthly.pdf', "rb"))
        output = PdfWriter()
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        output_stream = open(os.path.join('reports/monthly_4.pdf'), "wb")
        final_buffer = io.BytesIO()
        output.write(final_buffer)
        final_buffer.seek(0)

        return HttpResponse(
            final_buffer.getvalue(),
            content_type='application/pdf',
            headers={'Content-Disposition': 'attachment; filename="invoice.pdf"'}
        )