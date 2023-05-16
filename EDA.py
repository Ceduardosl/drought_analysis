#%%
import pandas as pd
import ruptures as rpt
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mks
#%%
data_q = pd.read_excel("Dados/streamflow_data.xlsx", sheet_name = "Monthly_TS", index_col = 0)

data_q = data_q.loc[(data_q.index.year >= 1935) & (data_q.index.year <= 2020)]

q_max = data_q["max"].resample("Y").max()
q_min = data_q["min"].resample("Y").min()
q_mean = data_q["mean"].resample("Y").mean()
#%%
m_mov = q_mean.rolling(window = 10).mean()

mks_test = mks.original_test(q_mean)
#%%
fig, ax = plt.subplots(dpi = 600)
ax.boxplot(data_q, labels = ["Média", "Máxima", "Mínima"])
ax.set_title("Vazões Mensais", loc = "left")
ax.set_ylabel("Vazões (m³/s)")
fig.savefig("Figuras/Boxplot_Vazao.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
#%%
fig, ax = plt.subplots(dpi = 600)
ax.plot(q_mean, c = "green", label = "Média Diária")
ax.plot(q_max, c = "blue", label = "Máxima Diária")
ax.plot(q_min, c = "red", label = "Mínima Diária")
ax.legend()
ax.set_title("Vazões Anuais", loc = "left")
fig.savefig("Figuras/TS_Vazao.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
# %%
fig, ax = plt.subplots(dpi = 600)
ax.plot(q_mean, c = "black", label = "Vazão Média Anual", zorder = 2)
ax.plot(m_mov, c = "blue", label = "Média Móvel (10 anos)", zorder = 3)
ax.plot(q_mean.index,
    mks_test.slope*range(len(q_mean))+mks_test.intercept,
    c = "red", lw = 0.75, zorder = 1)
ax.set_title("Vazão Média Anual", loc = "left")
ax.set_xlabel("Anos")
ax.set_ylabel("Vazão (m³/s)")
ax.legend(ncol = 2, loc = "lower left", borderaxespad = 0.2)
fig.savefig("Figuras/Q_Anual.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
# %%
