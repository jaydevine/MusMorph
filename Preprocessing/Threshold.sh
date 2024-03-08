#!/bin/bash

# This is a batch thresholding script. Oftentimes an image will have background noise, particularly when the specimen has been stained with a contrast agent. When the stain diffuses throughout the scanning medium (e.g. agarose), it can manifest as anatomy. As a result, the registration algorithm will scale and deform background noise instead of the actual anatomy, leading to labelling errors. Using a mask can reduce such errors, but it will not eliminate them altogether, especially if the images are automatically initialized.  

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2). Check:
if ! command -v mincblur &> /dev/null
then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit
fi

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# You only need to uncomment and edit the variables below if you don't use raw input.

# Create a variable called FILENAME that calls upon a .txt file (e.g. spec_list.txt) of specimen names. 
# FILENAME="/path/to/<PROJECT>/Source/<>.txt"

# Define path to MNC files.
# MNC_PATH="/path/to/<PROJECT>/Source/MNC"

# Prompt for FILENAME
read -p "Enter the path to the file containing the list of specimen names (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/spec_list.txt): " FILENAME

# Prompt for MNC_PATH
read -p "Enter the path to MNC files (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/MNC/): " MNC_PATH

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Start while loop using the images that have been intensity corrected via Downsample_and_Correct.sh. 
while read -r line
do
	# Input name info.
	Biosample="${line}.mnc"
	# Alter path to images.
	cd "$MNC_PATH"
	echo "Working on ${Biosample} at $MNC_PATH."
	# Get image resolution, assuming isotropic voxels.
	IMAGE_RES=$(mincinfo ${Biosample} -attvalue zspace:step)
	BLUR_RES=$(awk "BEGIN {scale=$IMAGE_RES*1.5; print scale}")
	# Blur file slightly to make intensities more homogeneous for thresholding. 
	mincblur -clobber -fwhm ${BLUR_RES} ${Biosample} ${line}
	# Prompt user for thresholding method.
	echo "Select thresholding method: (1) Bimodal or (2) Kapur"
	read -p "Enter your choice (1/2): " choice
	if [ "$choice" == "1" ]; then
		# Calculate lower density bound for thresholding using the Bimodal method.
		BIMODAL=$(mincstats -quiet -biModalT ${line}_blur.mnc)
	elif [ "$choice" == "2" ]; then
		# Calculate lower density bound for thresholding using the Kapur method.
		KAPUR_STATS=$(mincstats -quiet -kapur ${line}_blur.mnc)
		KAPUR=$(echo ${KAPUR_STATS} | tr " " "\n" | sed -n '21p')
	else
		echo "Invalid choice. Defaulting to Bimodal thresholding."
		BIMODAL=$(mincstats -quiet -biModalT ${line}_blur.mnc)
	fi

	ZERO=0
	# Calculate upper (max) bound.
	MAX_STATS=$(mincstats -max ${line}_blur.mnc)
	MAX=$(echo ${MAX_STATS} | cut -d' ' -f2-)
	# Create mask for individual image. Currently using 8 dilations here, but this can be changed.
	mincmorph -clobber -successive B[${BIMODAL}:${MAX}]DDDDDDDD ${line}_blur.mnc ${line}_blur_mask.mnc 
	# Generate a new image called ${Biosample}_thresh.mnc that only shows the density values in the mask and 0 everywhere else. This will remove background noise.
	minccalc -clobber -expression "if(A[1]<0.5) result=0 else result=A[0]+${ZERO}" ${Biosample} ${line}_blur_mask.mnc ${line}_thresh.mnc
done < "${FILENAME}"
