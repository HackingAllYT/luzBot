from matplotlib.pyplot import title
import requests
import json
import pandas as pd


def createImage(name):
    r = requests.get('https://api.esios.ree.es/archives/70/download_json')

    if r.status_code != 200:
        return
    page = r.text

    data = json.loads(page)

    info_data = []
    column_values = ['Hora', 'Precio']

    for info in data['PVPC']:
        '''aux = {
            'PCB': info['PCB'],
            'Hora': info['Hora']
        }'''
        info_data.append([int(info['Hora'].split('-')[0]),
                          float(str(info['PCB']).replace(',', '.'))])
    horas = [x for x in range(24)]

    df = pd.DataFrame(data=info_data, columns=column_values, index=horas)
    ax = df.plot(x='Hora', y='Precio', c='Precio',
                 kind='scatter', cmap='viridis', xticks=horas, title=name.split('/')[1])
    # ax = df.plot.line()
    ax.figure.set_size_inches(10, 7)
    ax.figure.savefig(name)
