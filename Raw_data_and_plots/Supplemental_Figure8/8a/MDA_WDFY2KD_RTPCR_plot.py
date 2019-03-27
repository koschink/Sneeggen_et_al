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
from scipy.stats import ttest_1samp
import os


from pylab import rcParams
rcParams['figure.figsize'] = 3, 4



csvname = "MDA_RTPCR.csv"
epsname = "MDA_RTPCR.eps"

datapath = os.path.dirname(__file__)
filepath = datapath+"/"+csvname
savepath = datapath + "/" + epsname


df = pd.read_csv(filepath, sep= ";",  decimal=',', index_col=0)
df = df.reset_index()
#df["Normalized intensity"] =df.groupby(["Experiment", "Genotype"])["Mean intensity"].apply(lambda x: x/x.mean())

mean_width = 0.6

pal = sns.color_palette("viridis", 4)

pal2 = ["grey", "grey"]


ax=sns.barplot(x="Treatment", y="Expression", data=df, capsize=0.3)
ax= sns.swarmplot(x="Treatment", y="Expression", data=df, palette=pal, size=10)

ax.set_ylabel("relative MT1-MMP protein level (%)", fontsize = 12)
ax.set_xlabel("")
plt.tight_layout()
plt.savefig(savepath)
plt.show()


ax=sns.pointplot(x="Treatment", y="Expression", data=df, join=False, capsize=0.3, color="Black")
ax= sns.swarmplot(x="Treatment", y="Expression", data=df, palette=pal2, size=10)
for tick, text in zip(ax.get_xticks(), ax.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the mean value for all replicates of either X or Y
    mean_val = df[df['Treatment']==sample_name]["Expression"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax.plot([tick-mean_width/3, tick+mean_width/3], [mean_val, mean_val],
            lw=4, color='black')
ax.tick_params(labelsize=14)
ax.set_ylabel("relative WDFY2 expression (%)", fontsize = 12)
ax.set_xlabel("")

plt.tight_layout()
plt.savefig(savepath)
plt.show()

cat1_wt = df[df['Treatment']=='Scr']
cat1_KO = df[df['Treatment']=='siWDFY2']

stats = ttest_1samp(cat1_KO['Expression'], 100)
dof=(len(cat1_wt)+len(cat1_KO))-2
print("Statistics summary:")
print("p-value: "+ str(stats[1]))
print("t value: "+ str(stats[0]))
print("Degrees of Freedom: " + str(dof))


"""


"""
"""
g = g = sns.violinplot(y="Mean intensity", x="Genotype", data=df, order=["WT","KO"])
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


plt.savefig("d:/Vamp3_EEA1_Normalized.eps")


plt.show()
# generate normalized datafrome

"""