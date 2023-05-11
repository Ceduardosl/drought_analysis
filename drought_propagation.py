#métrica para avaliar a propagação de seca meteorológica para hidrológica
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, pearsonr
from collections import namedtuple
import scipy.stats as sc

def correl_indexes(x,y):
    corr_list = list()
    for i in range(1,12+1):
        corr_list.append([i,spearmanr(x.iloc[:,i],y)[0], spearmanr(x.iloc[:,i],y)[1]])
        # corr_list.append([i,pearsonr(x.iloc[:,i],y)[0], pearsonr(x.iloc[:,i],y)[1]])
    corr_df = pd.DataFrame(corr_list, columns = ["scale", "correl", "p-value"])
    return corr_df
#%%
spi_df = pd.read_csv("Dados/spi.csv", index_col = 0)
sri_df = pd.read_csv("Dados/sri.csv", index_col = 0)
spei_df = pd.read_csv("Dados/spei.csv", index_col = 0)

spi_df.index = pd.to_datetime(spi_df.index)
sri_df.index = pd.to_datetime(sri_df.index)
spei_df.index = pd.to_datetime(spei_df.index)

spi_df = spi_df.iloc[:,::2]
sri_df = sri_df.iloc[:,::2]
spei_df = spei_df.iloc[:,::2]

p1 = [1935, 1994]
p2 = [1995, 2020]

spi_p1 = spi_df.loc[(spi_df.index.year >= p1[0]) & (spi_df.index.year <= p1[1])]
spi_p2 = spi_df.loc[(spi_df.index.year >= p2[0]) & (spi_df.index.year <= p2[1])]

sri_p1 = sri_df["Q_index_1"].loc[(sri_df.index.year >= p1[0]) & (sri_df.index.year <= p1[1])]
sri_p2 = sri_df["Q_index_1"].loc[(sri_df.index.year >= p2[0]) & (sri_df.index.year <= p2[1])]

spei_p1 = spei_df.loc[(spei_df.index.year >= p1[0]) & (spei_df.index.year <= p1[1])]
spei_p2 = spei_df.loc[(spei_df.index.year >= p2[0]) & (spei_df.index.year <= p2[1])]
    
corr_spi_p1 = correl_indexes(spi_p1, sri_p1)
corr_spi_p2 = correl_indexes(spi_p2, sri_p2)
corr_spei_p1 = correl_indexes(spei_p1, sri_p1)
corr_spei_p2 = correl_indexes(spei_p2, sri_p2)
#%%
#3 meses foi o tempo de propagação da seca meteorológica para hidrológica
spi_p1 = spi_p1["Pr_index_3"]
spi_p2 = spi_p2["Pr_index_3"]
spei_p1 = spei_p1["wb_index_3"]
spei_p2 = spei_p2["wb_index_3"]

#%%
count_d = 0
list_d = []
for i in range(len(sri_p1)):
    print(sri_p1.iloc[i])
    if sri_p1.iloc[i] < 0:
        end_d = sri_p1.index[i]
        count =+ 1
        if sri_p1.iloc[i+1] >= 0:
            end_d = sri_p1.index[i]
            list_d.append([end_d, count])
    else:
        list_d.append([end_d, count])
        count = 0
# %%
