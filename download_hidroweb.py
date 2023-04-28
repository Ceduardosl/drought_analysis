#%%
import requests
import xml.etree.ElementTree as ET
import datetime
import calendar
import pandas as pd
import os

#Créditos das funções extract_data(), save_data() e download_hidroweb(): Duarte Jr (https://github.com/duartejr)
#https://medium.com/@duarte.jr105/download-de-dados-hidrol%C3%B3gicos-3a7bee10f868
#https://github.com/duartejr/pyHidroWeb
def extract_data(data, dataType):
    list_data = []
    list_consistenciaF = []
    list_month_dates = []

    for i in data.iter('SerieHistorica'):

        consistencia = i.find('NivelConsistencia').text
        date = i.find('DataHora').text
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        last_day = calendar.monthrange(date.year, date.month)[1]
        month_dates = [date + datetime.timedelta(days=i) for i in range(last_day)]
        content = []
        list_consistencia = []

        for day in range(last_day):

            if dataType == 3:
                value = f'Vazao{day+1:02d}'
            if dataType == 2:
                value = f'Chuva{day+1:02d}'
            
            try:
                content.append(float(i.find(value).text))
                list_consistencia.append(int(consistencia))
            except TypeError:
                content.append(i.find(value).text)
                list_consistencia.append(int(consistencia))
            except AttributeError:
                content.append(None)
                list_consistencia.append(int(consistencia))
        
        list_data += content
        list_consistenciaF += list_consistencia
        list_month_dates += month_dates

    return list_data, list_consistenciaF, list_month_dates

def save_data(data, dates, consistency, station, dataType, path_folder):
    df = pd.DataFrame({'Date': dates, 
                        f'Consistence_{dataType}_{station}':consistency,
                        f'Data{dataType}_{station}': data})
    filename = f'{dataType}_{station}.csv'
    df.to_csv(f'{path_folder}/{filename}')
    print(f'Done --> {path_folder}/{filename}\n')

def download_hidroweb(station, startDate='', endDate='', dataType='', 
                      consistencyLevel='', path_folder=os.path.expanduser('~')):
    while dataType not in [2, 3]:
        print('Especifique o tipo de dado:\n2-Chuva\n3-Vazão')
        dataType = int(input())
    params = {'codEstacao':station, 'dataInicio':startDate, 'dataFim':endDate,
              'tipoDados':dataType, 'nivelConsistencia':consistencyLevel}
    server = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica'
    response = requests.get(server, params)
    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()
    data, consistency, dates = extract_data(root, dataType)
    if len(data) > 0:
        save_data(data, dates, consistency, station, dataType, path_folder)

#%%
if __name__ == "__main__":
    list_pluvs = pd.read_csv("Dados/list_estacoes_poligonal.txt", sep = ";")
    list_pluvs = list_pluvs.loc[list_pluvs["TipoEstaca"] == 2]
    print(len(list_pluvs))
    for i in list_pluvs.Codigo:
        print(i)
        download_hidroweb(i, dataType = 2, path_folder = "{}/Dados/Pluvs".format(os.getcwd()))
    print("Finalizado")
        
# %%
