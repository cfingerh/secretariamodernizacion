# import pandas as pd
# import pyreadstat
# file="/home/christian/repo/hacienda/satisfaccion2021/s3/metodologia/2020_Bases_SPSS/2020_ESU_FONASA.sav"
# df,meta = pd.read_spss(file)


# items = []

# df, meta= pyreadstat.read_sav(file)

# for index, columna in enumerate(meta.column_names):

#     item = {
#         'descripcion':meta.column_names_to_labels[columna],
#         'nombre':columna,
#         'label':meta.column_labels[index]
#     }

#     if columna in meta.variable_to_label.keys():
#         item["valores"] =meta.value_labels[meta.variable_to_label[columna]]

#     items.append(item)

# import json
# with open("columnas2.json", "w") as write_file:
#     json.dump(items, write_file, indent=4, ensure_ascii=False)


from openpyxl import Workbook
import json
# Python program to read
# json file


import json
f = open('columnas2.json',)
items = json.load(f)

wb = Workbook()


ws = wb.active

for row, item in enumerate(items):
    for column, col in enumerate(['nombre', 'label', 'descripcion', 'valores', 'pendiente', 'pendiente2','tipo']):
        value = item.get(col)
        if type(value) is dict:
            value = json.dumps(value, ensure_ascii=False)

        d = ws.cell(row=row + 1, column=column + 1, value=value)

wb.save('columns.xlsx')
