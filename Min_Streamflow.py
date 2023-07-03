#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mks
import matplotlib.ticker as mtick
import scipy.stats as sc
from matplotlib.ticker import AutoMinorLocator
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 9})

def permance_curve(q):

    q = np.array(df_daily.Q)
    list_prob = []
    list_flow = []
    for i in range(0, 100, 1):
        list_prob.append(1-(i/100))
        list_flow.append(np.percentile(q,i))

    perm_curve = np.array([list_prob, list_flow])

    return perm_curve
# %%
daily_data = pd.read_csv("Dados/3_46902000.csv", usecols = [1,2,3], index_col = 0)
daily_data.index = pd.to_datetime(daily_data.index)
daily_data.columns = ["Consist", "Q"]
#%%
list_r = []
dict_period = {
    "P1": [1935, 1954],
    "P2": [1955, 1969],
    "P3": [1970, 1984],
    "P4": [1985, 2000],
    "P5": [2001, 2010],
    "P6": [2011, 2020]
}
fig, ax = plt.subplots(dpi = 600)

plt.yscale("log")
for p, color in zip(["P1", "P2", "P3", "P4", "P5", "P6"], ["black", "blue", "purple", "green", "darkorange", "red"]):
    df_daily = pd.DataFrame({"Q": np.nan},
            index = daily_data.loc[
                        (daily_data.index.year >= dict_period[p][0])& 
                        (daily_data.index.year <= dict_period[p][1])].index)
    df_daily.Q.fillna(daily_data.Q.loc[daily_data.Consist == 2], inplace = True)
    df_daily.Q.fillna(daily_data.Q.loc[daily_data.Consist == 1], inplace = True)
    df_daily.to_csv("Dados/{}_Q_daily_TS.csv".format(p), index = True, header = True)
    curve = permance_curve(df_daily)
    ax.plot(curve[0,:], curve[1,:], label = p, zorder = 3, lw = 1.5, c = color)
    list_r.append([p, curve[1, np.where(curve[0,:] == 0.95)].item()])

ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.00])
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.grid(visible = True, which = "both", zorder = 1)
ax.legend(framealpha = 1)
ax.set_title("Flow-Duration Curves", loc = "left")
ax.set_ylabel("Streamflow (m³/s)")
ax.set_xlabel("Probability of Exceedance (%)")
fig.savefig("Figuras/Curvas_Permanencia.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
df_r = pd.DataFrame(list_r, columns = ["Period", "Q95"])
df_r.to_csv("Dados/Q95.csv", index = False, header = True, sep = ";")
#%%
list_r = []
dict_period = {
    "P1": [1935, 1954],
    "P2": [1955, 1969],
    "P3": [1970, 1984],
    "P4": [1985, 2000],
    "P5": [2001, 2010],
    "P6": [2011, 2020]
}
for p in ["P1", "P2", "P3", "P4", "P5", "P6"]:
    daily_data = daily_data.loc[(daily_data.index.year >= 1935) & (daily_data.index.year <= 2020)]
    df_daily = pd.DataFrame({"Q": np.nan},
            index = daily_data.loc[
                        (daily_data.index.year >= dict_period[p][0])& 
                        (daily_data.index.year <= dict_period[p][1])].index)
    df_daily.Q.fillna(daily_data.Q.loc[daily_data.Consist == 2], inplace = True)
    df_daily.Q.fillna(daily_data.Q.loc[daily_data.Consist == 1], inplace = True)

    df_daily.sort_values("Date", inplace = True)
    m_mov = df_daily.rolling(window = 7).mean()
    m_mov.dropna(inplace = True)

    min_annual = m_mov.resample("Y").min()
    fig, ax = plt.subplots(dpi = 600)
    sc.probplot(min_annual.Q, dist = sc.gumbel_l,
            sparams = sc.gumbel_l.fit(min_annual.Q),
            plot = ax, rvalue = True)
    ax.set_title("{}) Q-Q Plot Gumbel - Min. Annual Moving Average (7 dias) ".format(p),
            loc = "left")
    ax.set_title(None, loc = "center")
    fig.savefig("Figuras/{}_Q-Q_plot_Gumbel_m_mov_7.png".format(p),
        dpi = 600,  bbox_inches = "tight", facecolor = "w")

    list_r.append([
        sc.kstest(min_annual.Q, cdf = "gumbel_l", args = sc.gumbel_l.fit(min_annual.Q))[0],
        sc.kstest(min_annual.Q, cdf = "gumbel_l", args = sc.gumbel_l.fit(min_annual.Q))[1],
        sc.gumbel_l.ppf(1-(1/10), *sc.gumbel_l.fit(min_annual.Q))])
    
df_r = pd.DataFrame(list_r, index = ["P1", "P2", "P3", "P4", "P5", "P6"],
        columns = ["stats_kms", "p-value", "q7,10"])
df_r.to_csv("Dados/q_7,10_Gumbel_l.csv", index = True, header = True)
#%%
# dict_period = {
#     "P1": [1961, 1976],
#     "P2": [1976, 1986],
#     "P3": [1986, 2001],
#     "P4": [2001, 2011],
#     "P5": [2011, 2020]
# }
dict_period = {
    "P1": [1935, 1955],
    "P2": [1955, 1970],
    "P3": [1970, 1985],
    "P4": [1985, 2001],
    "P5": [2001, 2011],
    "P6": [2011, 2020]
}
daily_data = daily_data.loc[(daily_data.index.year >= 1935) & (daily_data.index.year <= 2020)]
df_daily = pd.DataFrame({"Q": np.nan},
            index = daily_data.index)
df_daily.Q.fillna(daily_data.Q.loc[daily_data.Consist == 2], inplace = True)
df_daily.Q.fillna(daily_data.Q.loc[daily_data.Consist == 1], inplace = True)
min_annual = df_daily.resample("Y").min()
min_annual.index = min_annual.index.year
mks_test = mks.original_test(min_annual)

fig, ax = plt.subplots(dpi = 600)
for p, color in zip(["P1", "P2", "P3", "P4", "P5", "P6"], ["black", "blue", "purple", "green", "darkorange", "red"]):
    ax.plot(min_annual.loc[
        (min_annual.index >= dict_period[p][0]) &
        (min_annual.index <= dict_period[p][1])],
        c = color, marker = "o", label = p, markersize = 4.5,
        zorder = 3)
if mks_test.h == True:
    ax.plot(min_annual.index,
        mks_test.slope*range(len(min_annual))+mks_test.intercept,
        c = "darkred", ls = "--", lw = 1.5, zorder = 2, label = "Trend")
ax.legend(ncol = 2, loc = "best")
ax.grid(zorder = 1)
ax.set_ylabel("Streamflow (m³/s)")
ax.set_title("Minimum Annual Daily Streamflow", loc = "left") 
fig.savefig("Figuras/Q_min_anual.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
# %%
