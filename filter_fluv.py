#%%
import pandas as pd 
import numpy as np
import os
from glob import glob

def daily_failure(df):
    count_daily = pd.DataFrame({"Count": df.iloc[:,0].resample("M").count()})
    count_daily.insert(len(count_daily.columns), column = "Status", value = np.nan)
    for i in range(len(count_daily)):
        if count_daily.index[i].month in [1,3,5,7,8,10,12]:
            if count_daily.iloc[i,0] < 26:
                count_daily.iloc[i, -1] = 0
            else:
                count_daily.iloc[i, -1] = 1
                
        if count_daily.index[i].month in [4,6,9,11]:
            if count_daily.iloc[i,0] < 25:
                count_daily.iloc[i, -1] = 0
            else:
                count_daily.iloc[i, -1] = 1
                
        if count_daily.index[i].month in [2]:
            if count_daily.iloc[i,0] < 24:
                count_daily.iloc[i, -1] = 0
            else:
                count_daily.iloc[i, -1] = 1
        
    # count_daily.insert(0, column = "Ano", value = count_daily.index.year)
    # count_daily.insert(1, column = "Mes", value = count_daily.index.month)
    # matrix = pd.pivot_table(data = count_daily, values = "Status", index = "Ano", columns = "Mes")

    return count_daily
#%%
# list_fluvs = glob("Dados/Fluvs/*.csv")
path_fluv = "Dados/Fluvs/3_46902000.csv"
fluv_id = path_fluv.split("_")[-1].split(".")[0]
fluv_df = pd.DataFrame(index = pd.date_range("01-01-1934", "31-12-2022", freq = "M"))
fluv_data = pd.read_csv(path_fluv, index_col = 0, usecols = [1,2,3])
fluv_data.index = pd.to_datetime(fluv_data.index)

fluv_data.rename(columns={fluv_data.columns[0]:"Consist",
                    fluv_data.columns[1]:"Q"}, inplace = True)

cons_data = fluv_data.loc[fluv_data.Consist == 2]
raw_data = fluv_data.loc[fluv_data.Consist == 1]

ts_daily = pd.DataFrame({"Q": np.nan}, index = pd.date_range("01-01-1900", "31-12-2022", freq = "D"))
ts_daily.Q.fillna(cons_data.Q, inplace = True)
ts_daily.Q.fillna(raw_data.Q, inplace = True)
ts_daily.dropna(inplace = True)
#%%
count_daily = daily_failure(ts_daily)
#%%
idx_failure = count_daily.loc[count_daily.Status == 0].index
ts_monthly = ts_daily.resample("M").mean()
ts_monthly.Q.loc[idx_failure] = np.nan

fluv_df = fluv_df.merge(ts_monthly, left_index = True, right_index = True, how = "left")
fluv_df.columns = [*fluv_df.columns[:-1], fluv_id]
fluv_df.to_excel("Dados/streamflow_data.xlsx", sheet_name = "Monthly_TS", na_rep = -999, header = True, index = True)
#%%