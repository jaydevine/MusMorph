#!/bin/bash

# This script batch converts AIM (.aim) files to MINC (.mnc) files. However, it can also be used to convert other raw image data to MINC.

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2). Check:
if ! command -v rawtominc &> /dev/null
then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit
fi

# Create a variable called FILENAME that calls upon a .txt file (e.g. spec_list.txt) of specimen names. 
FILENAME="/path/to/<PROJECT>/Source/<>.txt" 

# Invoke the montage command to produce an output .png containing images of the newly created .mnc files. 
MONTAGE_CMD="montage -geometry +2+2"

# Begin rawtominc loop:
while read -r line
do
	# The 'Biosample' variable becomes each line within FILENAME. 
	Biosample="$line"
	cd "/path/to/<PROJECT>/Source/Orig"
	echo "Working on $Biosample at /path/to/<PROJECT>/Source/Orig"
	# TXTFILE and AIMFILE use the variable $Biosample, or the line, to define the text and aim files. Thus, each specimen in FILENAME should not have a suffix. 
	TXTFILE="$Biosample.txt"
	AIMFILE="$Biosample.aim"
	# The new .mnc file is sent to /path/to/aim and is given the Biosample $Biosample.mnc. 
	MNCFILE="/path/to/<PROJECT>/Source/Orig/$Biosample.mnc"	
	# Change the .txt header to UNIX format, then use information within the header to automatically produce .mnc files. 
	dos2unix $TXTFILE				
	# Search for offset.
	OFFSET_LINE=`cat $TXTFILE | grep offset`
	# Code the offset line as ARR_OFF.		
	ARR_OFF=($OFFSET_LINE)
	# Extract the offset value from the ARR_OFF variable. Note that ARR_OFF[6] may SLIGHTLY differ between studies based on the header information.
	ACT_OFFSET=${ARR_OFF[6]:0:4}	
	# Search for dim. 
	DIMENSIONS=`cat $TXTFILE | grep -m 1 dim`
	# Code the dim variable as ARR_DIM
	ARR_DIM=($DIMENSIONS)
	# Extract the x, y, z DIMENSIONS from ARR_DIM. Note that ARR_DIM[1], ARR_DIM[2], and ARR_DIM[3] may also SLIGHTLY differ between studies based on the header information. 
	ACT_X=${ARR_DIM[1]}
	ACT_Y=${ARR_DIM[2]}
	ACT_Z=${ARR_DIM[3]}
	# Search for element (i.e., RESOLUTION). 
	RESOLUTION=`cat $TXTFILE | grep element`
	# Code the element line as ARR_RES.
	ARR_RES=($RESOLUTION)
	# Extract the x, y, z RESOLUTION.
	RES_X=${ARR_RES[4]}
	RES_Y=${ARR_RES[5]}
	RES_Z=${ARR_RES[6]}
	# Use the parameters defined above to convert the raw data into a .mnc file.
	rawtominc -input $AIMFILE -short -scan_range -clobber -skip $ACT_OFFSET -xstep $RES_X -ystep $RES_Y -zstep $RES_Z -origin 0 0 0 $MNCFILE $ACT_Z $ACT_Y $ACT_X
	echo "rawtominc -input "$Biosample.aim" -short -scan_range -clobber -skip $ACT_OFFSET -xstep $RES_X -ystep $RES_Y -zstep $RES_Z -origin 0 0 0 "$Biosample.mnc" $ACT_Z $ACT_Y $ACT_X"
	# Create the montage image for all newly created .mnc files.
	cd "/path/to/<PROJECT>/Source/Orig"		
	QCPOST="_QC.png"	
	QCFILE="$Biosample$QCPOST"	
	LABPOST="_QC_labeled.png"
	LABFILE="$Biosample$LABPOST"	
	mincpik -clobber -scale 20 -triplanar "$Biosample.mnc" "$QCFILE"
	convert -label $Biosample "$QCFILE" "$LABFILE"
	# Build full montage command
	MONTAGE_CMD+=" /path/to/<PROJECT>/Source/Orig/$LABFILE"
	echo $MONTAGE_CMD
done < "$FILENAME"
# Create a montage of the converted images. 
MONTAGE_CMD+=" /path/to/<PROJECT>/Source/Orig/<Montage.png>"
$MONTAGE_CMD 
