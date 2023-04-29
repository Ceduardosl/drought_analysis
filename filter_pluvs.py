#Algoritmo para filtrar os pluvs sem falhas
#%%
import pandas as pd
import numpy as np
from glob import glob
import os

def daily_failure_matrix(df):
    count_daily = pd.DataFrame({"Count": df.iloc[:,1].resample("M").count()})
    count_daily.insert(len(count_daily.columns), column = "Status", value = np.nan)
    for i in range(len(count_daily)):
        if count_daily.index[i].month in [1,3,5,7,8,10,12]:
            if count_daily.iloc[i,0] < 28:
                count_daily.iloc[i, -1] = 0
            else:
                count_daily.iloc[i, -1] = 1
                
        if count_daily.index[i].month in [4,6,9,11]:
            if count_daily.iloc[i,0] < 27:
                count_daily.iloc[i, -1] = 0
            else:
                count_daily.iloc[i, -1] = 1
                
        if count_daily.index[i].month in [2]:
            if count_daily.iloc[i,0] < 26:
                count_daily.iloc[i, -1] = 0
            else:
                count_daily.iloc[i, -1] = 1
        
    count_daily.insert(0, column = "Ano", value = count_daily.index.year)
    count_daily.insert(1, column = "Mes", value = count_daily.index.month)
    matrix = pd.pivot_table(data = count_daily, values = "Status", index = "Ano", columns = "Mes")
    
    return matrix

#%%
list_pluvs = glob("Dados/Pluvs/*.csv")

path_pluv = list_pluvs[153]

pluv_data = pd.read_csv(path_pluv, index_col = 0, usecols = [1,2,3])
pluv_data.index = pd.to_datetime(pluv_data.index)
pluv_data.rename(columns={pluv_data.columns[0]:"Consist",
                          pluv_data.columns[1]:"Pr"}, inplace = True)

ts_daily = pd.DataFrame(index = pd.date_range("01-01-1985", "31-12-2022", freq = "D"))


#%%
if (pluv_data.index.year.min() <= 1985) & (pluv_data.index.year.max() >= 2014):
    #garanti no mínimo 30 anos
    failure_matrix = daily_failure_matrix(pluv_data)
else:
    print("Fora")
#     break
#%%
count_daily = pd.DataFrame({"Count": pluv_data.iloc[:,1].resample("M").count()})
count_daily.insert(len(count_daily.columns), column = "Status", value = np.nan)
count_daily.iloc[i,0]
#%%
for i in range(len(count_daily)):
    if count_daily.index[i].month in [1,3,5,7,8,10,12]:
        if count_daily.iloc[i,0] < 28:
            count_daily.iloc[i, -1] = 0
        else:
            count_daily.iloc[i, -1] = 1
                
    if count_daily.index[i].month in [4,6,9,11]:
        if count_daily.iloc[i,0] < 27:
            count_daily.iloc[i, -1] = 0
        else:
            count_daily.iloc[i, -1] = 1
                
    if count_daily.index[i].month in [2]:
        if count_daily.iloc[i,0] < 26:
            count_daily.iloc[i, -1] = 0
        else:
            count_daily.iloc[i, -1] = 1
        
count_daily.insert(0, column = "Ano", value = count_daily.index.year)
count_daily.insert(1, column = "Mes", value = count_daily.index.month)
matrix = pd.pivot_table(data = count_daily, values = "Status", index = "Ano", columns = "Mes")
    