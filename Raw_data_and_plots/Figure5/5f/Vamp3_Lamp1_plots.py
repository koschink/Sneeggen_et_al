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


csvname = "vamp3_lamp1.csv"
epsname = "vamp3_lamp1.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname


df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)
df = df.reset_index(drop=True)

pal = sns.color_palette("viridis", 4)
g = sns.boxplot(y="Mean intensity", x="Genotype", data=df, order=["WT","KO"])
g = sns.swarmplot(y="Mean intensity", x="Genotype", hue="Experiment", data=df,order=["WT","KO"], palette=pal)


plt.show()


cat1_wt = df[df['Genotype']=='WT']
cat1_KO = df[df['Genotype']=='KO']
a= ttest_ind(cat1_wt['Mean intensity'], cat1_KO['Mean intensity'])
print(a)
print(mannwhitneyu(cat1_wt['Normalized intensity'], cat1_KO['Normalized intensity'], alternative="two-sided"))


df2 = df.groupby([df["Experiment"],df["Genotype"]]).mean()
df2.reset_index()
df3 = df2.reset_index()
print("Plotting means ")
#sns.boxplot(x="Genotype", y="Normalized intensity", data=df3, order=["WT","KO"] )
sns.stripplot(x="Genotype", y="Normalized intensity", data=df3, order=["WT","KO"], hue="Experiment")
sns.pointplot(x="Genotype", y="Normalized intensity", data=df3, order=["WT","KO"], ci=95, join=False, capsize=0.1, dodge=True)


plt.show()

cat1_wt = df3[df3['Genotype']=='WT']
cat1_KO = df3[df3['Genotype']=='KO']
print("T-test on means")
print(ttest_ind(cat1_wt['Mean intensity'], cat1_KO['Mean intensity']))
