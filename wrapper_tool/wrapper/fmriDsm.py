#
#  fmriDsm.py
#  
#
#  Created by Geethmala Sridaran on 3/5/10.
#  Copyright (c) 2010 Dartmouth College. All rights reserved.
#

# Usage:
# fmriDsm.py 
#       [ [[ dataset <filename> mask <filename> samples <filename> ] 
#        [ select <list> ]
#        [ detrend ]
#        [ zscore ]
#        [ average ]] || 
#        [ datamat <filename>] ]
#        [ dsm correlation <name> dsmsave <filename> dsmdisplay ]
#        [ searchlight <radius> dsmmeasure <name> ]
#        [ save <filename> ]


import sys
import time
import pdb
import fmriDsmOp

# globals
minArgCnt = 2 #data file 

class Dsm:
    def __init__(self, localtime):
        self.dataFile = ''
        self.sampleAttrFile = ''
        self.maskFile = ''
        self.detrend = 0 
        self.zscore = 0 
        self.labelList = None
        self.reg = 1
        self.matFile = ''
        #self.dictName = ''
        self.radius = 0.0
        self.dsmMeasure = 'pearson'
        self.avg = 0
        self.dsmCorr = 'spearman'
        self.dsmFile = 'dsm'+str(localtime[0])+str(localtime[1])+str(localtime[2])+str(localtime[3])+str(localtime[4])+'.dat'
        self.dsmDisp = 0 
        self.filename ='file'+str(localtime[0])+str(localtime[1])+str(localtime[2])+str(localtime[3])+str(localtime[4])+'.nii.gz'

    def parseCommand(self, count):
        
        argci = 1 # argument counter
        
        #pdb.set_trace()

        while argci <= count:

            #pdb.set_trace()        
            #get the data set file
            if sys.argv[argci] == 'dataset':
                self.reg = 1 #regular or matlab
                argci += 1
                self.dataFile = sys.argv[argci]
                argci += 2
                #there shoud be a mask and attribute file
                self.maskFile = sys.argv[argci]
                argci += 2
                self.sampleAttrFile = sys.argv[argci]                
                argci += 1 #better way to do this?
                continue
              
       
            if sys.argv[argci] == 'dsm':
                argci += 1
                # optional arguments (please maintain order)
                if sys.argv[argci] == 'correlation':
                    argci += 1
                    self.dsmCorr = sys.argv[argci]
                    argci += 1
                if argci <= count: 
                    if sys.argv[argci] == 'dsmsave':
                        argci += 1
                        self.dsmFile = sys.argv[argci]
                        argci += 1
                if argci <= count: 
                    if sys.argv[argci] == 'dsmdisplay':
                        self.dsmDisp = 1
                        argci += 1
                continue

            if sys.argv[argci] == 'select':
                argci += 1
                # has to be a list, otherwise eval throws errors
                self.labelList = eval(sys.argv[argci])
                argci += 1
                continue
              
            # fixme(gs): check for the names and isdigit whereever appropriate

            if sys.argv[argci] == 'detrend':
                self.detrend = 1
                argci += 1
                continue
              
       
            elif sys.argv[argci] == 'zscore':
                self.zscore = 1
                argci += 1
                continue

            elif sys.argv[argci] == 'average':
                self.avg = 1
                argci += 1
                continue
        
            # matlab file
            elif sys.argv[argci] == 'datamat':
                self.reg = 0
                argci += 1
                self.matFile = sys.argv[argci]
                #argci += 2
                #self.dictName = sys.argv[argci]
                argci += 1
                continue
                
           
            elif sys.argv[argci] == 'searchlight':
                argci += 1
                self.radius = float(sys.argv[argci])
                argci += 1
                if sys.argv[argci] == 'dsmmeasure':
                    argci += 1
                    self.dsmMeasure = sys.argv[argci]
                    argci += 1
                continue
                
            elif sys.argv[argci] == 'save':
                argci += 1
                self.filename = sys.argv[argci]
                argci += 1
                continue
                
            else:
                # call disperr with usage
                argci += 1
                self.dispErr() 

    # to check the values. debug
    def display(self):
        print "Data File:", self.dataFile
        print "Attribute File:", self.sampleAttrFile
        print "Mask File:", self.maskFile
        print "Detrend:", self.detrend
        print "Zscore:", self.zscore
        print "Labels:", self.labelList
        print "Regular(1) or Matlab(0):", self.reg
        print "Matfile:", self.matFile
        #print "Dictname:", self.dictName
        print "Searchlight radius:", self.radius
        print "Searchlight dsmmeasure:", self.dsmMeasure
        print "Average:", self.avg
        print "Dsm correlation:", self.dsmCorr
        print "Dsm filename:", self.dsmFile
        print "Dsm display:", self.dsmDisp  
        print "Filename:", self.filename
             

    def dispErr(self):
        print "Invalid options"
        print "Usage:"
        print "fmriDsm.py"
        print "           [ [[ dataset <filename> mask <filename> samples <filename> ]"
        print "           [ detrend ]"
        print "           [ zscore ]"
        print "           [ select <list> ]"
        print "           [ average ] or "
        print "           [ datamat <filename>] ]"
        print "           [ dsm correlation <name> dsmsave <filename> dsmdisplay ]"
        print "           [ searchlight <radius> dsmmeasure <name> ]"


# main function
localtime = time.localtime(time.time())

dsmObj = Dsm(localtime)

# start after fmriCmd.py
arguments = sys.argv[1:]
count = len(arguments)

# debug
print "arg count:", count

if count < minArgCnt:
    dsmObj.dispErr()
    sys.exit(0)

dsmObj.parseCommand(count)

# debug
dsmObj.display()

fmriDsmOp.callApis(dsmObj)
