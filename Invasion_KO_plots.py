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


filepath = datapath+"/data/Invasion_KO.csv"
df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)
df = df.reset_index()
pal = sns.color_palette("viridis", 4)
g = sns.boxplot(y="Invasion", x="Genotype", data=df, order=["WT","KO"])
g = sns.swarmplot(y="Invasion", x="Genotype", hue="Experiment", data=df,order=["WT","KO"], palette=pal)

plt.show()


cat1_wt = df[df['Genotype']=='WT']
cat1_KO = df[df['Genotype']=='KO']
print ttest_ind(cat1_wt['Invasion'], cat1_KO['Invasion'])


