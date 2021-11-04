#!/bin/bash

# This script batch converts TIFF (.tiff) files into MINC (.mnc) files. If you have .tif or .tiff slices, convert the stack to a single volume e.g. using ImageJ. 

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2). Check:
if ! command -v itk_convert &> /dev/null
then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit
fi

# Create a .txt file with the specimen names in the first column, excluding the file extension, and the original image resolutions in the second column. Use a space to delimit columns.
FILENAME="/path/to/<PROJECT>/Source/<>.txt"

# Begin itk_convert loop:
while read -r line
do
	cd "/path/to/<PROJECT>/Source/Orig"
	# The 'VAR' variable becomes each line within FILENAME.
	VAR=( $line )
	Biosample=${VAR[0]}
	echo "Working on $Biosample at /path/to/<PROJECT>/Source/Orig"
	RES=${VAR[1]}
	echo $RES
	# Define extensions.
	TIFF=".tiff"
	MNC=".mnc"
	# Run itk_convert command.
	itk_convert "$Biosample$TIFF" "$Biosample$MNC"; minc_modify_header -dinsert xspace:step=$RES "$Biosample$MNC"; minc_modify_header -dinsert yspace:step=$RES "$Biosample$MNC"; minc_modify_header -dinsert zspace:step=$RES "$Biosample$MNC"
done < "$FILENAME"
