# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 19:14:36 2018

@author: kaysch
"""
from __future__ import print_function
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
from scipy.stats import mannwhitneyu
csvname = "MT1-MMP_Exocytosis.csv"
epsname = "MT1-MMP_Exocytosis.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname



df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)
df = df.reset_index()
pal = sns.color_palette("viridis", 3)
g = sns.boxplot(y="events", x="genotype", data=df, order=["WT","KO"])
g = sns.swarmplot(y="events", x="genotype", hue="experiment", data=df,order=["WT","KO"], palette=pal)
plt.ylim(-0, 0.18)
plt.show()

df2 = df.groupby([df["experiment"],df["genotype"]]).mean()
df2.reset_index()
df3 = df2.reset_index()
print("Plotting means ")
pal = sns.color_palette("viridis", 4)
g = sns.pointplot(y="events", x="genotype", data=df3, order=["WT","KO"], join=False)
g = sns.swarmplot(y="events", x="genotype", hue="experiment", data=df3,order=["WT","KO"], palette=pal)


plt.show()

cat1_wt = df3[df3['genotype']=='WT']
cat1_KO = df3[df3['genotype']=='KO']
print("T-test on means")
print(ttest_ind(cat1_wt['events'], cat1_KO['events']))
