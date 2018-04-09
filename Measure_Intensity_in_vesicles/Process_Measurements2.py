# -*- coding: utf-8 -*-
"""
Created on Fri Jan 05 08:50:37 2018

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


datapath0 = os.path.dirname(__file__)

datapath = datapath0+"/Measurements/"

dirnames = ["WT", "KO"]

plt.rcParams["figure.figsize"] = (12,8)
list1 = []

# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 


for dirnum,directory in enumerate(dirnames):
    print directory
    datapath1 = datapath+"/"+directory
    print datapath1
    files1 = glob.glob(datapath1+"/*.csv") 
    print files1 ## these files will be processed
    for filenum, csvfile in enumerate(files1):
        df = pd.read_csv(csvfile, sep= ",",  decimal='.', index_col=0)
        df1 = pd.DataFrame()
        df1["Area"] = df["Area"].copy()
        df1["Mean intensity"] = df["Mean intensity"]
        df1["Compartment"] =  df["Compartment"].copy()
        df1["Genotype"] = directory
        df1["Cell"] = str(filenum)
        
        df2 = df1[(df1["Area"] < 100)] # filtering out big aggregates


        list1.append(df2)





df4 = pd.concat(list1, axis=0)
df5 = df4

# aggregating per cell intensities by grouping measurements per cell an genotype.

df6 = df5.groupby([df5["Compartment"], df5["Genotype"], df5["Cell"]])

df7 = df6["Mean intensity","Area"].agg("mean").reset_index()

df7 = df7.sort_values("Genotype",ascending=False)

f, ax = plt.subplots()



g = sns.boxplot(x="Compartment", y="Mean intensity", hue="Genotype", data=df7, dodge=True, order=["EEA1", "Lamp1"])
g = sns.swarmplot(x="Compartment", y="Mean intensity", hue="Genotype", data=df7, dodge=True, order=["EEA1", "Lamp1"])


plt.ylabel("mean Vamp3 intensity per compartment and cell", labelpad=2)
plt.show()

# splitting data for t-test measurements

cat1 = df7[df7['Compartment']=='EEA1']
cat1_wt = cat1[cat1['Genotype']=='WT']
cat1_KO = cat1[cat1['Genotype']=='KO']
print ttest_ind(cat1_wt['Mean intensity'], cat1_KO['Mean intensity'])

#g.set(xticks=[10, 30, 50, 70, 90, 110], xticklabels=[10, 30, 50, 70, 90, 110])
