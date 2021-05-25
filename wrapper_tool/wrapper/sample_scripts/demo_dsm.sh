#!/bin/sh
python fmriDsm.py dataset /home/geethmala/data/small-haxby/bold.nii.gz mask /home/geethmala/data/small-haxby/mask.nii.gz samples /home/geethmala/data/small-haxby/attributes.txt select [1,2,3,4,5,6,7,8] average 
