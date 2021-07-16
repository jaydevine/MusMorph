#!/bin/bash

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2).

# This script converts a single volume .tiff file into a .mnc file.

# Create a .txt file with the specimen names in the first column and the original image resolutions in the second column. Use a space to delimit columns.
FILENAME="/path/to/TIFF/<spec_list.txt>"

while read -r line
do
	cd "/path/to/TIFF"
	# The 'VAR' variable becomes each line within FILENAME.
	VAR=( $line )
	SpecID=${VAR[0]}
	echo "Working on $SpecID at /path/to/TIFF"
	RES=${VAR[1]}
	echo $RES
	# Define extensions.
	TIFF=".tiff"
	MNC=".mnc"
	# Run command.
	itk_convert "$SpecID$TIFF" "$SpecID$MNC"; minc_modify_header -dinsert xspace:step=$RES "$SpecID$MNC"; minc_modify_header -dinsert yspace:step=$RES "$SpecID$MNC"; minc_modify_header -dinsert zspace:step=$RES "$SpecID$MNC"
done < "$FILENAME"
