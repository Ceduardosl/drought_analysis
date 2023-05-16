#métrica para avaliar a propagação de seca meteorológica para hidrológica
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, pearsonr
from collections import namedtuple
import scipy.stats as sc
from mpl_toolkits.axes_grid1 import make_axes_locatable
def correl_indexes(x,y):
    corr_list = list()
    for i in range(1,12+1):
        corr_list.append([i,spearmanr(x.iloc[:,i],y)[0], spearmanr(x.iloc[:,i],y)[1]])
        # corr_list.append([i,pearsonr(x.iloc[:,i],y)[0], pearsonr(x.iloc[:,i],y)[1]])
    corr_df = pd.DataFrame(corr_list, columns = ["scale", "correl", "p-value"])
    return corr_df

def drought_run(df):
    count_d = 0
    severity = 0
    list_d = []
    drought_state = False
    for i in range(len(df)):
        if df.iloc[i] < 0:
            if drought_state == False:
                ini_d = df.index[i]
            drought_state = True
            count_d += 1
            severity += df.iloc[i]
            if df.iloc[i] == df.iloc[-1]:
                end_d = df.index[-1]
                list_d.append([ini_d, end_d, count_d, severity])
                count_d = 0
                severity = 0
                drought_state = 0
                break   
            if df.iloc[i+1] >= 0:
                end_d = df.index[i]
                list_d.append([ini_d, end_d, count_d, severity])
                count_d = 0
                severity = 0
                drought_state = False
    df_drought = pd.DataFrame(list_d, columns = ["ini", "end", "duration", "severity"])
    
    return df_drought

def plot_scatter_hist(x1, y1, x2, y2, label1, label2, title, file_name):
    fig, ax = plt.subplots(figsize = (11, 8))
    ax.scatter(x1, y1, label = label1)
    ax.scatter(x2, y2, label = label2)
    ax.set_aspect(1.)
    divider = make_axes_locatable(ax)
    ax.set_ylabel("Severidade")
    ax.set_xlabel("Duração")
    ax_histx = divider.append_axes("top", 1.5, pad = 0.1, sharex = ax)
    ax_histy = divider.append_axes("right", 2, pad = 0.1, sharey = ax)

    ax_histx.xaxis.set_tick_params(labelbottom = False)
    ax_histy.yaxis.set_tick_params(labelleft = False)

    ax_histx.hist([x1, x2], density = True)
    ax_histx.set_ylabel("Frequência")
    ax_histy.hist([y1, y2], density = True, orientation = "horizontal", label = [label1, label2])
    ax_histy.set_xlabel("Frequência")
    ax_histy.legend(loc = "lower right", fontsize = 'medium', markerscale = 0.5,
            borderaxespad = 0.2)

    ax_histy.set_title(title, loc = "center", y = 1.2, fontsize = "xx-large",
        bbox = dict(facecolor = "none", edgecolor = "black", boxstyle = "round, pad = 1"))

    fig.savefig("Figuras/{}.png".format(file_name), dpi = 600, bbox_inches = "tight", facecolor = "w")
    return (fig, ax)
#%%
spi_df = pd.read_csv("Dados/spi.csv", index_col = 0)
sri_df = pd.read_csv("Dados/sri.csv", index_col = 0)
spei_df = pd.read_csv("Dados/spei.csv", index_col = 0)

spi_df.index = pd.to_datetime(spi_df.index)
sri_df.index = pd.to_datetime(sri_df.index)
spei_df.index = pd.to_datetime(spei_df.index)

spi_df = spi_df.loc[spi_df.index.year >= 1935]
sri_df = sri_df.loc[sri_df.index.year >= 1935]
spei_df = spei_df.loc[spei_df.index.year >= 1935]

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
fig, ax = plt.subplots(dpi = 600)
ax.bar(x = corr_spi_p1.scale-0.2, height = corr_spi_p1.correl,
    width = 0.4, label = "P1 ({}-{})".format(p1[0], p1[1]))
ax.bar(x = corr_spi_p2.scale+0.2, height = corr_spi_p2.correl,
    width = 0.4, label = "P2 ({}-{})".format(p2[0], p2[1]))
ax.set_ylabel("Correlação de Spearman")
ax.set_xlabel("Escala (n)")
ax.set_xticks(list(range(1,13)))
ax.set_title("Correlação de Spearman - SPI-n e SRI-01", loc = "left")
ax.legend(loc = "best")
fig.savefig("Figuras/Spearman_SPI_SRI.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
#%%
# fig, ax = plt.subplots(dpi = 600)
# ax.bar(x = corr_spei_p1.scale-0.2, height = corr_spei_p1.correl,
#     width = 0.4, label = "P1 ({}-{})".format(p1[0], p1[1]))
# ax.bar(x = corr_spei_p2.scale+0.2, height = corr_spei_p2.correl,
#     width = 0.4, label = "P2 ({}-{})".format(p2[0], p2[1]))
# ax.set_ylabel("Correlação de Spearman")
# ax.set_xlabel("Escala (n)")
# ax.set_xticks(list(range(1,13)))
# ax.set_title("Correlação de Spearman - SPEI-n e SRI-01", loc = "left")
# ax.legend(loc = "best")
# fig.savefig("Figuras/Spearman_SPEI_SRI.png", dpi = 600, bbox_inches = "tight", facecolor = "w")

#%%
#3 meses foi o tempo de propagação da seca meteorológica para hidrológica

run_spi_1 = drought_run(spi_p1["Pr_index_3"])
run_spi_2 = drought_run(spi_p2["Pr_index_3"])
run_sri_1 = drought_run(sri_p1)
run_sri_2 = drought_run(sri_p2)
run_spei_1 = drought_run(spei_p1["wb_index_3"])
run_spei_2 = drought_run(spei_p2["wb_index_3"])

#%%
fig, ax = plt.subplots(figsize = (11, 8))
ax.scatter(run_sri_1.duration, run_sri_1.severity, label = "P1 ({} - {})".format(p1[0], p1[1]))
ax.scatter(run_sri_2.duration, run_sri_2.severity, label = "P2 ({} - {})".format(p2[0], p2[1]))
ax.set_aspect(1.)
divider = make_axes_locatable(ax)
ax.set_ylabel("Severidade")
ax.set_xlabel("Duração")
ax.legend(bbox_to_anchor = (1.679, 1.139), fontsize = 'medium')
ax_histx = divider.append_axes("top", 1.5, pad = 0.1)
ax_histy = divider.append_axes("right", 2, pad = 0.1)

ax_histx.xaxis.set_tick_params(labelbottom = False)
ax_histy.yaxis.set_tick_params(labelleft = False)

ax_histx.hist([run_sri_1.duration, run_sri_2.duration], density = True)
ax_histy.hist([run_sri_1.severity, run_sri_2.severity], density = True, orientation = "horizontal")
ax_histy.set_xlabel("Frequência")
ax_histx.set_ylabel("Frequência")

ax_histy.set_title("SPI-01", loc = "center", y = 1.2, fontsize = "xx-large",
        bbox = dict(facecolor = "none", edgecolor = "black", boxstyle = "round, pad = 1"))

ax_histx.sharex(ax)
# %%
plot_scatter_hist(run_sri_1.duration,
                run_sri_1.severity,
                run_sri_2.duration,
                run_sri_2.severity,
                "P1 ({} - {})".format(p1[0], p1[1]), 
                "P2 ({} - {})".format(p2[0], p2[1]),
                "SRI-01", "SRI_duration_severity")
plot_scatter_hist(run_spi_1.duration,
                run_spi_1.severity,
                run_spi_2.duration,
                run_spi_2.severity,
                "P1 ({} - {})".format(p1[0], p1[1]), 
                "P2 ({} - {})".format(p2[0], p2[1]),
                "SPI-03", "SPI_duration_severity")
plot_scatter_hist(run_spei_1.duration,
                run_spei_1.severity,
                run_spei_2.duration,
                run_spei_2.severity,
                "P1 ({} - {})".format(p1[0], p1[1]), 
                "P2 ({} - {})".format(p2[0], p2[1]),
                "SPEI-03", "SPEI_duration_severity")

#%%