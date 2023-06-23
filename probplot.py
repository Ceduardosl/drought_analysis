#%%
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 9})
#%%
spi = pd.read_csv("Dados\spi.csv", index_col = 0)
sri = pd.read_csv("Dados\sri.csv", index_col = 0)

spi.index = pd.to_datetime(spi.index)
sri.index = pd.to_datetime(sri.index)

spi = spi.loc[spi.index.year >= 1935]
sri = sri.loc[sri.index.year >= 1935]
# %%
pr = spi["Pr_acc_12"].dropna()
q = sri["Q_acc_12"].dropna()


#%%
fig, ax = plt.subplots(dpi = 600)
stats.probplot(pr, dist = stats.gamma, sparams = stats.gamma.fit(pr),
        plot = ax, rvalue = True)
ax.set_title("a) Q-Q plot of Gamma distribution | Aggregate Precipitation (12 months)", loc = "left")
ax.set_title(None, loc = "center")
fig.savefig("Figuras/Q-Q_Plot_Gamma_Pr-12.png", dpi = 600,  bbox_inches = "tight", facecolor = "w")
#%%
fig1, ax1 = plt.subplots(dpi = 600)
stats.probplot(q, dist = stats.gamma, sparams = stats.gamma.fit(q),
        plot = ax1, rvalue = True)
ax1.set_title("b) Q-Q plot of Gamma distribution | Aggregate Streamflow (12 months)", loc = "left")
ax1.set_title(None, loc = "center")
fig1.savefig("Figuras/Q-Q_Plot_Gamma_Q-12.png", dpi = 600,  bbox_inches = "tight", facecolor = "w")
#%%
fig, (ax1, ax2) = plt.subplots(1,2,dpi = 600)
stats.probplot(pr, dist = stats.gamma, sparams = stats.gamma.fit(pr),
        plot = ax1, rvalue = True)
stats.probplot(q, dist = stats.gamma, sparams = stats.gamma.fit(q),
        plot = ax2, rvalue = True)
# %%
