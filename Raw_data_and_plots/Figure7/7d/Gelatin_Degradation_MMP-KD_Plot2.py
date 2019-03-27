# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 19:14:36 2018

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


csvname = "Gelatin_MT1_MMP_KD_raw.csv"
epsname = "Gelatin_MT1_MMP_KD_plot.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname

df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)
df = df.reset_index()
#df["Normalized intensity"] =df.groupby(["Experiment", "Treatment"])["Mean intensity"].apply(lambda x: x/x.mean())
means_stds = df.groupby(['Experiment'])['degradation_per_cell'].agg('mean').reset_index()

means_stds = means_stds.rename(columns={"degradation_per_cell": "mean_norm"})
df = df.merge(means_stds,on=(["Experiment"]))
df["Normalized degradation"] = df["degradation_per_cell"]/df["mean_norm"]




df2 = df.groupby([df["Experiment"],df["Treatment"]]).mean()
df2 = df2.drop(["Experiment"], axis=1)
df3 = df2.reset_index()

print("Plotting means ")
pal = sns.color_palette("viridis", 4)
g = sns.pointplot(y="Normalized degradation", x="Treatment", data=df3, order=["siControl","siMT1-MMP"], join=False)
g = sns.swarmplot(y="Normalized degradation", x="Treatment", hue="Experiment", data=df3,order=["siControl","siMT1-MMP"], palette=pal)


plt.show()


cat1_wt = df3[df3['Treatment']=='siControl']
cat1_KO = df3[df3['Treatment']=='siMT1-MMP']

stats = ttest_ind(cat1_wt['Normalized degradation'], cat1_KO['Normalized degradation'])
dof=(len(cat1_wt)+len(cat1_KO))-2
print("Statistics summary:")
print("p-value: "+ str(stats[1]))
print("t value: "+ str(stats[0]))
print("Degrees of Freedom: " + str(dof))

ax=sns.pointplot(x="Treatment", y="Normalized degradation", data=df3, join=False, order=["siControl","siMT1-MMP"], capsize=0.3, color="Black")
ax= sns.swarmplot(x="Treatment", y="Normalized degradation", data=df3, palette=pal2, order=["siControl","siMT1-MMP"], size=10)
for tick, text in zip(ax.get_xticks(), ax.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the mean value for all replicates of either X or Y
    mean_val = df[df['Treatment']==sample_name]["Normalized degradation"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax.plot([tick-mean_width/3, tick+mean_width/3], [mean_val, mean_val],
            lw=4, color='black')
ax.tick_params(labelsize=14)
ax.set_ylabel("Relative Gelatin degradation", fontsize = 12)
ax.set_xlabel("")

plt.tight_layout()
plt.savefig(savepath)
plt.show()