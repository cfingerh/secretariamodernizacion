from load import *
from base.models import *


import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('ResumenGenerado.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
expenses = (
    ['Rent', 1000],
    ['Gas', 100],
    ['Food', 300],
    ['Gym', 50],
)

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

for anio in [2015, 2016, 2017, 2018, 2019, 2020]:
    col = (anio - 2015) * 6
    worksheet.write(row, col + 1, anio)
    worksheet.write(row, col + 2, anio)
    worksheet.write(row, col + 3, anio)
    worksheet.write(row, col + 4, anio)
    worksheet.write(row, col + 5, anio)
    worksheet.write(row, col + 6, anio)
    worksheet.write(row + 1, col + 1, 'eval positivo')
    worksheet.write(row + 1, col + 2, 'eval negativo')
    worksheet.write(row + 1, col + 3, 'eval neutro')
    worksheet.write(row + 1, col + 4, 'experiencia positivo')
    worksheet.write(row + 1, col + 5, 'experiencia negativo')
    worksheet.write(row + 1, col + 6, 'experiencia neutro')

row = 1
for institucion in Institucion.objects.all().order_by('nombre'):
    row += 1
    worksheet.write(row, 0, institucion.nombre)
    anios_existentes = [a.get("anio") for a in institucion.resumen.get("anios")]
    for anio in [2015, 2016, 2017, 2018, 2019, 2020]:
        if anio in anios_existentes:
            col = (anio - 2015) * 6
            dato = [a for a in institucion.resumen.get("anios") if a.get("anio") == anio][0]
            worksheet.write(row, col + 1, dato.get("eval_inst").get("positivo"))
            worksheet.write(row, col + 2, dato.get("eval_inst").get("negativo"))
            worksheet.write(row, col + 3, dato.get("eval_inst").get("neta"))
            worksheet.write(row, col + 4, dato.get("experiencia").get("positivo"))
            worksheet.write(row, col + 5, dato.get("experiencia").get("negativo"))
            worksheet.write(row, col + 6, dato.get("experiencia").get("neta"))

workbook.close()
