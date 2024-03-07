#!/bin/bash

# This script batch converts NIFTI (.nii) files to MINC (.mnc) files. 

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2). Check:
if ! command -v nii2mnc &> /dev/null
then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit
fi

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# You only need to edit the variables within these dashed lines.

# Create a variable called FILENAME that calls upon a .txt file (e.g. spec_list.txt) of specimen names. 
FILENAME="/path/to/<PROJECT>/Source/<>.txt" 

# Path to original images.
SOURCE_PATH="/path/to/<PROJECT>/Source/Orig"

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------



# Begin nii2mnc loop:
while read -r line
do
	cd "${SOURCE_PATH}"
	# The 'Biosample' variable becomes each line within FILENAME. 
	Biosample="$line"
	echo "Working on $Biosample at ${SOURCE_PATH}"
	NIIFILE="$Biosample.nii"
	MNCFILE="$Biosample.mnc"
	nii2mnc ${NIIFILE} ${MNCFILE} |& tee ./"CT_log_details_${NIIFILE%.*}.txt"
done < "$FILENAME"
