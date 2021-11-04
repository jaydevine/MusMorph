#!/bin/bash

# This is a batch thresholding script. Oftentimes an image will have background noise, particularly when the specimen has been stained with a contrast agent. When the stain diffuses throughout the scanning medium (e.g. agarose), it can manifest as anatomy. As a result, the registration algorithm will scale and deform background noise instead of the actual anatomy, leading to labelling errors. Using a mask can reduce such errors, but it will not eliminate them altogether, especially if the images are automatically initialized.  

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2). Check:
if ! command -v mincblur &> /dev/null
then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit
fi

# Create a variable called FILENAME that calls upon a .txt file (e.g. spec_list.txt) of specimen names. 
FILENAME="/path/to/<PROJECT>/Source/<>.txt" 

# Start while loop using the images that have been intensity corrected via Downsample_and_Correct.sh. 
while read -r line
do
	# Input name info.
	Biosample="${line}_ds_norm.mnc"
	# Alter path to images.
	cd "/path/to/<PROJECT>/Source/MNC"
	echo "Working on ${Biosample} at /path/to/<PROJECT>/Source/MNC."
	# Get image resolution, assuming isotropic voxels.
	IMAGE_RES=$(mincinfo ${Biosample} -attvalue zspace:step)
	BLUR_RES=$(awk "BEGIN {scale=$IMAGE_RES*1.5; print scale}")
	# Blur file slightly to make intensities more homogeneous for thresholding. 
	mincblur -clobber -fwhm ${BLUR_RES} ${Biosample} ${line}
	# Calc lower density bound for thresholding. Use Kapur or Bimodal metric. Bimodal thresholding is our default.
	BIMODAL=$(mincstats -quiet -biModalT ${line}_blur.mnc)
	ZERO=0
	#KAPUR_STATS=$(mincstats -quiet -kapur ${line}_blur.mnc)
	#KAPUR=$(echo "${KAPUR_STATS}" | tr " " "\n" | sed -n '21p')
	# Calculate upper (max) bound.
	MAX=$(mincstats -max ${line}_blur.mnc)
	# Create mask for individual image. Currently using 8 dilations here, but this can be changed.
	mincmorph -clobber -successive B[${BIMODAL}:${MAX}]DDDDDDDD ${line}_blur.mnc ${line}_blur_mask.mnc 
	# Generate a new image called ${Biosample}_thresh.mnc that only shows the density values in the mask and 0 everywhere else. This will remove background noise.
	minccalc -clobber -expression "if(A[1]<0.5) result=0 else result=A[0]+${ZERO}" ${Biosample} ${line}_blur_mask.mnc  ${Biosample}_thresh.mnc
done < "${FILENAME}"
