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
import os
from scipy.stats import ttest_ind
from pylab import rcParams
rcParams['figure.figsize'] = 3, 4


csvname = "WB_WDFY2_OE_MMP14.csv"
epsname = "WB_WDFY2_OE_MMP14.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname

df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)


df = df.reset_index()


#df["Normalized intensity"] =df.groupby(["Experiment", "Genotype"])["Mean intensity"].apply(lambda x: x/x.mean())

mean_width = 0.6

pal = sns.color_palette("viridis", 4)

pal2 = ["grey", "grey"]




ax=sns.barplot(x="Genotype", y="MMP14", data=df, capsize=0.3)
ax= sns.swarmplot(x="Genotype", y="MMP14", data=df, palette=pal, size=10)

ax.set_ylabel("relative MT1-MMP protein level", fontsize = 12)
ax.set_xlabel("")


plt.tight_layout()
plt.savefig(savepath)


plt.show()


ax=sns.pointplot(x="Genotype", y="MMP14", data=df, join=False, capsize=0.3, color="Black")
ax= sns.swarmplot(x="Genotype", y="MMP14", data=df, palette=pal, size=10)
for tick, text in zip(ax.get_xticks(), ax.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the mean value for all replicates of either X or Y
    mean_val = df[df['Genotype']==sample_name]["MMP14"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax.plot([tick-mean_width/3, tick+mean_width/3], [mean_val, mean_val],
            lw=4, color='black')

ax.tick_params(labelsize=14)


ax.set_ylabel("relative MT1-MMP protein level", fontsize = 12)
ax.set_xlabel("")
plt.ylim(0,5)

plt.tight_layout()
plt.savefig(savepath)





plt.show()



cat1_wt = df[df['Genotype']=='RPE1']
cat1_KO = df[df['Genotype']=='GFP-WDFY2']

stats = ttest_ind(cat1_wt['MMP14'], cat1_KO['MMP14'])
dof=(len(cat1_wt)+len(cat1_KO))-2
print("Statistics summary:")
print("p-value: "+ str(stats[1]))
print("t value: "+ str(stats[0]))
print("Degrees of Freedom: " + str(dof))
