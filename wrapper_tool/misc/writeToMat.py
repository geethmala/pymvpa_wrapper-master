# This script produces a mat file from a dat file
# change the shape appropriately in reshape
# tested only with dissimilarity matrices

from mvpa.suite import *
from nifti import NiftiImage

import scipy.io as sci

avgDsmArr = N.fromfile('cb_io.dat',float)

avgDsm = N.reshape(avgDsmArr,(7,7))

print avgDsm

avgDsmDict = {}

avgDsmDict['dsm'] = avgDsm

sci.savemat('cb_io.mat',avgDsmDict)
