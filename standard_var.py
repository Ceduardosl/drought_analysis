#%%
import pandas as pd
import standard_precip as spr
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as sc

def spi_calculate (var, window, var_name, distr = "gamma"):

    x = var.rolling(window = window).sum()

    df = pd.DataFrame({
        "{}".format(var_name): var,
        "{}_acc_{}".format(var_name, window): x,
        "{}_index_{}".format(var_name, window): np.nan})

    x = np.array(x)
    x = x[~np.isnan(x)]
    
    if distr == "gamma":
        q = len(np.where(x == 0)[0])/(len(x))
        x_nozero = x[x  > 0]
        params_fit = sc.gamma.fit(x_nozero, floc = 0)
        prob_acc = q + (1-q)*sc.gamma.cdf(x, *params_fit)
    
    if distr == "pearson3":
        params_fit = sc.pearson3.fit(x)
        prob_acc = sc.pearson3.cdf(x, *params_fit)
    
    if distr == "logistic":
        params_fit = sc.logistic.fit(x)
        prob_acc = sc.logistic.cdf(x, *params_fit)

    df["{}_index_{}".format(var_name, window)][(window-1):] = sc.norm.ppf(prob_acc, loc = 0, scale = 1)

    return df
        

#%%
if __name__ == '__main__':
    data_EPQ = pd.read_excel("Dados/Dataset_EPQ.xlsx", sheet_name = "EPQ", index_col = 0)
    #wb é o "water balance" entre precipitação e ETP
    data_EPQ.insert(len(data_EPQ.columns), "wb", data_EPQ.Pr - data_EPQ.ETP)
    for i in range(1, 12+1):
        if i == 1:
            spi_df = spi_calculate(data_EPQ.Pr, window = i, var_name = "Pr", distr = "gamma")
            sri_df = spi_calculate(data_EPQ.Q, window = i, var_name = "Q", distr = "gamma")
            spei_df = spi_calculate(data_EPQ.wb, window = i, var_name = "wb", distr = "pearson3")
        else:
            spi = spi_calculate(data_EPQ.Pr, window = i, var_name = "Pr", distr = "gamma")
            sri = spi_calculate(data_EPQ.Q, window = i, var_name = "Q", distr = "gamma")
            spei = spi_calculate(data_EPQ.wb, window = i, var_name = "wb", distr = "pearson3")
            spi_df = spi_df.merge(spi.iloc[:,1:], left_index = True, right_index = True)
            sri_df = sri_df.merge(sri.iloc[:,1:], left_index = True, right_index = True)
            spei_df = spei_df.merge(spei.iloc[:,1:], left_index = True, right_index = True)

    spi_df.to_csv("Dados/spi.csv", index = True, header = True)
    sri_df.to_csv("Dados/sri.csv", index = True, header = True)
    spei_df.to_csv("Dados/spei.csv", index = True, header = True)
#%%
