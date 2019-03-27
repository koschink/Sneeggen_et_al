"""
This script generates a series of boxes along a freehand line ROI in ImageJ and then extracts the mean intensity in Channel 2 (or the channel indicated in "measure_channel".
for questions see: Sneeggen et al. or contact kay.oliver.schink@rr-research.no
Use Jython in imageJ to run.
"""
from __future__ import division
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
from ij.process import ImageProcessor
from ij.process import ImageStatistics
from ij.plugin import Duplicator
from ij.gui import Roi
from ij.gui import PointRoi
from ij.gui import Line
from ij.gui import PolygonRoi
import math 
from java.awt import * 
from java.awt import Font
import itertools 
from ij.plugin.filter import MaximumFinder
from ij.measure import ResultsTable



try:
    rm = RoiManager().getInstance()

    
except:
    rm = RoiManager()


 ### Insert here how many ROIs you want, i.e. every 5 % would be 20


savepath = " " # insert your savepath here

autosave_results = True # automatically save results to path indicated in "savepath" variable

number_of_rois = 10

roi_width = 25 ### insert here the width of the ROI you want (will be double of that, i.e. the ROI will extend that to either side

measure_channel = 2  # which channel to measure


imp1 = IJ.getImage()

channelname = "Vamp3"


# get the line roi and define where to put boxes

roi0 = imp1.getRoi()

calibration = imp1.getCalibration()
pixelsize = calibration.pixelWidth


coordinates = roi0.getInterpolatedPolygon(int(roi0.getLength()/pixelsize/(number_of_rois)), True)
#coordinates = roi0.getPolygon()
number_of_rois  = coordinates.npoints


point1= (coordinates.xpoints[0], coordinates.ypoints[0])
point2= (coordinates.xpoints[1], coordinates.ypoints[1])

def angle(xy1, xy2):
    diffx = xy2[0]-xy1[0]
    diffy = xy2[1]-xy1[1]
    return math.atan2(diffy, diffx)

def calculate_point(x_orig, y_orig, distance, angle):
	x_new = distance*math.cos(math.radians(angle))+x_orig
	y_new = (distance*math.sin(math.radians(angle))-y_orig)*-1
	return (x_new, y_new)


# Defining the boxes

roi1 = Line(point1[0], point1[1], point2[0],point2[1])


upangle = roi1.getAngle() + 90

downangle = roi1.getAngle() - 90

distance = roi1.getLength()/pixelsize

# calculating the coordinates of the box ROIs
starting_upper_point = (calculate_point(point1[0],point1[1], roi_width, upangle))
starting_lower_point = (calculate_point(point1[0],point1[1], roi_width, downangle))
end_upper_point = (calculate_point(point2[0],point2[1], roi_width, roi1.getAngle()+90))
end_lower_point = (calculate_point(point2[0],point2[1], roi_width, roi1.getAngle()-90))

x_coordinates = [starting_upper_point[0], starting_lower_point[0], end_lower_point[0], end_upper_point[0]]
y_coordinates = [starting_upper_point[1], starting_lower_point[1], end_lower_point[1], end_upper_point[1]]

roi2 = PolygonRoi(x_coordinates, y_coordinates, Roi.POLYGON)
imp1.setRoi(roi2)
rm.addRoi(roi2);

# Generate boxes along line profile and add them to the ROI manager

for i in range(1,(number_of_rois-1)):
    point1= (coordinates.xpoints[i], coordinates.ypoints[i])
    point2= (coordinates.xpoints[i+1], coordinates.ypoints[i+1])
    if i+2 == number_of_rois:
        point3= (coordinates.xpoints[i+1], coordinates.ypoints[i+1]) # for graceful interpolation of angles
    else:
        point3= (coordinates.xpoints[i+2], coordinates.ypoints[i+2]) # for graceful interpolation of angles
    roi4 = Line(point1[0], point1[1], point3[0],point3[1])
    roi1 = Line(point1[0], point1[1], point2[0],point2[1])
    starting_upper_point = end_upper_point
    starting_lower_point = end_lower_point
    end_upper_point = (calculate_point(point2[0],point2[1], roi_width, roi4.getAngle()+90))
    end_lower_point = (calculate_point(point2[0],point2[1], roi_width, roi4.getAngle()-90))

    x_coordinates = [starting_upper_point[0], starting_lower_point[0], end_lower_point[0], end_upper_point[0]]
    y_coordinates = [starting_upper_point[1], starting_lower_point[1], end_lower_point[1], end_upper_point[1]]

    roi2 = PolygonRoi(x_coordinates, y_coordinates, Roi.POLYGON)
    imp1.setRoi(roi2)
    rm.addRoi(roi2);




MeanChannel1 = []

#Iterate through the ROI manager and measure the ROIs in Channel 2

roinumber = RoiManager.getInstance().getCount()
for roi1 in range(roinumber):
    RoiManager().getInstance().select(imp1, roi1)
    imp1.setC(measure_channel)
    roi = imp1.getRoi()
    stats = imp1.getStatistics(Measurements.MEAN | Measurements.AREA | Measurements.FERET | Measurements.CENTROID)
    MeanChannel1.append(stats.mean)


# Generate results table and display results

ort = ResultsTable()
ort.setPrecision(3)

count = len(MeanChannel1)

for i in range(len(MeanChannel1)):
    ort.incrementCounter()
    ort.addValue("ROI", i)
    ort.addValue(channelname, MeanChannel1[i])

ort.show("Measured intensities")

# Save Results in CSV file

if autosave_results:
    dataname = imp1.getShortTitle()
    filename = dataname+"_001.csv"
    savename = savepath+"/"+filename
    ort.saveAs(savename)

rm.runCommand("Deselect");
rm.runCommand("Delete");
