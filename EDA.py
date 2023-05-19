#%%
import pandas as pd
import ruptures as rpt
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mks
from matplotlib.gridspec import GridSpec
from scipy.stats import norm, kstest

#%%
data_EPQ = pd.read_excel("Dados/Dataset_EPQ.xlsx", sheet_name = "EPQ", index_col = 0)

annual_df = pd.DataFrame({"Q":data_EPQ.Q.resample("Y").mean(),
                          "Pr": data_EPQ.Pr.resample("Y").sum(),
                          "ETP": data_EPQ.ETP.resample("Y").sum()})
ks_q = kstest(annual_df.Q, "norm", args = norm.fit(annual_df.Q))
ks_pr = kstest(annual_df.Pr, "norm", args = norm.fit(annual_df.Pr))
ks_ETP = kstest(annual_df.ETP, "norm", args = norm.fit(annual_df.ETP))

# annual_df.Q = (annual_df.Q - annual_df.Q.mean())/annual_df.Q.std()
# annual_df.Pr = (annual_df.Pr - annual_df.Pr.mean())/annual_df.Pr.std()
# annual_df.ETP = (annual_df.ETP - annual_df.ETP.mean())/annual_df.ETP.std()

m_mov = pd.DataFrame({"Q_mov": annual_df.Q.rolling(window = 10).mean(),
                      "Pr_mov": annual_df.Pr.rolling(window = 10).mean(),
                      "ETP_mov": annual_df.ETP.rolling(window = 10).mean()})
#%%
df_p1 = annual_df.loc[(annual_df.index.year >= 1935) & (annual_df.index.year <= 1984)]
df_p2 = annual_df.loc[(annual_df.index.year >= 1985) & (annual_df.index.year <= 2020)]
#%%
mks_df = pd.DataFrame({
    "q_t": mks.original_test(annual_df.Q),
    "q_p1": mks.original_test(df_p1.Q),
    "q_p2": mks.original_test(df_p2.Q),
    "pr_t": mks.original_test(annual_df.Pr),
    "pr_p1": mks.original_test(df_p1.Pr),
    "pr_p2": mks.original_test(df_p2.Pr),
    "ETP_t": mks.original_test(annual_df.ETP),
    "ETP_p1": mks.original_test(df_p1.ETP),
    "ETP_p2": mks.original_test(df_p2.ETP)},
    index = ["trend", "h", "p", "z", "Tau", "s",
            "var_s", "a", "b"])
# %%
fig = plt.figure(dpi = 600, figsize = (10, 8))

gs = GridSpec(3,1, figure = fig, wspace = 0, hspace = 0.3)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex = ax1)
ax3 = fig.add_subplot(gs[2], sharex = ax1)
plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)
# ax1.sharey(ax3)
# ax2.sharey(ax3)
ax1.axvline(x = df_p2.index[0], c = "black", ls = "--", zorder = 1)
ax1.plot(annual_df.Q, c = "black", zorder = 3)
ax1.plot(m_mov.Q_mov, c = "blue", label = "Média Móvel (10 anos)", zorder = 2)
ax1.plot(df_p2.index,
        mks_df.q_p2.a*range(0, len(df_p2)) + mks_df.q_p2.b, 
        c = "red", label = "TendÊncia (P2)", zorder = 2)

ax2.axvline(x = df_p2.index[0], c = "black", ls = "--", zorder = 1)
ax2.plot(annual_df.Pr, c = "black", zorder = 3)
ax2.plot(m_mov.Pr_mov, c = "blue", label = "Média Móvel (10 anos)", zorder = 2)

ax3.axvline(x = df_p2.index[0], c = "black", ls = "--", zorder = 1)
ax3.plot(annual_df.ETP, c = "black", zorder = 3)
ax3.plot(m_mov.ETP_mov, c = "blue", label = "Média Móvel (10 anos)", zorder = 2)
ax3.plot(df_p2.index,
    mks_df.ETP_p2.a*range(0, len(df_p2)) + mks_df.ETP_p2.b,
    c = "red", label = "Tendência (P2)", zorder = 2)
# ax3.plot(annual_df.index,
#     mks_df.ETP_t.a*range(0, len(annual_df)) + mks_df.ETP_t.b,
#     c = "orange", label = "Trend (P1+P2)")
ax1.set_ylabel("Vazão (m³/s)")
ax2.set_ylabel("Precipitação (mm)")
ax3.set_ylabel("ETP (mm)")
ax3.set_xlabel("Anos")
ax1.set_title("a) Vazão média anual", loc = "left")
ax2.set_title("b) Precipitação anual", loc = "left")
ax3.set_title("c) ETP anual", loc = "left")
ax1.legend()
ax2.legend()
ax3.legend()

fig.savefig("Figuras/annual_TS.png", dpi = 600, bbox_inches = "tight", facecolor = "w")
#%%