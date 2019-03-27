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

csvname = "MMP_Accumulation.csv"
epsname= "MMP_Accumulation.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname



df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)

df = df.reset_index()
#df["Normalized intensity"] =df.groupby(["Experiment", "Genotype"])["Mean intensity"].apply(lambda x: x/x.mean())

mean_width = 0.6

pal = sns.color_palette("viridis", 4)

pal2 = ["grey", "grey"]


ax=sns.pointplot(x="Genotype", y="MMP14 intensity", data=df, join=False, capsize=0.3, order=["WT", "GFP-WDFY2" ], color="black", markers="_" )
ax= sns.swarmplot(x="Genotype", y="MMP14 intensity", data=df, palette=pal2,order=["WT", "GFP-WDFY2"], size=10, hue="Experiment")

for tick, text in zip(ax.get_xticks(), ax.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the mean value for all replicates of either X or Y
    mean_val = df[df['Genotype']==sample_name]["MMP14 intensity"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax.plot([tick-mean_width/3, tick+mean_width/3], [mean_val, mean_val],
            lw=4, color='black')
ax.tick_params(labelsize=14)
ax.set_ylabel("MT1-MMP intensity (normalized)", fontsize = 14)
ax.set_xlabel("")

plt.tight_layout()



plt.savefig(savepath)
plt.show()
