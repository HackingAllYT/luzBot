from turtle import colormode
from matplotlib.pyplot import xticks
import requests
import re
import json
import pandas as pd
import os
import time
import stat
import datetime


r = requests.get(
    'https://api.esios.ree.es/archives/70/download_json')

# print(HTML(r.text))
page = r.text
if r.status_code != 200:
    print("Erro")

data = json.loads(page)

info_data = []
column_values = ['Hora', 'Precio']
precios = []
horas = [x for x in range(24)]

for info in data['PVPC']:
    '''aux = {
        'PCB': info['PCB'],
        'Hora': info['Hora']
    }'''
    # print(info['Dia'])
    precios.append(float(str(info['PCB']).replace(',', '.')))
    info_data.append([int(info['Hora'].split('-')[0]),
                     float(str(info['PCB']).replace(',', '.'))])

'''
precios.sort()
preciosVerdes = precios[0:8]
preciosLaranxas = precios[8:16]
preciosVermello = precios[16:24]

info_data_grn = []
info_data_ora = []
info_data_red = []

#print(preciosVerdes, preciosLaranxas, preciosVermello)
# print(precios)

for info in data['PVPC']:
    if float(str(info['PCB']).replace(',', '.')) in preciosVerdes:
        info_data_grn.append(
            [info['Hora'], float(str(info['PCB']).replace(',', '.'))])

    elif float(str(info['PCB']).replace(',', '.')) in preciosLaranxas:
        info_data_ora.append(
            [info['Hora'], float(str(info['PCB']).replace(',', '.'))])

    elif float(str(info['PCB']).replace(',', '.')) in preciosVermello:
        info_data_red.append(
            [info['Hora'], float(str(info['PCB']).replace(',', '.'))])


df_grn = pd.DataFrame(data=info_data_grn, columns=column_values)
df_ora = pd.DataFrame(data=info_data_ora, columns=column_values)
df_red = pd.DataFrame(data=info_data_red, columns=column_values)


ax = df_grn.plot(x='Hora', y='Precio', kind='scatter', color='Green')
ay = df_ora.plot(x='Hora', y='Precio', kind='scatter', color='Orange', ax=ax)
az = df_red.plot(x='Hora', y='Precio', kind='scatter', color='Red', ax=ay)

az.figure.savefig('try.pdf')
'''

df = pd.DataFrame(data=info_data, columns=column_values, index=horas)
ax = df.plot(x='Hora', y='Precio', c='Precio',
             kind='scatter', cmap='viridis', xticks=horas)
# ax = df.plot.line()
ax.figure.set_size_inches(10, 7)
ax.figure.savefig('demo-file-try.png')


fileStats = os.stat('demo-file-try.png')
modificationTime = time.ctime(fileStats[stat.ST_MTIME])
print(modificationTime)

modTimesinceEpoc = os.path.getmtime('demo-file-try.png')
modificationTime = time.strftime(
    '%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))

day = time.strftime('%d', time.localtime(modTimesinceEpoc))

print(modificationTime)
print(time.strftime('%d', time.localtime(modTimesinceEpoc)))


modTimesinceEpoc = os.path.getmtime('demo-file-try.png')
day = time.strftime('%d', time.localtime(modTimesinceEpoc))

today = datetime.datetime.now()
if int(today.day) == int(day):
    print("Mismo dia")
else:
    print(today.day, day)
