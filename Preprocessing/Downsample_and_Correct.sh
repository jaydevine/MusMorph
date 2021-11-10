#!/bin/bash

# This is a batch isotropic downsampling and intensity correction script. It has a function that will read in the input image resolution, find the scaling factor that relates the this resolution to the (presumably lower) ATLAS resolution, read in the z,y,x voxel lengths, then reduce them to what they should be at the new res. This downsampled image is then corrected for intensity inhomogeneities, and the image values are normalized between 0 and 1. 

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2). Check:
if ! command -v mincresample &> /dev/null
then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit
fi

# Create a variable called FILENAME that calls upon a .txt file (e.g. spec_list.txt) of specimen names. 
FILENAME="/path/to/<PROJECT>/Source/<spec_list.txt>"
# Define atlas file.
ATLAS="/path/to/<PROJECT>/Source/MNC/<.mnc>"

# Start while loop.
while read -r line
do 
	# Input and output name info.
	Biosample="${line}.mnc"
	Biosample_DS="${line}_ds.mnc"
	Biosample_CORR="${line}_ds_corr.mnc"
	Biosample_NORM="${line}_ds_norm.mnc"
	# Alter path to images.
	cd "/path/to/<PROJECT>/Source/Orig"
	echo "Working on ${Biosample} at /path/to/<PROJECT>/Source/Orig."
	# Image dimension info.
	Z=$(mincinfo -dimlength zspace ${Biosample})
	Y=$(mincinfo -dimlength yspace ${Biosample})
	X=$(mincinfo -dimlength xspace ${Biosample})
	Z_START=$(mincinfo ${Biosample} -attvalue zspace:start)
	Y_START=$(mincinfo ${Biosample} -attvalue yspace:start)
	X_START=$(mincinfo ${Biosample} -attvalue xspace:start)
	# Image res info, assuming isotropic res. 
	ATLAS_RES=$(mincinfo ${ATLAS} -attvalue zspace:step)
	IMAGE_RES=$(mincinfo ${Biosample} -attvalue zspace:step)
	SCALAR=$(awk "BEGIN {scale=$ATLAS_RES/$IMAGE_RES; print scale}")
	# Now divide Z,Y,X by SCALAR.
	Z_DS=$(awk "BEGIN {z=$Z/$SCALAR; print int(z+0.5)}")
	Y_DS=$(awk "BEGIN {y=$Y/$SCALAR; print int(y+0.5)}")
	X_DS=$(awk "BEGIN {x=$X/$SCALAR; print int(x+0.5)}")
	# Run resampling.
	mincresample -clobber -zstart ${Z_START} -ystart ${Y_START} -xstart ${X_START} -zstep ${ATLAS_RES} -ystep ${ATLAS_RES} -xstep ${ATLAS_RES} -znelements ${Z_DS} -ynelements ${Y_DS} -xnelements ${X_DS} ${Biosample} ${Biosample_DS}
	# Run intensity correction.
	nu_correct ${Biosample_DS} ${Biosample_CORR}
	rm ${Biosample_DS}
	# Run intensity normalization between 0 and 1. 
	mincnorm -out_floor 0 -out_ceil 1 ${Biosample_CORR} ${Biosample_NORM}
	rm ${Biosample_CORR}
done < "${FILENAME}"
