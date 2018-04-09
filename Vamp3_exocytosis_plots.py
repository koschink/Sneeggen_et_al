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


filepath = datapath+"/data/vamp3_exocytosis.csv"
df = pd.read_csv(filepath, sep= ";",  decimal='.', index_col=0)
df = df.reset_index()
pal = sns.color_palette("viridis", 3)
g = sns.boxplot(y="events", x="genotype", data=df, order=["WT","KO"])
g = sns.swarmplot(y="events", x="genotype", hue="experiment", data=df,order=["WT","KO"], palette=pal)
plt.ylim(-0, 0.18)


plt.show()

