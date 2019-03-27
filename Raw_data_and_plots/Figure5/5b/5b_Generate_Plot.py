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
plt.rcParams["figure.figsize"] = (12,8)

datapath = os.path.dirname(__file__)

dirnames = ["WT", "KO"]


list1 = []



f2 = lambda x: (x/x.max()*100)

normalize_to_first = lambda x: (x/x.iloc[0])
# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 


for dirnum,directory in enumerate(dirnames):
    print(directory)
    datapath1 = datapath+"/"+directory
    print(datapath1)
    files1 = glob.glob(datapath1+"/*.csv") 
    print(files1) ## these files will be processed
    for filenum, csvfile in enumerate(files1):
        df = pd.read_csv(csvfile, sep= ",",  decimal='.', index_col=0)
        df1 = pd.DataFrame()
        #df1["Mean intensity"] = df["Channel 1"].copy()

        #df1["Cell"] = str(filenum)
        df3 = df.apply(f2)
        df1["Normalized"] = df3["Vamp3"].copy()

        df1["Genotype"] = directory
        list1.append(df1)



#df3 = df2.query("Channel == 2")
#fig = plt.figure(1)
#ax1 = fig.add_subplot(111)
#df3["Count"] = df3.groupby("Cell")["Point #"].transform('count')
#df3["Mean_Int_Norm"] = ((df3["Mean Intensity of spot"] - df3["Mean Intensity of spot"].min()) / (df3["Mean Intensity of spot"].max() - df3["Mean Intensity of spot"].min())*100)
#sns.violinplot(df3["Mean_Int_Norm"], df3.Count, color="cubehelix", bw="silverman",inner="box")
#ax1.set_xlabel("Number of spots per cell")
#ax1.set_ylabel("Mean intensity per Spot")
#sns.despine()




df4 = pd.concat(list1, axis=0)

df4.index.names = ['ROI']
df5 = df4.reset_index()

pal = sns.color_palette("viridis", 10)
g = sns.pointplot(x="ROI", y="Normalized", hue="Genotype", data=df5, dodge=False, ci=95,capsize=.15)

plt.show()




