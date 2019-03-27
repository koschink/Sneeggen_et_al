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
rcParams['figure.figsize'] = 4, 4

csvname = "Gelatin_degradation_Vamp3KD_raw.csv"
epsname = "Gelatin_degradation__Vamp3KD_plot.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname

df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)
df = df.reset_index()
#df["Normalized intensity"] =df.groupby(["Experiment", "Genotype"])["Mean intensity"].apply(lambda x: x/x.mean())
means_stds = df.groupby(['Experiment'])['degradation_per_cell'].agg('mean').reset_index()

means_stds = means_stds.rename(columns={"degradation_per_cell": "mean_norm"})
df = df.merge(means_stds,on=(["Experiment"]))
df["Normalized degradation"] = df["degradation_per_cell"]/df["mean_norm"]


mean_width = 0.6

pal = sns.color_palette("viridis", 4)

pal2 = ["grey", "grey"]



df2 = df.groupby([df["Experiment"],df["Genotype"]]).mean()
df2 = df2.drop(["Experiment"], axis=1)
df3 = df2.reset_index()

print("Plotting means ")
pal = sns.color_palette("viridis", 4)
g = sns.pointplot(y="Normalized degradation", x="Genotype", data=df3, order=["SCR","siVamp3"], join=False)
g = sns.swarmplot(y="Normalized degradation", x="Genotype", hue="Experiment", data=df3,order=["SCR","siVamp3"], palette=pal)


plt.show()


cat1_wt = df3[df3['Genotype']=='SCR']
cat1_KO = df3[df3['Genotype']=='siVamp3']

stats = ttest_ind(cat1_wt['Normalized degradation'], cat1_KO['Normalized degradation'])
dof=(len(cat1_wt)+len(cat1_KO))-2
print("Statistics summary:")
print("p-value: "+ str(stats[1]))
print("t value: "+ str(stats[0]))
print("Degrees of Freedom: " + str(dof))

ax=sns.pointplot(x="Genotype", y="Normalized degradation", data=df3, join=False, order=["SCR","siVamp3"], capsize=0.3, color="Black")
ax= sns.swarmplot(x="Genotype", y="Normalized degradation", data=df3, palette=pal2, order=["SCR","siVamp3"], size=10)
for tick, text in zip(ax.get_xticks(), ax.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the mean value for all replicates of either X or Y
    mean_val = df[df['Genotype']==sample_name]["Normalized degradation"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax.plot([tick-mean_width/3, tick+mean_width/3], [mean_val, mean_val],
            lw=4, color='black')
ax.tick_params(labelsize=14)
ax.set_ylabel("Average area of Gelatin degradation", fontsize = 12)
ax.set_xlabel("")

plt.tight_layout()
plt.savefig(savepath)
plt.show()