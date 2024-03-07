#!/bin/bash

# This is a batch isotropic downsampling and intensity correction script. It has a function that will read in the input image resolution, find the scaling factor that relates the this resolution to the (presumably lower) ATLAS resolution, read in the z,y,x voxel lengths, then reduce them to what they should be at the new res. This downsampled image is then corrected for intensity inhomogeneities, and the image values are normalized between 0 and 1.

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2). Check:
if ! command -v mincinfo &> /dev/null
then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit
fi

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# You only need to edit the variables within these dashed lines.

# Create a variable called FILENAME that calls upon a .txt file (e.g. spec_list.txt) of specimen names (e.g., "/mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/spec_list.txt").
FILENAME=""
# Define atlas file (include .mnc extension; e.g., "/mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/MNC/Calgary_Adult_Skull_Atlas.mnc")
ATLAS=""
# Define path to MNC files.
MNC_PATH="/path/to/<PROJECT>/Source/MNC/"

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Default values
RESAMPLE="false"
CORRECT_INTENSITY="true"
NORMALIZE_INTENSITY="false"

# Prompt for RESAMPLE option
read -p "Do you want to resample the image to the atlas dimensions and resolution? (true/false, default: true): " input_resample
RESAMPLE=${input_resample:-$RESAMPLE}

# Prompt for CORRECT_INTENSITY option
read -p "Do you want to perform intensity correction? (true/false, default: true): " input_correct_intensity
CORRECT_INTENSITY=${input_correct_intensity:-$CORRECT_INTENSITY}

# Prompt for NORMALIZE_INTENSITY option
read -p "Do you want to perform intensity normalization? (true/false, default: false): " input_normalize_intensity
NORMALIZE_INTENSITY=${input_normalize_intensity:-$NORMALIZE_INTENSITY}

# Start while loop.
while read -r line
do
	# Input and output name info.
	Biosample="${line}.mnc"
	Biosample_DS="${line}_ds.mnc"
	Biosample_CORR="${line}_ds_corr.mnc"
	Biosample_CORR_IMP="${line}_ds_corr.imp"
	Biosample_NORM="${line}_ds_norm.mnc"
	# Alter path to images.
	cd ${PATH}
	echo "Working on ${Biosample}."

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

	# Optional resampling step.
	if [ "$RESAMPLE" == "true" ]; then
            if (( $(echo "$IMAGE_RES < $ATLAS_RES" | bc -l) )); then
            # Upsampling
                SCALAR=$(awk "BEGIN {scale=$IMAGE_RES/$ATLAS_RES; print scale}")
                Z_UP=$(awk "BEGIN {z=$Z*$SCALAR; print int(z+0.5)}")
                Y_UP=$(awk "BEGIN {y=$Y*$SCALAR; print int(y+0.5)}")
                X_UP=$(awk "BEGIN {x=$X*$SCALAR; print int(x+0.5)}")
                mincresample -clobber -zstart ${Z_START} -ystart ${Y_START} -xstart ${X_START} -zstep ${IMAGE_RES} -ystep ${IMAGE_RES} -xstep ${IMAGE_RES} -znelements ${Z_UP} -ynelements ${Y_UP} -xnelements ${X_UP} ${Biosample} ${Biosample_DS}
            else
            # Downsampling
                SCALAR=$(awk "BEGIN {scale=$ATLAS_RES/$IMAGE_RES; print scale}")
                Z_DS=$(awk "BEGIN {z=$Z/$SCALAR; print int(z+0.5)}")
                Y_DS=$(awk "BEGIN {y=$Y/$SCALAR; print int(y+0.5)}")
                X_DS=$(awk "BEGIN {x=$X/$SCALAR; print int(x+0.5)}")
                mincresample -clobber -zstart ${Z_START} -ystart ${Y_START} -xstart ${X_START} -zstep ${ATLAS_RES} -ystep ${ATLAS_RES} -xstep ${ATLAS_RES} -znelements ${Z_DS} -ynelements ${Y_DS} -xnelements ${X_DS} ${Biosample} ${Biosample_DS}
            fi
        else
            Biosample_DS="${Biosample}"
        fi

	# Optional intensity correction step.
	if [ "$CORRECT_INTENSITY" == "true" ]; then
		nu_correct ${Biosample_DS} ${Biosample_CORR}
		rm ${Biosample_DS}
                rm ${Biosample_CORR_IMP}
	else
		Biosample_CORR="${Biosample_DS}"
	fi

	# Optional intensity normalization step.
	if [ "$NORMALIZE_INTENSITY" == "true" ]; then
		mincnorm -out_floor 0 -out_ceil 1 ${Biosample_CORR} ${Biosample_NORM}
		rm ${Biosample_CORR}
	else
		Biosample_NORM="${Biosample_CORR}"
	fi

done < "${FILENAME}"
