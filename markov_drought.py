#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mks

def drought_class(df):
    #Extreme Dry (ED) - SPI <= -2.0 - index = 4
    #Severely Dry (SD) - -2.00 < SPI <= -1.50 - index = 3
    #Moderately Dry (MD) - -1.50 < SPI <= -1.0 - index = 2
    #Mild Drought - -1.00 < SPI < 0 - index = 1
    #No Drought - SPI >= 0 - index = 0

    df.loc[df >= 0] = np.int16(0)
    df.loc[(df > -1) & (df < 0)] = np.int16(1)
    df.loc[(df > -1.5) & (df <= -1.0)] = np.int16(2)
    df.loc[(df > -2) & (df <= -1.5)] = np.int16(3)
    df.loc[df <= -2] = np.int16(4)
    
    df = df.astype("int16")
    
    return df

def transition_matrix(n_class, ts):
    #ts = time series (pandas.series) não um dataframe
    #n_class = número de classes para as transições
    M = np.zeros((n_class + 1, n_class + 1))

    for i,j in zip(ts, ts[1:]):
        M[i][j] += 1
    
    M = M/M.sum(axis = 1, keepdims = True)
    #sri_p1 não ocorre classe  4 - Jogar zero para esses valores
    return M
#%%
spi_df = pd.read_csv("Dados/spi.csv", index_col = 0)
spi_df.index = pd.to_datetime(spi_df.index)
sri_df = pd.read_csv("Dados/sri.csv", index_col = 0)
sri_df.index = pd.to_datetime(sri_df.index)
#%%

spi = spi_df["Pr_index_12"]
spi_p1 = spi.loc[(spi.index.year >= 1935) & (spi.index.year <= 1984) & (spi.index.month == 12)]
spi_p2 = spi.loc[(spi.index.year >= 1985) & (spi.index.year <= 2020) & (spi.index.month == 12)]
sri = sri_df["Q_index_12"]
sri_p1 = sri.loc[(sri.index.year >= 1935) & (sri.index.year <= 1984) & (sri.index.month == 12)]
sri_p2 = sri.loc[(sri.index.year >= 1985) & (sri.index.year <= 2020) & (sri.index.month == 12)]

spi_p1 = drought_class(spi_p1)
spi_p2 = drought_class(spi_p2)
sri_p1 = drought_class(sri_p1)
sri_p2 = drought_class(sri_p2)
#%%
M_spi_p1 = transition_matrix(n_class = 4, ts = spi_p1)
M_spi_p2 = transition_matrix(n_class = 4, ts = spi_p2)
M_sri_p1 = transition_matrix(n_class = 4, ts = sri_p1)
M_sri_p2 = transition_matrix(n_class = 4, ts = sri_p2)

#%%
n_class = 4

M = np.zeros((n_class + 1, n_class + 1))


for i,j in zip(sri_p1, sri_p1[1:]):
    M[i][j] += 1

M = M/M.sum(axis = 1, keepdims = True)
#%%



# %%
