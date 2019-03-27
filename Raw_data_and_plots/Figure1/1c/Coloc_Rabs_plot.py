from __future__ import division
from pandas import *
import pandas as pd
from math import *
import os
import matplotlib.pyplot as plt
import numpy
import glob
import random
import seaborn as sns
import matplotlib.ticker as ticker
from scipy.stats import ttest_ind


csvname = "Colocalization_Rabs.csv"
epsname = "Colocalization_Rabs.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname

df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)
df = df.reset_index()
#df["Normalized intensity"] =df.groupby(["Experiment", "Genotype"])["Mean intensity"].apply(lambda x: x/x.mean())

mean_width = 0.6

pal = sns.color_palette("viridis", 4)

pal2 = ["grey", "grey"]

# plots individual data points and error bars
ax=sns.pointplot(x="Marker", y="Colocalization", data=df, join=False, capsize=0.3, color="black", markers="_" )
ax= sns.swarmplot(x="Marker", y="Colocalization", data=df, palette=pal2, size=10)

# plots a large bar as the mean of each experiment

for tick, text in zip(ax.get_xticks(), ax.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the mean value for all replicates of either X or Y
    mean_val = df[df['Marker']==sample_name]["Colocalization"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax.plot([tick-mean_width/3, tick+mean_width/3], [mean_val, mean_val],
            lw=4, color='black')
ax.tick_params(labelsize=14)
ax.set_ylabel("Colocalization with WDFY2", fontsize = 14)
ax.set_xlabel("")

plt.tight_layout()



plt.savefig(savepath)
plt.show()


