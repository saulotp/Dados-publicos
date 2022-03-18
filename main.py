# LIBRARIES
import requests
import pandas as pd


# API URL
url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?itens=1000&ordem=ASC&ordenarPor=nome'

# Request
r = requests.get(url)

# create a dataframe
df = pd.DataFrame(r.json()['dados'])

# create a new dataframe with only the column we need
df_id = df['id']


# lists to store the data and the ids
list = []
id_list = []

# request the data for each id
for id in df_id:
    url_despezas = 'https://dadosabertos.camara.leg.br/api/v2/deputados/' + \
        str(id) + '/despesas?ano=2022&itens=500&ordem=ASC&ordenarPor=ano'
    r2 = requests.get(url_despezas)
    df_despezas = pd.json_normalize(r2.json()['dados'])

    # counting how many times the ID appears
    count = len(r2.json()['dados'])

    # create a list with the ID and the number of times it appears
    for i in range(count):
        id_list.append(id)

    # create a list with the data for each ID
    list.append(df_despezas)

# create a dataframe with the data from the list
df_despezastotal = pd.concat(list)

# add the ID column to the dataframe
df_despezastotal['id'] = id_list
