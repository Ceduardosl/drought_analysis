#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
#%%
spi = pd.read_csv("Dados/spi.csv", index_col = 0)
sri = pd.read_csv("Dados/sri.csv", index_col = 0)
spi.index = pd.to_datetime(spi.index)
sri.index = pd.to_datetime(sri.index)
#%%
spi = spi["Pr_index_12"].loc[(spi.index.year >= 1935) & (spi.index.month == 12)]
sri = sri["Q_index_12"].loc[(sri.index.year >= 1935) & (sri.index.month == 12)]

#%%
fig = plt.figure(dpi = 600, figsize = (8, 6))

gs = GridSpec(2,1, figure = fig, wspace = 0.15, hspace = 0.35)
# gs.tight_layout(figure = fig, h_pad = 2, w_pad = 1.5)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
# ax1.plot(spi, zorder = 4)
# ax2.plot(sri)
ax1.fill_between(spi.index, spi.values, 0,
                 where = spi.values < 0, interpolate = True,
                 color = "red")
ax1.fill_between(spi.index, spi.values, 0,
                 where = spi.values > 0, interpolate = True,
                 color = "blue")
ax2.fill_between(sri.index, sri.values, 0,
                 where = sri.values < 0, interpolate = True,
                 color = "red")
ax2.fill_between(sri.index, sri.values, 0,
                 where = sri.values > 0, interpolate = True,
                 color = "blue")
ax1.set_title("a) SPI-12", loc = "left")
ax2.set_title("b) SRI-12", loc = "left")
ax1.axhline(y = 0, c = "black", ls = "-", lw = 0.7, zorder = 3)
ax2.axhline(y = 0, c = "black", ls = "-", lw = 0.7, zorder = 3)
ax1.axhline(y = -1.5, c = "grey", ls = "--", lw = 0.5, zorder = 1)
ax2.axhline(y = -1.5, c = "grey", ls = "--", lw = 0.5, zorder = 1)
ax1.set_yticks([-1.5, 0,  1.5])
ax2.set_yticks([-1.5, 0,  1.5])
fig.savefig("Figuras/SPI-12_SRI_12.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
# %%
# %%

for i in range(1, 10, 1):
    spi_acc = spi.rolling(window = i).mean()
    spi_acc.dropna(inplace = True)
    df = pd.DataFrame(spi_acc)
    df = df.merge(sri, left_index = True, right_index = True)

    print(np.corrcoef(df["Pr_index_12"], df["Q_index_12"]))
    # fig, ax = plt.subplots(dpi = 600)
    # ax.scatter(df["Pr_index_12"], df["Q_index_12"])
    # ax.set_title("Janela {}".format(i))
# %%
