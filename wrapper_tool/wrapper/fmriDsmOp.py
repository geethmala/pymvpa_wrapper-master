#
#  fmriDsmOp.py
#  
#
#  Created by Geethmala Sridaran on 3/5/10.
#  Copyright (c) 2010 Dartmouth College. All rights reserved.
#


from mvpa.suite import *
import scipy.io as sci
import pdb

if __debug__:
    debug.active += ["SLC"]

matDict = {}

def readFromMatFile(fileName):
    mat_dict = sci.loadmat(fileName)
    return mat_dict

def callApis(dsmObj):

    if dsmObj.reg == 1:

        # load PyMVPA dataset
        attr = SampleAttributes(dsmObj.sampleAttrFile)
        dataset = NiftiDataset(samples=dsmObj.dataFile,
	       labels=attr.labels,
	       chunks=attr.chunks,
	       mask=dsmObj.maskFile)

        if dsmObj.detrend == 1:
            # do chunkswise linear detrending on dataset
            detrend(dataset, perchunk=True, model='linear') 

        if dsmObj.zscore == 1:
            # zscore dataset relative to baseline ('rest') mean
            zscore(dataset, perchunk=True, baselinelabels=[0],
	      targetdtype='float32')

    
        dataset = dataset.selectSamples(
		    N.array([l in dsmObj.labelList for l in dataset.labels],
		       dtype='bool'))

        print dataset.summary()
        samples = dataset.samples
 
        #pdb.set_trace()

        count = 0
        #have to average across labels. new version of pymvpa does this easily
        if dsmObj.avg != 0:
            sortedLab = dataset.uniquelabels       

            c = (dataset.samples.shape)[1]
            print c 
            avgA = N.zeros((len(dataset.uniquelabels),c))
            for i in sortedLab:
	        datasetAvg = dataset.selectSamples(N.array([l in [i] for l in dataset.labels], dtype='bool'))                    
	        #c = (datasetAvg.samples.shape)[1]

	        sum1 = N.zeros((1,c))
	        avg1 = N.zeros((1,c))
	
	        r1 = (datasetAvg.samples.shape)[0]
	        for j in datasetAvg.samples:
	            sum1 += j

	        avg1 = sum1/r1
	        count += 1
	
	        #pdb.set_trace() 
	        #find a better way!
	        if count == 1:
	            avgA = N.vstack(avg1)
	        else:
	            avgA = N.vstack((avgA,avg1))        
	    
            samples = avgA

    #mat file
    else:   
        pdb.set_trace()
        matDict = readFromMatFile(dsmObj.matFile)
        # FIXME(gs): to do

        #modify dict - with comparison 

        #if z == version or header 
        #skip

        # better way?
        #!!!!! can't use this method because matlab has random dictionaries placed in different locations. so this technique does not always work
        #dictCount = 0 #stupid scipy returns random dictionaries. have to keep a count so that we can stop after the second one
        for z in matDict.keys():
            if z == '__version__' or z == '__header__':
                continue
            else:
                samples = matDict[z]
                break
 
            #if dictCount < 1:
                #samples = matDict[z]
                #dictCount += 1
            #else:
                #break
        #sorry, use this for now
        #samples = matDict[dsmObj.dictName] #use the dictionary name which is basically your matlab variable
  
    #pdb.set_trace()  
    dsm = DSMatrix(samples, dsmObj.dsmCorr)

    if dsmObj.dsmDisp == 1:
        P.imshow(dsm.full_matrix, interpolation="nearest", aspect='equal')
        P.colorbar()

        if cfg.getboolean('examples', 'interactive', True):
            P.show()


    dsm.full_matrix.tofile(dsmObj.dsmFile)

        
    if dsmObj.radius != 0.0:
        dsmetric = DSMDatasetMeasure(dsm, dsmObj.dsmMeasure, dsmObj.dsmMeasure)
        sl = Searchlight(dsmetric, radius = dsmObj.radius)
        sl_map = sl(dataset)
        print 'Best performing sphere error:', max(sl_map)
        #can save only for regular files
        if reg == 1:                   
            orig_sl_map = dataset.mapReverse(N.array(sl_map))
            data_hdr = dataset.niftihdr
            NiftiImage(orig_sl_map,header=data_hdr).save(dsmObj.filename)

