#Algoritmo para filtrar os pluvs sem falhas
#%%
import pandas as pd
import numpy as np
from glob import glob
import os

def daily_failure(df):
    count_daily = pd.DataFrame({"Count": df.iloc[:,0].resample("M").count()})
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
        
    # count_daily.insert(0, column = "Ano", value = count_daily.index.year)
    # count_daily.insert(1, column = "Mes", value = count_daily.index.month)
    # matrix = pd.pivot_table(data = count_daily, values = "Status", index = "Ano", columns = "Mes")

    return count_daily

#%%
list_pluvs = glob("Dados/Pluvs/*.csv")
pr_df = pd.DataFrame(index = pd.date_range("01-01-1985", "31-12-2021", freq = "M"))
# path_pluv = list_pluvs[153]
count = 0
for path_pluv in list_pluvs:
    pluv_id = path_pluv.split("_")[-1].split(".")[0]
    pluv_data = pd.read_csv(path_pluv, index_col = 0, usecols = [1,2,3])

    pluv_data.index = pd.to_datetime(pluv_data.index)
    pluv_data.rename(columns={pluv_data.columns[0]:"Consist",
                            pluv_data.columns[1]:"Pr"}, inplace = True)
    raw_data = pluv_data.loc[pluv_data.Consist == 1]
    cons_data = pluv_data.loc[pluv_data.Consist == 2]

    ts_daily = pd.DataFrame({"Pr": np.nan}, index = pd.date_range("01-01-1985", "31-12-2021", freq = "D"))
    ts_daily.Pr = ts_daily.Pr.fillna(cons_data.Pr)
    ts_daily.Pr = ts_daily.Pr.fillna(raw_data.Pr)
    ts_daily = ts_daily.dropna()

    if (ts_daily.index.year.min() <= 1985) & (ts_daily.index.year.max() >= 2014):
        #garanti no mínimo 30 anos
        # failure_matrix = daily_failure(ts_daily)[0]
        count_daily = daily_failure(ts_daily)
        idx_failure = count_daily.loc[count_daily.Status == 0].index
        # failure_matrix.insert(len(failure_matrix.columns), "check", failure_matrix.sum(axis = 1))
        if count_daily.resample("Y").sum().Status.min() >= 10:
            count += 1
            print("Estação Aprovada - {}".format(pluv_id))
            # failure_matrix.to_csv("Dados/Pluvs/Failure_Matrix/FM_{}.csv".format(pluv_id))
            ts_monthly = ts_daily.resample("M").sum()
            ts_monthly.Pr.loc[idx_failure] = np.nan
            ts_monthly.to_csv("Dados/Pluvs/Monthly_Pr/{}.csv".format(pluv_id))
            pr_df = pr_df.merge(ts_monthly, left_index = True, right_index = True, how = "left")
            pr_df.columns = [*pr_df.columns[:-1], pluv_id]
        else:
            print("Estação Descartada - {}".format(pluv_id))
    else:
        print("Estação {} sem dados no período".format(pluv_id))
pr_df.to_excel("Dados/filtered_pluvs.xlsx", sheet_name = "Monthly_TS", na_rep = -999, header = True, index = True)
# pr_df.to_excel("Dados/filtered_pluvs.csv")
print("{} Aprovados".format(count))
print("### Finalizado ####")
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
    