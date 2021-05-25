#
#  fmriClassify.py
#  
#
#  Created by Geethmala Sridaran on 1/29/10.
#  Copyright (c) 2010 Dartmouth College. All rights reserved.
#

from mvpa.suite import *
import time

if __debug__:
    debug.active += ["SLC"]

def callApis(fmriObj):

    # load PyMVPA dataset
    attr = SampleAttributes(fmriObj.sampleAttrFile)
    dataset = NiftiDataset(samples=fmriObj.dataFile,
                       labels=attr.labels,
                       chunks=attr.chunks,
                       mask=fmriObj.maskFile)
    
    if fmriObj.detrend == 1:
        # do chunkswise linear detrending on dataset
        detrend(dataset, perchunk=fmriObj.dPerchunkVal, model=fmriObj.modelName) 

    if fmriObj.zscore == 1:
        # zscore dataset relative to baseline ('rest') mean
        zscore(dataset, perchunk=fmriObj.zPerchunkVal, baselinelabels=fmriObj.baselineLabels,
            targetdtype=fmriObj.targetType)

    if fmriObj.select == 1:
        #type of cv checked outside
        if fmriObj.cvType != '':
           
            dataset = dataset.selectSamples(
                                      N.array([l in fmriObj.labelList for l in dataset.labels],
                                      dtype='bool'))
        #else:
            # do nothin for now
            # fixme(gs): add code to select training and test samples explicity if no cv is performed


    print dataset.summary()
 
    if fmriObj.classifierName == 'smlr':
        clf = SMLR(lm = fmriObj.classObj.lm)

    # couldn't give dfx as the option
    elif fmriObj.classifierName == 'knn':
        clf = kNN(k = fmriObj.classObj.k, voting = fmriObj.classObj.voting)
    
    elif fmriObj.classifierName == 'svm':
        clf = SVM(kernel_type = fmriObj.classObj.kernel)

    # not working with the dataset. memory error
    elif fmriObj.classifierName == 'blr':
        clf = BLR()

    # not defined??
    elif fmriObj.classifierName == 'enet':
        clf = ENET(lm = fmriObj.classObj.lm)

    # not defined???
    elif fmriObj.classifierName == 'glmnet':
        clf = GLMNET_C()

    elif fmriObj.classifierName == 'gpr':
        clf = GPR(kernel = fmriObj.classObj.kernel)

    # not defined??
    elif fmriObj.classifierName == 'lars':
        clf = LARS(model_type = fmriObj.classObj.modelType)

    # some error. may be not using it the right way
    # error: "Regressors for logistic regression should be [0,1]"
    elif fmriObj.classifierName == 'plr':
        clf = PLR()

    # memory error
    elif fmriObj.classifierName == 'ridgereg':
        clf = RidgeReg()
        
    elif fmriObj.classifierName == 'LinearCSVMC':
        clf = LinearCSVMC()


    # setup cross validation procedure, using classifier

    if fmriObj.cvType != '':
    
        if fmriObj.cvType == 'oddeven':
            #print 'here'
            cv = CrossValidatedTransferError(
                         TransferError(clf),
                         OddEvenSplitter())

        elif fmriObj.cvType == 'nfold':
            cv = CrossValidatedTransferError(
                         TransferError(clf),
                         NFoldSplitter(cvtype = fmriObj.cvFold))
        
        # special case. the user can give n splits which means that is the number of 
        # n fold crossvalidation. for each such split, perform the cv and sl and avg 
        # the accuracy values
        # eg: 4 splits, 4-fold
        # fixme(gs): waiting for results, then code this
        elif fmriObj.cvType == 'custom':
            cv = CrossValidatedTransferError(
                         TransferError(clf),
                         CustomSplitter(fmriObj.splitList)
                         )

        if fmriObj.searchLight == 0:
            # and run it
            st = time.time()
            error = cv(dataset)
 
            el = time.time()-st
            print el

            if fmriObj.accuracy == 1:
                error = (1 - error) * 100

            print "Percent correct for %i-fold cross-validation on %i-class problem: %f" \
               % (len(dataset.uniquechunks), len(dataset.uniquelabels), error)

        else:
           sl = Searchlight(cv, radius = fmriObj.radius)
           sl_map = sl(dataset)
           
           if fmriObj.accuracy == 1:
               fmriObj.chanceLevel = 1.0/(len(fmriObj.labelList))
               print fmriObj.chanceLevel
               # can't do map here since can't pass chanceLevel as param               
               # sl_map = map(accMap, sl_map, fmriObj.chanceLevel)
               slMapNew = []       
               for slVal in sl_map:
                   diffVal = ((1.0 - slVal) - fmriObj.chanceLevel)
                   slMapNew.append(diffVal)
               # assign it back
               sl_map = [] # have to do this!
               sl_map = slMapNew        
                  
           orig_sl_map = dataset.mapReverse(N.array(sl_map))
           data_hdr = dataset.niftihdr
           NiftiImage(orig_sl_map,header=data_hdr).save(fmriObj.filename)

    # normal classification
    # fixme(gs): test this with code
    # else:
    #    clf.train(trainDataset)
    #    predict = clf.predict(testDataset.samples)
        
    # how do I save this?
    #    print predict

