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
import os
from scipy.stats import ttest_ind

datapath = os.path.dirname(__file__)

filename = "Tubule_Length_Latrunculin.csv"

mean_width = 0.6

file_to_open = datapath+"/"+filename
df = pd.read_csv(file_to_open, sep= ";",  decimal=',', index_col=0)
df = df.reset_index()
pal = sns.color_palette("viridis", 4)


pal = sns.color_palette("viridis", 4)
g = sns.boxplot(y="tubule length", x="Treatment", data=df, order=["Control","Latrunculin"])
g = sns.swarmplot(y="tubule length", x="Treatment", hue="Experiment", data=df, order=["Control","Latrunculin"], palette=pal)


plt.show()

df2 = df.groupby([df["Experiment"],df["Treatment"]]).mean()

df3 = df2.reset_index()


print("Plotting means ")
pal = sns.color_palette("viridis", 4)
g = sns.pointplot(y="tubule length", x="Treatment", data=df3, order=["Control","Latrunculin"], join=False)
g = sns.swarmplot(y="tubule length", x="Treatment", hue="Experiment", data=df3, order=["Control","Latrunculin"], palette=pal)

plt.show()


cat1_wt = df3[df3['Treatment']=='Control']
cat1_KO = df3[df3['Treatment']=='Latrunculin']
print("T-test on means")
print(ttest_ind(cat1_wt['tubule length'], cat1_KO['tubule length']))



mean = df3.groupby('Treatment', sort=False)["tubule length"].mean()
ax=sns.pointplot(x="Treatment", y="tubule length", data=df3, order=["Control","Latrunculin"], join=False, capsize=0.3, color="black", markers="_" )
ax= sns.swarmplot(x="Treatment", y="tubule length", data=df3, order=["Control","Latrunculin"], size=10)

for tick, text in zip(ax.get_xticks(), ax.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the mean value for all replicates of either X or Y
    mean_val = df3[df3['Treatment']==sample_name]["tubule length"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax.plot([tick-mean_width/3, tick+mean_width/3], [mean_val, mean_val],
            lw=4, color='black')

ax.tick_params(labelsize=14)
ax.set_ylabel("tubule length", fontsize = 14)
ax.set_xlabel("")
plt.ylim(0.6,1.5)
plt.tight_layout()

savename = datapath + "/" + os.path.splitext(filename)[0] + ".eps"

plt.savefig(savename)


plt.show()



stats = ttest_ind(cat1_wt['tubule length'], cat1_KO['tubule length'])
dof=(len(cat1_wt)+len(cat1_KO))-2
print("Statistics summary:")
print("p-value: "+ str(stats[1]))
print("t value: "+ str(stats[0]))
print("Degrees of Freedom: " + str(dof))