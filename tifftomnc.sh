#!/bin/bash

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2).

# This script converts a single volume .tiff file into a .mnc file.

# Create a .txt file, say spec_list.txt, with the specimen names in the first column and the original image resolutions in the second column. Use a space to delimit columns.
filename="/path/to/TIFF/<spec_list.txt>"

while read -r line
do
	cd "/path/to/TIFF"
	echo "Working on $spec at /path/to/TIFF"
	# The 'name' variable becomes each line within filename.
	name=( $line )
	echo $name
	spec=${name[0]}
	echo $spec
	res=${name[1]}
	echo $res
	# Define extensions.
	tiff=".tiff"
	mnc=".mnc"
	# Run command.
	itk_convert "$spec$tiff" "$spec$mnc"; minc_modify_header -dinsert xspace:step=$res "$spec$mnc"; minc_modify_header -dinsert yspace:step=$res "$spec$mnc"; minc_modify_header -dinsert zspace:step=$res "$spec$mnc"

done < "$filename"
