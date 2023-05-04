#%%
import pandas as pd
import numpy as np
from glob import glob
# %%
list_data = [
    "BH_46902000_precip_1931-01-01_1940-12-01.csv",
    "BH_46902000_precip_1941-01-01_1950-12-01.csv",
    "BH_46902000_precip_1951-01-01_1960-12-01.csv",
    "BH_46902000_precip_1961-01-01_1970-12-01.csv",
    "BH_46902000_precip_1971-01-01_1980-12-01.csv",
    "BH_46902000_precip_1981-01-01_1990-12-01.csv",
    "BH_46902000_precip_1991-01-01_2000-12-01.csv",
    "BH_46902000_precip_2001-01-01_2010-12-01.csv",
    "BH_46902000_precip_2011-01-01_2020-12-01.csv"
]

for path_data in list_data:
    if path_data == list_data[0]:
        df = pd.read_csv(path_data, sep = ";")
    else:
        df_aux = pd.read_csv(path_data, sep = ";")
        df = df.merge(df_aux, on = ["lon", "lat"])
df = df.T
df.insert(len(df.columns), "mean", df.mean(axis = 1))
#%%
df.to_csv("BH_46902000_precip_merged.csv", sep = ";", index = True, header = True)
#%%