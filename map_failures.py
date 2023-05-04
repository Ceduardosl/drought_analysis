#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
# %%
list_pluv = pd.read_csv("Dados/list_estacoes_poligonal.txt", sep = ";")
list_pluv = list_pluv.loc[list_pluv["TipoEstaca"] == 2]
list_pluv.index = list_pluv.Codigo
list_pluv.drop("Codigo", axis = 1, inplace = True)
failure_list = []
failures_list = []
#%%

# path_pluv = glob("Dados/Pluvs/*.csv")[0]
for path_pluv in glob("Dados/Pluvs/*.csv"):
    
    pluv_id = path_pluv.split("_")[-1].split(".")[0]

    pluv_data = pd.read_csv(path_pluv, index_col = 0, usecols = [1,2,3])
    pluv_data.index = pd.to_datetime(pluv_data.index)
    pluv_data.rename(columns={pluv_data.columns[0]:"Consist",
                    pluv_data.columns[1]:"Pr"}, inplace = True)

    pr_df = pd.DataFrame({"Pr": np.nan}, index = pd.date_range("01-01-1940", "31-12-2020", freq = "D"))
    raw_data = pluv_data.loc[pluv_data.Consist == 1]
    cons_data = pluv_data.loc[pluv_data.Consist == 2]

    pr_df.Pr.fillna(cons_data.Pr, inplace = True)
    pr_df.Pr.fillna(raw_data.Pr, inplace = True)

    failure_list.append([pluv_id, len(pr_df.loc[pr_df.Pr.isna()])])

#%%
failure_df = pd.DataFrame(failure_list, columns = ["Estacao", "Falhas"])
failure_df.index = failure_df.Estacao.astype(np.int64)
failure_df.drop("Estacao", axis = 1, inplace = True)
#%%
failure_df = failure_df.merge(list_pluv, left_index = True, right_index = True, how = "right")
no_data = failure_df.loc[failure_df.Falhas.isna() == True]
data_df = failure_df.loc[failure_df.Falhas.isna() == False]

#%%
fig, ax = plt.subplots(dpi = 600)
ax.scatter(data_df.Longitude, data_df.Latitude, c = data_df.Falhas)
ax.scatter(no_data.Longitude, no_data.Latitude, c = "black")