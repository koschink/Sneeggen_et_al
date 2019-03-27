
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
plt.rcParams["figure.figsize"] = (12,8)



datapath = os.path.dirname(__file__)
print (datapath)

dirnames = ["WT", "KO"]


list1 = []



f2 = lambda x: (x/x.max()*100)

normalize_to_first = lambda x: (x/x.iloc[0])
# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 

print(dirnames)

for dirnum,directory in enumerate(dirnames):
    print(directory)
    datapath1 = datapath+"/"+directory
    print(datapath1)
    files1 = glob.glob(datapath1+"/*.csv") 
    print(files1) ## these files will be processed
    for filenum, csvfile in enumerate(files1):
        print(csvfile)
        df = pd.read_csv(csvfile, sep= ";",  decimal=',', index_col=0)
        df["Genotype"]=directory
        list1.append(df)
        
        #df1["Mean intensity"] = df["Channel 1"].copy()

        #df1["Cell"] = str(filenum)


#df3 = df2.query("Channel == 2")
#fig = plt.figure(1)
#ax1 = fig.add_subplot(111)
#df3["Count"] = df3.groupby("Cell")["Point #"].transform('count')
#df3["Mean_Int_Norm"] = ((df3["Mean Intensity of spot"] - df3["Mean Intensity of spot"].min()) / (df3["Mean Intensity of spot"].max() - df3["Mean Intensity of spot"].min())*100)
#sns.violinplot(df3["Mean_Int_Norm"], df3.Count, color="cubehelix", bw="silverman",inner="box")
#ax1.set_xlabel("Number of spots per cell")
#ax1.set_ylabel("Mean intensity per Spot")
#sns.despine()



pal1 = ["lightgrey", "grey"]
df4 = pd.concat(list1, axis=0)

df4["Ratio"]=df4["Max length"]/df4["Endosomes size"]

pal = sns.color_palette("viridis", 10)

"""g = sns.boxplot(x="Genotype", y="Max length", data=df4, dodge=False)
g = sns.stripplot(x="Genotype", y="Max length", hue="Genotype", data=df4, dodge=False,  )
plt.show()

g = sns.boxplot(x="Genotype", y="Ratio", data=df4, dodge=False)
g = sns.stripplot(x="Genotype", y="Ratio", hue="Genotype", data=df4, dodge=False,)
plt.show()
"""
means = df4.groupby(["Experiment", "Genotype"]).mean()
df_means = means.reset_index()



g = sns.boxplot(x="Genotype", y="Ratio", data=df4, dodge=False, palette=pal1)
g = sns.stripplot(x="Genotype", y="Ratio", hue="Experiment", data=df4, dodge=False)
plt.ylabel("tubule length (um)")
plt.show()

df5= df4.groupby([df4["Experiment"],df4["Genotype"]]).mean()

df6 = df5.reset_index()


cat1_wt = df6[df6['Genotype']=='WT']
cat1_KO = df6[df6['Genotype']=='KO']
print("T-test on means")
print(ttest_ind(cat1_wt['Ratio'], cat1_KO['Ratio']))

stats = ttest_ind(cat1_wt['Max length'], cat1_KO['Max length'])
dof=(len(cat1_wt)+len(cat1_KO))-2
print("Statistics summary:")
print("p-value: "+ str(stats[1]))
print("t value: "+ str(stats[0]))
print("Degrees of Freedom: " + str(dof))
