#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 9})
#%%
data_EPQ = pd.read_excel("Dados/Dataset_EPQ.xlsx", sheet_name = "EPQ", index_col = 0)

#%%
EPQ_clim = data_EPQ.groupby(data_EPQ.index.month).mean()
var = ["Q", "Pr", "ETP"]
# %%
fig, ax = plt.subplots(dpi = 600)
ax.bar(EPQ_clim.Q.index, EPQ_clim.Q,
    tick_label = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"])
ax.set_ylabel("Streamflow (m³/s)")
ax.set_title("b) Streamflow - Climatology", loc = "left")
fig.savefig("Figuras/Vazao_Clim.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
#%%
fig1, ax1 = plt.subplots(dpi = 600)
ax1.bar(EPQ_clim.Pr.index, EPQ_clim.Pr,
    tick_label = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"])
ax1.set_ylabel("Precipitation (mm)")
ax1.set_title("a) Precipitation - Climatology", loc = "left")
fig1.savefig("Figuras/Pr_Clim.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
#%%
fig2, ax2 = plt.subplots(dpi = 600)
ax2.bar(EPQ_clim.ETP.index, EPQ_clim.ETP,
    tick_label = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"])
ax2.set_ylabel("ETP (mm)")
ax2.set_ylim(0, 170)
ax2.set_title("c) ETP", loc = "left")
fig2.savefig("Figuras/ETP_climatologica.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
#%%