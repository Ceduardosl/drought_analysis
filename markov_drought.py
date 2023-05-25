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

    if np.all(M.sum(axis = 1) != 1):
        print("### Há linhas em que o somatório das colunas é diferente de 1 ###")

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

def plot_transition_matrix(list_df, list_titles, output_path):
    fig = plt.figure(dpi = 600, figsize = (8, 6))

    gs = GridSpec(2,2, figure = fig, wspace = 0.15, hspace = 0.35)
    # gs.tight_layout(figure = fig, h_pad = 2, w_pad = 1.5)
    ax1 = fig.add_subplot(gs[0,0])
    ax2 = fig.add_subplot(gs[0,1])
    ax3 = fig.add_subplot(gs[1,0])
    ax4 = fig.add_subplot(gs[1,1])

    sns.heatmap(list_df[0], ax = ax1, cmap = "binary",
            linecolor = "black", linewidths = 0.5,
            annot = list_df[0].multiply(100).round(2).astype("str") + "%",
            fmt = "", cbar = False)

    sns.heatmap(list_df[1], ax = ax2, cmap = "binary",
            linecolor = "black", linewidths = 0.5,
            annot = list_df[1].multiply(100).round(2).astype("str") + "%",
            fmt = "", cbar = False)

    sns.heatmap(list_df[2], ax = ax3, cmap = "binary",
            linecolor = "black", linewidths = 0.5,
            annot = list_df[2].multiply(100).round(2).astype("str") + "%",
            fmt = "", cbar = False)

    sns.heatmap(list_df[3], ax = ax4, cmap = "binary",
            linecolor = "black", linewidths = 0.5,
            annot = list_df[3].multiply(100).round(2).astype("str") + "%",
            fmt = "", cbar = False)

    ax1.set_title(list_titles[0], loc = "left")
    ax2.set_title(list_titles[1], loc = "left")
    ax3.set_title(list_titles[2], loc = "left")
    ax4.set_title(list_titles[3], loc = "left")
    fig.savefig("{}.png".format(output_path), dpi = 600, bbox_inches = "tight", facecolor = "w")


    return ("#### Arquivo Criado - {}!####".format(output_path))
#%%
if __name__ == '__main__':
    spi_df = pd.read_csv("Dados/spi.csv", index_col = 0)
    spi_df.index = pd.to_datetime(spi_df.index)
    spei_df = pd.read_csv("Dados/spei.csv", index_col = 0)
    spei_df.index = pd.to_datetime(spei_df.index)
    sri_df = pd.read_csv("Dados/sri.csv", index_col = 0)
    sri_df.index = pd.to_datetime(sri_df.index)

    spi = spi_df["Pr_index_12"]
    spi_p1 = spi.loc[(spi.index.year >= 1935) & (spi.index.year <= 1984) & (spi.index.month == 12)]
    spi_p2 = spi.loc[(spi.index.year >= 1985) & (spi.index.year <= 2020) & (spi.index.month == 12)]

    spei = spei_df["wb_index_12"]
    spei_p1 = spei.loc[(spei.index.year >= 1935) & (spei.index.year <= 1984) & (spei.index.month == 12)]
    spei_p2 = spei.loc[(spei.index.year >= 1985) & (spei.index.year <= 2020) & (spei.index.month == 12)]

    sri = sri_df["Q_index_12"]
    sri_p1 = sri.loc[(sri.index.year >= 1935) & (sri.index.year <= 1984) & (sri.index.month == 12)]
    sri_p2 = sri.loc[(sri.index.year >= 1985) & (sri.index.year <= 2020) & (sri.index.month == 12)]

    spi_p1 = drought_class(spi_p1)
    spi_p2 = drought_class(spi_p2)
    spei_p1 = drought_class(spei_p1)
    spei_p2 = drought_class(spei_p2)
    sri_p1 = drought_class(sri_p1)
    sri_p2 = drought_class(sri_p2)

    M_spi_p1 = transition_matrix(n_class = 4, ts = spi_p1)
    M_spi_p2 = transition_matrix(n_class = 4, ts = spi_p2)
    M_spei_p1 = transition_matrix(n_class = 4, ts = spei_p1)
    M_spei_p2 = transition_matrix(n_class = 4, ts = spei_p2)
    M_sri_p1 = transition_matrix(n_class = 4, ts = sri_p1)
    M_sri_p2 = transition_matrix(n_class = 4, ts = sri_p2)

    M_spi_p1 = pd.DataFrame(M_spi_p1, columns = ["SS", "SL", "SM", "SSE"], index = ["SS", "SL", "SM", "SSE"])
    M_spi_p2 = pd.DataFrame(M_spi_p2, columns = ["SS", "SL", "SM", "SSE"], index = ["SS", "SL", "SM", "SSE"])
    M_spei_p1 = pd.DataFrame(M_spei_p1, columns = ["SS", "SL", "SM", "SSE"], index = ["SS", "SL", "SM", "SSE"])
    M_spei_p2 = pd.DataFrame(M_spei_p2, columns = ["SS", "SL", "SM", "SSE"], index = ["SS", "SL", "SM", "SSE"])
    M_sri_p1 = pd.DataFrame(M_sri_p1, columns = ["SS", "SL", "SM", "SSE"], index = ["SS", "SL", "SM", "SSE"])
    M_sri_p2 = pd.DataFrame(M_sri_p2, columns = ["SS", "SL", "SM", "SSE"], index = ["SS", "SL", "SM", "SSE"])


    s_spi_p1 = pd.DataFrame(stationary_distr(M_spi_p1),
                        columns = ["SS", "SL", "SM", "SSE"])
    s_spi_p2 = pd.DataFrame(stationary_distr(M_spi_p2),
                        columns = ["SS", "SL", "SM", "SSE"])
    s_spei_p1 = pd.DataFrame(stationary_distr(M_spei_p1),
                        columns = ["SS", "SL", "SM", "SSE"])
    s_spei_p2 = pd.DataFrame(stationary_distr(M_spei_p2),
                        columns = ["SS", "SL", "SM", "SSE"])
    s_sri_p1 = pd.DataFrame(stationary_distr(M_sri_p1),
                        columns = ["SS", "SL", "SM", "SSE"])
    s_sri_p2 = pd.DataFrame(stationary_distr(M_sri_p2),
                        columns = ["SS", "SL", "SM", "SSE"])

    s_df = pd.concat([s_spi_p1.iloc[-1:],
                s_spi_p2.iloc[-1:],
                s_spei_p1.iloc[-1:],
                s_spei_p2.iloc[-1:],
                s_sri_p1.iloc[-1:],
                s_sri_p2.iloc[-1:]])

    s_df.index = ["SPI-12|P1(1935 - 1984)",
                "SPI-12|P2(1985 - 2020)",
                "SPEI-12|P1(1935 - 1984)",
                "SPEI-12|P2(1985 - 2020)",
                "SRI-12|P1(1935 - 1984)",
                "SRI-12|P2(1985 - 2020)"]

    s_df.to_csv("Dados/stationary_distr_spi_sri.csv", index = True, header = True)

    plot_transition_matrix([M_spi_p1, M_spi_p2, M_sri_p1, M_sri_p2],
                        ["a) SPI-12 - P1", "b) SPI-12 - P2",
                            "c) SRI-12 - P1", "d) SRI-12 - P2"],
                            "Figuras/SPI_SRI_Transition_Matrix")

    plot_transition_matrix([M_spei_p1, M_spei_p2, M_sri_p1, M_sri_p2],
                        ["a) SPEI-12 - P1", "b) SPEI-12 - P2",
                            "c) SRI-12 - P1", "d) SRI-12 - P2"],
                            "Figuras/SPEI_SRI_Transition_Matrix")
# %%
