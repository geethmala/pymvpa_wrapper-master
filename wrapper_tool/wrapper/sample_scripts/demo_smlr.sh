#!/bin/sh
python fmriCmd.py dataset ../../data/bold.nii.gz samples ../../data/attributes.txt mask ../../data/mask.nii.gz classifier smlr select [1,2,3] crossvalidate oddeven accuracy
