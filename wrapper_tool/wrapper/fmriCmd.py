#
#  fmriCmd.py
#  
#
#  Created by Geethmala Sridaran on 1/29/10.
#  Copyright (c) 2010 Dartmouth College. All rights reserved.
#

# Usage:
# fmriCmd.py dataset <filename>
#        samples <filename> mask <filename> 
#        [ classifier <name> <options> ]
#        [ average labels <list> ]
#        [ detrend [perchunk <value> model <name> polyord <value>] ]
#        [ zscore [perchunk <value> pervoxel <value> targetdtype <type>] ]
#        [ select <list> ]
#        [ crossvalidate { oddeven | {nfold <foldval> } | custom [<list of tuples>] } ]
#        [ searchlight <radius> ]
#        [ accuracy ]
#        [ save <filename> ]


import sys
import time
import smlrClass
import knnClass
import svmClass
import blrClass
import enetClass
import gprClass
import larsClass
import plrClass
import rrClass
import fmriClassify
import pdb

# globals
minArgCnt = 6 

class Fmri:
    def __init__(self, localtime):
        self.dataFile = ''
        self.sampleAttrFile = ''
        self.maskFile = ''
        self.classifierName = 'smlr'

        #define by default to access lambda
        smlrObj = smlrClass.Smlr()
        self.classObj = smlrObj
  
        self.detrend = 1 
        self.dPerchunkVal = True
        self.modelName = 'linear'
        self.polyordVal = 3
        self.zscore = 1 
        self.zPerchunkVal = True
        self.baselineLabels = [0]
        self.perVoxelVal = True
        self.targetType = 'float32'
        self.select = 0
        self.labelList = None
        self.cvType = ''
        self.cvFold = 1
        self.searchLight = 0
        self.radius = 4.0
        self.splitList = None
        self.accuracy = 0
        self.chanceLevel = 0.5
        self.avgLabels = None
        self.filename ='file'+str(localtime[0])+str(localtime[1])+str(localtime[2])+str(localtime[3])+str(localtime[4])+'.nii.gz'

    def parseCommand(self, count):
        argci = 1 # argument counter
        #get the data set file
        argci += 1 #better way to do this?
        self.dataFile = sys.argv[argci]
        argci += 2
        self.sampleAttrFile = sys.argv[argci]
        argci += 2
        self.maskFile = sys.argv[argci]
        argci += 1
         
        #pdb.set_trace()
        # exhausted all options here!
        if argci > count:
            argci = count

        if sys.argv[argci] == 'classifier':
            argci += 1
            self.classifierName = sys.argv[argci]
            argci += 1 #check for the options


            # classifier options
            if self.classifierName == 'smlr':
                smlrObj = smlrClass.Smlr()
                if sys.argv[argci] == 'lm':
                    argci += 1 
                    smlrObj.lm = float(sys.argv[argci])
                    argci += 1
                    print argci
                self.classObj = smlrObj #assign a pointer in the current class


            elif self.classifierName == 'knn':
                knnObj = knnClass.Knn()
                # check for options
                # make the options in order to keep the code simple?
                if sys.argv[argci] == 'k':
                    argci += 1
                    knnObj.k = int(sys.argv[argci])
                    argci += 1

                # couldn't give dfx as the option
                if sys.argv[argci] == 'dfx':
                    argci += 1
                    knnObj.dfx = sys.argv[argci]
                    argci += 1
            
                if sys.argv[argci] == 'voting':
                    argci += 1
                    knnObj.voting = sys.argv[argci]
                    argci += 1
                self.classObj = knnObj

            elif self.classifierName == 'svm':
                svmObj = svmClass.Svm()
                if sys.argv[argci] == 'kernel':
                    argci += 1
                    svmObj.kernel = sys.argv[argci]
                    argci += 1
                self.classObj = svmObj

            elif self.classifierName == 'blr':
                blrObj = blrClass.Blr()
                if sys.argv[argci] == 'sigma_noise':
                    argci += 1
                    blrObj.sigmaNoise = float(sys.argv[argci])
                    argci += 1
                self.classObj = blrObj
      
            elif self.classifierName == 'enet':
                enetObj = enetClass.Enet()
                if sys.argv[argci] == 'lm':
                    argci += 1
                    enetObj.lm = float(sys.argv[argci])
                    argci += 1
                self.classObj = enetObj

            # for 'glmnet' and 'LinearCSVMC' nothing
         
            elif self.classifierName == 'gpr':
                gprObj = gprClass.Gpr()
                if sys.argv[argci] == 'kernel':
                    argci += 1
                    gprObj.kernel = sys.argv[argci]
                    argci += 1
                self.classObj = gprObj

            elif self.classifierName == 'lars':
                larsObj = larsClass.Lars()
                if sys.argv[argci] == 'model_type':
                    argci += 1
                    larsObj.modelType = sys.argv[argci]
                    argci += 1
                self.classObj = larsObj

            elif self.classifierName == 'plr':
                plrObj = plrClass.Plr()
                if sys.argv[argci] == 'lm':
                    argci += 1
                    plrObj.lm = int(sys.argv[argci])
                    argci += 1
                self.classObj = plrObj

            elif self.classifierName == 'ridgereg':
                rrObj = rrClass.Rr()
                if sys.argv[argci] == 'lm':
                    argci += 1
                    rrObj.lm = float(sys.argv[argci])
                    self.classObj = rrObj #assign a pointer in the current class
                    argci += 1
                self.classObj = rrObj
      
            # invalid classifer
            else:
                if (self.classifierName != 'glmnet') and (self.classifierName != 'LinearCSVMC'):
                    self.dispErr()


        # optional arguments
        #pdb.set_trace()
        while argci <= count:

            # please keep the arguments in the order specified in man

            if sys.argv[argci] == 'select':
                self.select = 1
                argci += 1
                # has to be a list, otherwise eval throws errors
                self.labelList = eval(sys.argv[argci])
                argci += 1
                continue # do this to make sure your arg count never exceeds the maximum
              
            # fixme(gs): check for the names and isdigit whereever appropriate

            if sys.argv[argci] == 'detrend':
                self.detrend = 1
                argci += 1
                if sys.argv[argci] == 'perchunk':
                    argci += 1
                    self.dPerchunkVal = sys.argv[argci]
                    argci += 1
                if sys.argv[argci] == 'model':
                    argci += 1
                    self.modelName = sys.argv[argci]
                    argci += 1
                if sys.argv[argci] == 'polyord':
                    argci += 1
                    self.polyordVal = int(sys.argv[argci])
                    argci += 1
                continue # do this to make sure your arg count never exceeds the maximum
       
            elif sys.argv[argci] == 'zscore':
                self.zscore = 1
                argci += 1
                if sys.argv[argci] == 'perchunk':
                    argci += 1
                    self.zPerchunkVal = sys.argv[argci]
                    argci += 1
                # fixme(gs): don't know how to pass this as argument
                #if sys.argv[argci] == 'baselinelabels':
                #    argci += 1
                #    self.baselineLabels = sys.argv[argci]                   
                #    argci += 1
                if sys.argv[argci] == 'pervoxel':
                    argci += 1
                    self.perVoxelVal = sys.argv[argci]
                    argci += 1
                if sys.argv[argci] == 'targetdtype':
                    argci += 1
                    self.targetType = sys.argv[argci]
                    argci += 1
                continue # do this to make sure your arg count never exceeds the maximum

            #fixme(gs): write code for averaging

            elif sys.argv[argci] == 'crossvalidate':
                argci += 1
                if sys.argv[argci] == 'oddeven':
                    self.cvType = 'oddeven'

                elif sys.argv[argci] == 'nfold':
                    self.cvType = 'nfold'
                    argci += 1
                    self.cvFold = int(sys.argv[argci])
                    
                elif sys.argv[argci] == 'custom':
                    self.cvType = 'custom'
                    argci += 1
                    # has to be a list of tuples
                    self.splitList = eval(sys.argv[argci])

                argci += 1
                continue # do this to make sure your arg count never exceeds the maximum

            elif sys.argv[argci] == 'searchlight':
                self.searchLight = 1
                argci += 1
                self.radius = float(sys.argv[argci])
                argci += 1
                continue # do this to make sure your arg count never exceeds the maximum
                
            elif sys.argv[argci] == 'accuracy':
                self.accuracy = 1
                argci += 1
                continue # do this to make sure your arg count never exceeds the maximum
                
            #elif sys.argv[argci] == 'chanceLevel':
            #    argci += 1
            #    self.chanceLevel = float(sys.argv[argci])
            #    argci += 1
            #    continue # do this to make sure your arg count never exceeds the maximum

            elif sys.argv[argci] == 'save':
                argci += 1
                self.filename = sys.argv[argci]
                argci += 1
                continue # do this to make sure your arg count never exceeds the maximum
                
            else:
                # call disperr with usage
                argci += 1
                self.dispErr() 

    # to check the values. debug
    def display(self):
        print "Data File:", self.dataFile
        print "Attribute File:", self.sampleAttrFile
        print "Mask File:", self.maskFile
        print "Classifier Name:", self.classifierName
        print "Detrend:", self.detrend
        print "Detrend per chunk value:", self.dPerchunkVal
        print "Detrend model:", self.modelName
        print "Detrend polyord:", self.polyordVal
        print "Zscore:", self.zscore
        print "Zscore per chunk value:", self.zPerchunkVal
        print "Zscore baseline Lables:", self.baselineLabels
        print "Zscore per voxel value:", self.perVoxelVal  
        print "Zscore target type:", self.targetType
        print "Select samples:", self.select
        print "Labels:", self.labelList
        print "Crossvalidation Type:", self.cvType
        print "Nfold value:", self.cvFold
        print "Custom Splitter values:", self.splitList
        print "Searchlight:", self.searchLight
        print "Searchlight radius:", self.radius
        print "Compute Accuracy:", self.accuracy
        #print "Compute above chancelevel:", self.chanceLevel
        print "Filename:", self.filename
       
    def dispClassifier(self):
        if self.classifierName == 'smlr':
            print "SMLR lm:", self.classObj.lm

        elif self.classifierName == 'knn':
            print "kNN k:", self.classObj.k
            print "kNN voting:", self.classObj.voting

        elif self.classifierName == 'svm':
            print "SVM kernel:", self.classObj.kernel

        elif self.classifierName == 'blr':
            print "BLR sigma noise:", self.classObj.sigmaNoise

        elif self.classifierName == 'enet':
            print "ENET lm:", self.classObj.lm

        elif self.classifierName == 'glmnet':
            print "GLMNET: No params"
  
        elif self.classifierName == 'gpr':
            print "GPR kernel:", self.classObj.kernel

        elif self.classifierName == 'lars':
            print "LARS model type:", self.classObj.modelType

        elif self.classifierName == 'plr':
            print "PLR lm:", self.classObj.lm

        elif self.classifierName == 'ridgereg':
            print "Ridge Reg lm:", self.classObj.lm
            
        elif self.classifierName == 'LinearCSVMC':
            print "LinearCSVMC"
        

    def dispErr(self):
        print "Invalid options"
        print "Usage:"
        print "fmriCmd.py dataset <filename>"
        print "           samples <filename> mask <filename>" 
        print "           [ classifier <name> <options> ]" 
        print "           [ detrend [ perchunk <value> model <name> polyord <value> ] ]"
        print "           [ zscore [ perchunk <value> pervoxel <value> targetdtype <type> ] ]"
        print "           [ select <list> ]"
        print "           [ crossvalidate { oddeven | {nfold <foldvalue> } | custom <list> } ]"
        print "           [ searchlight <radius> ]"
        print "           [ accuracy ]"
        #print "           [ chanceLevel <value> ]"
        print "           [ save <filename> ]"

# main function
localtime = time.localtime(time.time())

fmriObj = Fmri(localtime)

# start after fmriCmd.py
arguments = sys.argv[1:]
count = len(arguments)

# debug
print "arg count:", count

if count < minArgCnt:
    fmriObj.dispErr()
    sys.exit(0)

fmriObj.parseCommand(count)

# debug
fmriObj.display()
fmriObj.dispClassifier()

fmriClassify.callApis(fmriObj)

