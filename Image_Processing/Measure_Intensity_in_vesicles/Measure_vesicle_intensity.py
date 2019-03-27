"""
Aim of this script is to segment early and late endosomes (or other compartments) in two channels and measure distribution of a third marker within these segmented populations.
for questions see: Sneeggen et al. or contact kay.oliver.schink@rr-research.no
"""
from ij import IJ
from ij import *
from ij import ImagePlus
from ij import ImageStack
from ij.measure import *
from ij.plugin import *
from ij.process import *
from ij.plugin import ChannelSplitter
from ij.measure import Measurements
from ij.plugin import ImageCalculator
from ij.plugin.frame import RoiManager
from ij.plugin import Duplicator
from ij.process import ImageProcessor
from ij.process import ImageStatistics
from ij.gui import Roi
from ij.gui import PointRoi
import math 
from java.awt import * 
from java.awt import Font
import itertools 
from ij.plugin.filter import MaximumFinder
from ij.measure import ResultsTable
import time



# Indicate channel which should be used for Thresholding

# Save the results automatically as  CSV file ?
automatic_save_results = False

#path for CSV save
savepath = "d:\Marte/Vamp3_EEA1_Lamp_4/measurements/WT/"


# Clear all items from ROI manager

try:
    rm = RoiManager().getInstance()

    
except:
    rm = RoiManager()

rm.runCommand("reset")

channel2_name = "Lamp1"

channel3_name = "EEA1"

channel1_name = "Vamp3"

Threshold_Channel_1 = 2

Threshold_Channel_2 = 3

Measure_Channel = 1



imp1 = IJ.getImage()


# def maxZprojection(stackimp):
#     """ from EMBL python / Fiji cookbook"""
#     allTimeFrames = Boolean.TRUE
#     zp = ZProjector(stackimp)
#     zp.setMethod(ZProjector.MAX_METHOD)
#     zp.doHyperStackProjection()
#     zpimp = zp.getProjection()
#     return zpimp


def DoG(imp0, kernel1, kernel2):
    """Thresholds image and returns thresholded image,
    merge code still quite clumsy but functional"""
    imp1 = imp0.duplicate()
    imp2 = imp0.duplicate()
    IJ.run(imp1, "Gaussian Blur...", "sigma=" + str(kernel1) + " stack")
    IJ.run(imp2, "Gaussian Blur...", "sigma="+ str(kernel2) + " stack")
    ic = ImageCalculator()
    imp3 = ic.run("Subtract create stack", imp1, imp2)
    return imp3





def ExtractChannel(imp, channel):
    imp_height = imp.getHeight()
    imp_width = imp.getWidth()
    channelnumber = imp.getNChannels()
    slicenumber = imp.getNSlices()
    timepoints = imp.getNFrames()
    ExtractedChannel = Duplicator().run(imp, channel, channel, 1, slicenumber, 1, timepoints)
    ExtractedChannel.setTitle("Gallery_Channel_" + str(channel))
    return ExtractedChannel


def Generate_segmented_image(imp, channel):
    imp_Threshold_1 = ExtractChannel(imp1, channel)
    imp_Threshold_1.setTitle(("Threshold" + "Channel" + str(channel)))
    imp_Threshold_1.show()
    IJ.run(imp_Threshold_1, "Median...", "radius=1");
    IJ.run(imp_Threshold_1, "Subtract Background...", "rolling=50");
    IJ.setAutoThreshold(imp_Threshold_1, "Moments dark");
    #Prefs.blackBackground = True;
    IJ.run(imp_Threshold_1, "Convert to Mask", "");
    return imp_Threshold_1


def Generate_segmented_image2(imp, channel):
    imp_Threshold_1 = ExtractChannel(imp1, channel)
    imp_Threshold_1.setTitle(("Threshold" + "Channel" + str(channel)))
    imp_Threshold_1.show()
    IJ.run(imp_Threshold_1, "Median...", "radius=1");
    IJ.run(imp_Threshold_1, "Subtract Background...", "rolling=50");
    IJ.setAutoThreshold(imp_Threshold_1, "MaxEntropy dark");
    #Prefs.blackBackground = True;
    IJ.run(imp_Threshold_1, "Convert to Mask", "");
    return imp_Threshold_1


# segment and measure first Compartment

imp2 = Generate_segmented_image(imp1, 2)

# # # # Generate ROIs by "Analyse Particles"
IJ.run(imp2, "Analyze Particles...", "size=5-Infinity pixel add exclude stack");
IJ.run("Clear Results", "");

#generating results table
ort = ResultsTable() 
ort.setPrecision(1) 
imp_measure = ExtractChannel(imp1, Measure_Channel)
imp_measure.show()


for i, roi in enumerate(RoiManager.getInstance().getRoisAsArray()):
    roi2 = rm.getRoiIndex(roi)
    rm.select(imp_measure, roi2)
    stats = imp_measure.getStatistics(Measurements.MEAN | Measurements.AREA | Measurements.FERET | Measurements.CENTROID)
    ort.incrementCounter()
    ort.addValue("Compartment", (channel2_name))
    ort.addValue("Mean intensity", str(stats.mean))
    ort.addValue("Area", str(stats.area))
    ort.addValue("X_Coordinate", str(stats.xCentroid))
    ort.addValue("Y_Coordinate", str(stats.yCentroid))

time.sleep(0.5)


rm.runCommand("reset")

# segment and measure second Compartment


imp3 = Generate_segmented_image(imp1, 3)
# # # # Generate ROIs by "Analyse Particles"
IJ.run(imp3, "Analyze Particles...", "size=5-Infinity pixel add exclude stack")

for i, roi in enumerate(RoiManager.getInstance().getRoisAsArray()):
    roi2 = rm.getRoiIndex(roi)
    rm.select(imp_measure, roi2)
    stats = imp_measure.getStatistics(Measurements.MEAN | Measurements.AREA | Measurements.FERET | Measurements.CENTROID)
    ort.incrementCounter()
    ort.addValue("Compartment", (channel3_name))
    ort.addValue("Mean intensity", str(stats.mean))
    ort.addValue("Area", str(stats.area))
    ort.addValue("X_Coordinate", str(stats.xCentroid))
    ort.addValue("Y_Coordinate", str(stats.yCentroid))


time.sleep(0.5)

ort.show("Results")

#saving the data

dataname = imp1.getShortTitle()
print dataname
filename_ort = "Measurements_"+dataname+"_001.csv"
savename_ort = savepath+filename_ort # Generate complete savepath
print savename_ort
ort.saveAs(savename_ort) # save

# #####  Cleaning up... ####

imp_measure.changes = False
imp_measure.close()
imp2.changes = False
imp2.close()
imp3.changes = False
imp3.close()

