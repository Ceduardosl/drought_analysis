#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pymannkendall as mks
import seaborn as sns

def drought_class(df):
    #Extreme Dry (ED) - SPI <= -2.0 - index = 4
    #Severely Dry (SD) - -2.00 < SPI <= -1.50 - index = 3
    #Moderately Dry (MD) - -1.50 < SPI <= -1.0 - index = 2
    #Mild Drought - -1.00 < SPI < 0 - index = 1
    #No Drought - SPI >= 0 - index = 0

    df.loc[df >= 0] = 0
    df.loc[(df > -1) & (df < 0)] = 1
    df.loc[(df > -1.5) & (df <= -1.0)] = 2
    df.loc[(df <= -1.5)] = 3
    # df.loc[df <= -2] = 4
    #não ocorre ED no P1, então agrupa-se a ED e SD em uma única classe
    #evitar divisão por 0
    
    df = df.astype("int16")
    
    return df

def transition_matrix(n_class, ts):
    #ts = time series (pandas.series) não um dataframe
    #n_class = número de classes para as transições
    np.seterr(invalid = "ignore") 

    M = np.zeros((n_class, n_class))

    for i,j in zip(ts, ts[1:]):
        M[i][j] += 1
    
    M = M/M.sum(axis = 1, keepdims = True)

    return M

def stationary_distr(M):
    M = np.array(M)
    state = np.array([np.random.dirichlet((1,1,1,1))])
    state_list = state
    count_conv = 0
    for x in range(1,1000, 1):
        state = np.dot(state, M)
        state_list = np.append(state_list, state, axis = 0)
        if np.max(abs(state_list[x] - state_list[x-1])) <= 10**-8:
            count_conv += 1
            if count_conv >= 5:
                break
            else:
                continue
    return state_list
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

M_spi_p1 = pd.DataFrame(M_spi_p1, columns = ["SS", "SL", "SM", "SSE"], index = ["SS", "SL", "SM", "SSE"])
M_spi_p2 = pd.DataFrame(M_spi_p2, columns = ["SS", "SL", "SM", "SSE"], index = ["SS", "SL", "SM", "SSE"])
M_sri_p1 = pd.DataFrame(M_sri_p1, columns = ["SS", "SL", "SM", "SSE"], index = ["SS", "SL", "SM", "SSE"])
M_sri_p2 = pd.DataFrame(M_sri_p2, columns = ["SS", "SL", "SM", "SSE"], index = ["SS", "SL", "SM", "SSE"])

#%%
s_spi_p1 = pd.DataFrame(stationary_distr(M_spi_p1),
                    columns = ["SS", "SL", "SM", "SSE"])
s_spi_p2 = pd.DataFrame(stationary_distr(M_spi_p2),
                    columns = ["SS", "SL", "SM", "SSE"])
s_sri_p1 = pd.DataFrame(stationary_distr(M_sri_p1),
                    columns = ["SS", "SL", "SM", "SSE"])
s_sri_p2 = pd.DataFrame(stationary_distr(M_sri_p2),
                    columns = ["SS", "SL", "SM", "SSE"])
#%%
s_df = pd.concat([s_spi_p1.iloc[-1:],
            s_spi_p2.iloc[-1:],
            s_sri_p1.iloc[-1:],
            s_sri_p2.iloc[-1:]])

s_df.index = ["SPI-12|P1(1935 - 1984)",
            "SPI-12|P2(1985 - 2020)",
            "SRI-12|P1(1935 - 1984)",
            "SRI-12|P2(1985 - 2020)"]

s_df.to_csv("Dados/stationary_distr_spi_sri.csv", index = True, header = True)
#%%
fig = plt.figure(dpi = 600, figsize = (8, 6))
gs = GridSpec(2,2, figure = fig, wspace = 0.15, hspace = 0.35)
# gs.tight_layout(figure = fig, h_pad = 2, w_pad = 1.5)
ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[0,1])
ax3 = fig.add_subplot(gs[1,0])
ax4 = fig.add_subplot(gs[1,1])

sns.heatmap(M_spi_p1, ax = ax1, cmap = "binary",
        linecolor = "black", linewidths = 0.5,
        annot = M_spi_p1.multiply(100).round(2).astype("str") + "%",
        fmt = "", cbar = False)

sns.heatmap(M_spi_p2, ax = ax2, cmap = "binary",
        linecolor = "black", linewidths = 0.5,
        annot = M_spi_p2.multiply(100).round(2).astype("str") + "%",
        fmt = "", cbar = False)

sns.heatmap(M_sri_p1, ax = ax3, cmap = "binary",
        linecolor = "black", linewidths = 0.5,
        annot = M_sri_p1.multiply(100).round(2).astype("str") + "%",
        fmt = "", cbar = False)

sns.heatmap(M_sri_p2, ax = ax4, cmap = "binary",
        linecolor = "black", linewidths = 0.5,
        annot = M_sri_p2.multiply(100).round(2).astype("str") + "%",
        fmt = "", cbar = False)

ax1.set_title("a) SPI-12 - P1", loc = "left")
ax2.set_title("b) SPI-12 - P2", loc = "left")
ax3.set_title("c) SRI-12 - P1", loc = "left")
ax4.set_title("d) SRI-12 - P2", loc = "left")
fig.savefig("Figuras/Transition_Matrix.png", dpi = 600, bbox_inches = "tight", facecolor = "w")

#%%
#####################TESTES###################
state = [1,0,0,0]
state_list = []

for x in range(1, 100, 1):
    state = np.dot(state, M_sri_p1)
    state_list.append(state)

state_df = pd.DataFrame(state_list, columns = ["SS", "SL", "SM", "SSE"])

#%%
state = [1,0,0,0]
state_list = []
M = np.array(M_sri_p1)
for x in range(1,10,1):
    M = M@M

state = np.dot(state, M) 

   

# %%
