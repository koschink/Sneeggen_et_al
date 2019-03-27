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


csvname = "Invasion_KO.csv"
epsname = "Invasion_KO.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname

df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)
df = df.reset_index()


mean_width = 0.6


pal2 = ["grey", "grey"]


pal = sns.color_palette("viridis", 4)
g = sns.boxplot(y="Invasion", x="Genotype", data=df, order=["WT","KO"])
g = sns.swarmplot(y="Invasion", x="Genotype", hue="Experiment", data=df,order=["WT","KO"], palette=pal)

plt.show()


g = sns.violinplot(y="Invasion", x="Genotype", data=df, order=["WT","KO"])
g = sns.swarmplot(y="Invasion", x="Genotype", hue="Experiment", data=df,order=["WT","KO"], palette=pal, dodge=True)
plt.show()


cat1_wt = df[df['Genotype']=='WT']
cat1_KO = df[df['Genotype']=='KO']
print(ttest_ind(cat1_wt['Invasion'], cat1_KO['Invasion']))


df2 = df.groupby([df["Experiment"],df["Genotype"]]).mean()
df2.reset_index()
df3 = df2.reset_index()
print("Plotting means ")
sns.pointplot(x="Genotype", y="Invasion", data=df3, order=["WT","KO"], join=False, capsize=0.1, color="black" )
sns.swarmplot(x="Genotype", y="Invasion", data=df3, order=["WT","KO"], palette=pal2, size=10, )
plt.ylim(0,100)
plt.show()

cat1_wt = df3[df3['Genotype']=='WT']
cat1_KO = df3[df3['Genotype']=='KO']
print("T-test on means")
print(ttest_ind(cat1_wt['Invasion'], cat1_KO['Invasion']))


mean = df3.groupby('Genotype', sort=False)["Invasion"].mean()
ax=sns.pointplot(x="Genotype", y="Invasion", data=df3, order=["WT","KO"], join=False, capsize=0.25, color="black", markers="_" )
ax= sns.swarmplot(x="Genotype", y="Invasion", data=df3, order=["WT","KO"], palette=pal2, size=10)

for tick, text in zip(ax.get_xticks(), ax.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the mean value for all replicates of either X or Y
    mean_val = df3[df3['Genotype']==sample_name]["Invasion"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax.plot([tick-mean_width/3, tick+mean_width/3], [mean_val, mean_val],
            lw=4, color='black')

ax.tick_params(labelsize=14)
ax.set_ylabel("Invasion", fontsize = 14)
ax.set_xlabel("")
plt.ylim(0,100)
plt.tight_layout()
plt.savefig("d:\Invasion_KO.eps")
plt.show()
plt.show()