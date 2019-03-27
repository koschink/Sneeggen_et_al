# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 21:02:12 2018

@author: kaysch
"""

from __future__ import division
from pandas import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt
import numpy
import glob
import random
import seaborn as sns
import matplotlib.ticker as ticker
from scipy.stats import ttest_ind
import os
from pylab import rcParams
rcParams['figure.figsize'] = 3, 4


csvname = "WDFY2_KD_RTPCR.csv"
epsname = "WDFY2_KD_RTPCR.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname

df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)


df = df.reset_index()


#df["Normalized intensity"] =df.groupby(["Experiment", "Genotype"])["Mean intensity"].apply(lambda x: x/x.mean())

mean_width = 0.6

pal = sns.color_palette("viridis", 4)

pal2 = ["grey", "grey"]


df["WDFY2 expression"] = df["WDFY2 expression"]*100

#df["Normalized intensity"] =df.groupby(["Experiment", "Genotype"])["Mean intensity"].apply(lambda x: x/x.mean())

mean_width = 0.6

pal = sns.color_palette("viridis", 4)

pal2 = ["grey", "grey"]




ax=sns.barplot(x="Treatment", y="WDFY2 expression", data=df, capsize=0.3)
ax= sns.swarmplot(x="Treatment", y="WDFY2 expression", data=df, palette=pal, size=10)




ax.set_ylabel("relative WDFY2 expression (%)", fontsize = 12)
ax.set_xlabel("")


plt.tight_layout()



plt.show()


ax=sns.pointplot(x="Treatment", y="WDFY2 expression", data=df, join=False, capsize=0.3, color="Black")
ax= sns.swarmplot(x="Treatment", y="WDFY2 expression", data=df, palette=pal, size=10)
for tick, text in zip(ax.get_xticks(), ax.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the mean value for all replicates of either X or Y
    mean_val = df[df['Treatment']==sample_name]["WDFY2 expression"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax.plot([tick-mean_width/3, tick+mean_width/3], [mean_val, mean_val],
            lw=4, color='black')
ax.tick_params(labelsize=14)

ax.set_ylabel("relative WDFY2 expression (%)", fontsize = 12)
ax.set_xlabel("")

plt.tight_layout()
plt.savefig(savepath)


plt.show()

