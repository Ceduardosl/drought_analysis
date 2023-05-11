#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
data_EPQ = pd.read_excel("Dados/Dataset_EPQ.xlsx", sheet_name = "EPQ", index_col = 0)

#%%
EPQ_clim = data_EPQ.groupby(data_EPQ.index.month).mean()
var = ["Q", "Pr", "ETP"]
# %%
fig, ax = plt.subplots(dpi = 600)
ax.bar(EPQ_clim.Q.index, EPQ_clim.Q,
    tick_label = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"])
ax.set_ylabel("Vazão (m³/s)")
ax.set_title("a) Vazão", loc = "left")
fig.savefig("Figuras/Vazao_Climatologica.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
#%%
fig1, ax1 = plt.subplots(dpi = 600)
ax1.bar(EPQ_clim.Pr.index, EPQ_clim.Pr,
    tick_label = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"])
ax1.set_ylabel("Precipitação (mm)")
ax1.set_title("b) Precipitação", loc = "left")
fig1.savefig("Figuras/Pr_Climatologica.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
#%%
fig2, ax2 = plt.subplots(dpi = 600)
ax2.bar(EPQ_clim.ETP.index, EPQ_clim.ETP,
    tick_label = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"])
ax2.set_ylabel("ETP (mm)")
ax2.set_ylim(0, 170)
ax2.set_title("c) ETP", loc = "left")
fig2.savefig("Figuras/ETP_climatologica.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
#%%