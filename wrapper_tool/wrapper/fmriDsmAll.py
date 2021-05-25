#
#  fmriDsmAll.py
#  
#
#  Created by Geethmala Sridaran on 3/5/10.
#  Copyright (c) 2010 Dartmouth College. All rights reserved.
#

from mvpa.suite import *
from nifti import NiftiImage
import sys
import time
import pdb
import scipy.io as sci
import os, glob

minArgCnt = 2
localtime = time.localtime(time.time())

arguments = sys.argv[1:]
count = len(arguments)

# debug
print "arg count:", count

if count < minArgCnt:
    print "fmriDsmAll.py shape <value> matfile <filename> save <filename>"
    sys.exit(0)

matFile = 'avgAll'+str(localtime[0])+str(localtime[1])+str(localtime[2])+str(localtime[3])+str(localtime[4])+'.mat'
filename = 'avgAll'+str(localtime[0])+str(localtime[1])+str(localtime[2])+str(localtime[3])+str(localtime[4])+'.dat'

argci = 1

while argci <= count:
    if sys.argv[argci] == 'shape':
        #pdb.set_trace()
        argci += 1
        r = float(sys.argv[argci])
        c = r
        argci += 1
        continue
    if sys.argv[argci] == 'matfile':
        argci += 1
        matFile = sys.argv[argci]
        argci += 1
        continue
    if sys.argv[argci] == 'save':
        argci += 1
        filename = sys.argv[argci]
        argci += 1
        continue

#pdb.set_trace()        
sumAll = N.zeros((r,c))
for infile in glob.glob('*.dat'):
    print "current file is: " + infile
    sub1DsmArr = N.fromfile(infile,float)
    sub1Dsm = N.reshape(sub1DsmArr,(r,c))
    sumAll = sumAll + sub1Dsm
    
avgAll = sumAll/r

P.imshow(avgAll)
P.colorbar()

if cfg.getboolean('examples', 'interactive', True):
    P.show()


avgAll.tofile(filename)

avgDsmDict = {}

avgDsmDict['dsm'] = avgAll

sci.savemat(matFile,avgDsmDict)
