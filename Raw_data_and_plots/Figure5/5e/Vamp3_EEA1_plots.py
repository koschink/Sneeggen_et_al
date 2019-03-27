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


csvname = "vamp3_eea1.csv"
epsname = "vamp3_eea1.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname

df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)

df = df.reset_index()
#df["Normalized intensity"] =df.groupby(["Experiment", "Genotype"])["Mean intensity"].apply(lambda x: x/x.mean())
means_stds = df.groupby(['Experiment'])['Mean intensity'].agg('mean').reset_index()

means_stds = means_stds.rename(columns={"Mean intensity": "mean_norm"})
df = df.merge(means_stds,on=(["Experiment"]))
df["Normalized intensity"] = df["Mean intensity"]/df["mean_norm"]


pal = sns.color_palette("viridis", 4)
g = sns.boxplot(y="Mean intensity", x="Genotype", data=df, order=["WT","KO"])
g = sns.swarmplot(y="Mean intensity", x="Genotype", hue="Experiment", data=df,order=["WT","KO"], palette=pal)


plt.show()




cat1_wt = df[df['Genotype']=='WT']
cat1_KO = df[df['Genotype']=='KO']
print(ttest_ind(cat1_wt['Mean intensity'], cat1_KO['Mean intensity']))


df2 = df.groupby([df["Experiment"],df["Genotype"]]).mean()
df2.reset_index()
df3 = df2.reset_index()
print("Plotting means ")
pal = sns.color_palette("viridis", 4)
g = sns.pointplot(y="Mean intensity", x="Genotype", data=df3, order=["WT","KO"], join=False)
g = sns.swarmplot(y="Mean intensity", x="Genotype", hue="Experiment", data=df3,order=["WT","KO"], palette=pal)


plt.show()


cat1_wt = df3[df3['Genotype']=='WT']
cat1_KO = df3[df3['Genotype']=='KO']
print("T-test on means")
print(ttest_ind(cat1_wt['Mean intensity'], cat1_KO['Mean intensity']))


print("Plotting normalized intensity means ")
#sns.boxplot(x="Genotype", y="Normalized intensity", data=df3, order=["WT","KO"] )
sns.stripplot(x="Genotype", y="Normalized intensity", data=df3, order=["WT","KO"], hue="Experiment")
sns.pointplot(x="Genotype", y="Normalized intensity", data=df3, order=["WT","KO"], ci=95, join=False, capsize=0.1, dodge=True)


plt.show()


print("T-test on normalized intensity")
print(ttest_ind(cat1_wt['Normalized intensity'], cat1_KO['Normalized intensity']))

print("Plotting normalized values")
pal = sns.color_palette("viridis", 4)
g = sns.boxplot(y="Normalized intensity", x="Genotype", data=df, order=["WT","KO"])
g = sns.swarmplot(y="Normalized intensity", x="Genotype", hue="Experiment", data=df,order=["WT","KO"], palette=pal)


plt.savefig(savepath)


plt.show()
# generate normalized datafrome

