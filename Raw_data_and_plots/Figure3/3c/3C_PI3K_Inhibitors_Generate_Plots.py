# -*- coding: utf-8 -*-
"""
Created on Fri Jan 05 08:50:37 2018

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
plt.rcParams["figure.figsize"] = (12,8)
import os


list1 = []

# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 



#df3 = df2.query("Channel == 2")
#fig = plt.figure(1)
#ax1 = fig.add_subplot(111)
#df3["Count"] = df3.groupby("Cell")["Point #"].transform('count')
#df3["Mean_Int_Norm"] = ((df3["Mean Intensity of spot"] - df3["Mean Intensity of spot"].min()) / (df3["Mean Intensity of spot"].max() - df3["Mean Intensity of spot"].min())*100)
#sns.violinplot(df3["Mean_Int_Norm"], df3.Count, color="cubehelix", bw="silverman",inner="box")
#ax1.set_xlabel("Number of spots per cell")
#ax1.set_ylabel("Mean intensity per Spot")
#sns.despine()


#datapath = "I:/780/02_05_18/XBP1u_in_KO/results/" 
datapath = os.path.abspath('')
dirnames = ["SAR405", "Wortmannin", "DMSO"]



palette3 = ["Magenta", "Cyan"]

# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 

nuclei_count = []


for dirnum,directory in enumerate(dirnames):
    print(directory)
    datapath1 = datapath+"/"+directory
    print(datapath1)
    files1 = glob.glob(datapath1+"/*.csv") 
    print(files1) ## these files will be processed
    nuclei = 0
    for filenum, csvfile in enumerate(files1):
        df = pd.read_csv(csvfile, sep= ",",  decimal='.', index_col=0)
        df["Treatment"] = directory
        df["Image"] = str(filenum)
        df.reset_index(inplace=True, drop=True)
        df.index.name = "time"
        df.reset_index(inplace=True)
        #df["Count"] = df["Count"]*1.0
        #max_count = df["Count"].max()
        df["% of WDFY2 spots"] = df["Count"].apply(lambda x: x/df["Count"].max()*100)
        df["minutes"] = df["time"]/60*5


        list1.append(df)
        



df4 = pd.concat(list1, axis=0)


g =  sns.FacetGrid(data=df4, col="Treatment", hue="Treatment")
g.map(sns.lineplot, "minutes", "% of WDFY2 spots")
plt.show()


save_csv = datapath + "/Data.xls"
