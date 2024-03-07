# This is a Python script for validating and labelling initialized images after non-linearly registering them to an atlas. It will generate a series of Bash scripts that will resample the initialized image into the non-linear atlas space, compare the similarity of the two images, concatenate the registration transformation files, invert them, and propagate the labels to the initialized space using this concatenated transformation. 

# Any compute cluster can be used. To run these scripts, you must install the MINC Toolkit module onto the cluster beforehand, unless one already exists. You will notice here, for example, that we use a module called "minc/1.9.15", which is defined in the Bash header of every script via "module load minc/1.9.15". SLURM identifies the software on the cluster using this line. Other parameters you can play around with are time and memory. To execute these scripts, upload them to your remote /path/to/<PROJECT>/Scripts directory, and run "sbatch Job_Submission_First.sh". The landmark files will end up in /path/to/<PROJECT>/Source/Tag and the segmentations will end up in /path/to/<PROJECT>/Source/Resample. 

# To use OS dependent functionality
import os 
# To read and write data in the .csv format.      
import csv

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PLEASE READ! THE ONLY VARIABLES THAT NEED TO BE EDITED WITHIN THIS SCRIPT ARE BETWEEN THESE DASHED LINES.

# 1) Your local and remote directories must be mapped correctly (i.e., the directories match the variables and "<PROJECT>" should be replaced with your project name);
# 2) Let's assume your local specimen list is called spec_list.txt;
# 3) The Bash (.sh) scripts you generate from running this Python script should be sftp'd into your remote /path/to/<PROJECT>/Scripts directory.

# Create remote directory structure that matches your local structure. E.g.:
# mkdir -p <PROJECT>/{Scripts,Quality,Source/{Blurred,MNC,Orig,Resample,Tag,XFM},lsq6/{Blurred,MNC,XFM},lsq12/{Blurred,MNC,XFM},nl/{Ana_Test,Blurred,INIT,MNC,XFM}}

# Define project name.
PROJECT_NAME = "<PROJECT>"

# Define /path/to/ project on cluster (e..g, /work/hallgrimsson_lab/)
PROJECT_PATH = "/path/to/" + PROJECT_NAME + "/"

# Change the local working directory to print out scripts.
os.chdir("/path/to/<PROJECT>/Scripts")
# Define list of all specimens Here, spec_list.txt is usually a list of 25 specimens. 
All_Specimens = "/path/to/<PROJECT>/Source/spec_list.txt"

# Define atlas file and mask. E.g. the Calgary adult skull atlas:
Atlas = "Calgary_Adult_Skull_Atlas.mnc"
Atlas_Mask = "Calgary_Adult_Skull_Atlas_Mask.mnc"

# Define atlas landmarks. If one of these doesn't exist, leave the string empty "".
Atlas_LM = "Calgary_Adult_Cranium_Atlas_Landmarks.tag"
Atlas_Endo_LM = "Calgary_Adult_Endocast_Atlas_Landmarks.tag"
Atlas_Mand_LM = "Calgary_Adult_Mandible_Atlas_Landmarks.tag"

# Define atlas segmentations. If this doesn't exist, leave the string empty "".
Atlas_Segs = "Calgary_Adult_Skull_Atlas_Segs.mnc"

# Cluster parameters:
Module = "minc/1.9.15"
n_nodes = "1"
Label_Time = "10:00:00"
Label_Mem = "40000M"
Job_Submission_Time = "05-00:00:00"
Job_Submission_Mem = "2000M"

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Define compute cluster paths.
Scripts_path = PROJECT_PATH + "Scripts/"
Quality_path = PROJECT_PATH + "Quality/"
Source_Tag_path = PROJECT_PATH + "Source/Tag/"
Source_Resample_path = PROJECT_PATH + "Source/Resample/"
Source_XFM_path = PROJECT_PATH + "Source/XFM/"
Source_MNC_path = PROJECT_PATH + "Source/MNC/"
lsq6_Blurred_path = PROJECT_PATH + "lsq6/Blurred/"
lsq6_XFM_path = PROJECT_PATH + "lsq6/XFM/"
lsq6_MNC_path = PROJECT_PATH + "lsq6/MNC/"
lsq12_Blurred_path = PROJECT_PATH + "lsq12/Blurred/"
lsq12_XFM_path = PROJECT_PATH + "lsq12/XFM/"
lsq12_MNC_path = PROJECT_PATH + "lsq12/MNC/"
nl_Init_path = PROJECT_PATH + "nl/INIT/"
nl_Blurred_path = PROJECT_PATH + "nl/Blurred/"
nl_XFM_path = PROJECT_PATH + "nl/XFM/"
nl_MNC_path = PROJECT_PATH + "nl/MNC/"

# Define full paths to atlas files.
Atlas_Avg = Source_MNC_path + Atlas
Atlas_Avg_Mask = Source_MNC_path + Atlas_Mask
Atlas_Avg_LM = Source_MNC_path + Atlas_LM
Atlas_Avg_Endo_LM = Source_MNC_path + Atlas_Endo_LM
Atlas_Avg_Mand_LM = Source_MNC_path + Atlas_Mand_LM
Atlas_Avg_Segs = Source_MNC_path + Atlas_Segs

# Open and read ('r') the all specimen list.
Specimen_List=open(All_Specimens,'r')
# Read specimen list as a single string.
Specimens=Specimen_List.read()
# Split the specimens by line to obtain a vector of specimen IDs.
Specimen_IDs=Specimens.split('\n')
# Remove the last blank entry caused by the final \n.
del Specimen_IDs[-1]
# Define the length of the specimen list.
Specimen_List_Length=len(Specimen_IDs)
# Divide the length of the list by the same number.
Specimen_Group=int(Specimen_List_Length/Specimen_List_Length)
# Calculate upper limit of specimen list to use in for loop sequences.
Specimen_Upper=(Specimen_List_Length)-1
# Close the specimen list.
Specimen_List.close()

# Create .sh files for landmarks and segmentations.
# Begin a counter.
Label_Counter=0
for SpecID in Specimen_IDs:
    # Add 1 to the counter for every new file in the loop.
    Label_Counter += 1
    # Open a file to write to; 'a' for append; lsq6_Second is the second stage of .sh scripts to submit.
    Label_Query = open("Label_Query_" + str(Label_Counter) + ".sh",'a')
    # Add header.
    Label_Query.write("#!/bin/bash\n#SBATCH --nodes=" + n_nodes + "\n#SBATCH --mem=" + Label_Mem + "\n#SBATCH --time=" + Label_Time + "\n\nmodule load " + Module + "\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
    Label_Query.write("echo \"Begin the label propagation for " + SpecID + ".\"\n\n")
    # Concatenate the transformation files.
    Label_Query.write("xfmconcat -clobber " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + SpecID + "_lsq12_2.xfm " + nl_XFM_path + SpecID + "_ANTS_nl.xfm " + nl_XFM_path + SpecID + "_origtoANTS_nl.xfm\n")
    # Resample the initialized images into the non-linear atlas space.
    Label_Query.write("mincresample -like " + Atlas_Avg + " -clobber -transformation " + nl_XFM_path + SpecID + "_origtoANTS_nl.xfm " + Source_MNC_path + SpecID + ".mnc "+ nl_MNC_path + SpecID + "_ANTS_nl.mnc\n")
    # Compare the similarity of the resampled image and the atlas. 
    Label_Query.write("echo -e \"" + SpecID + "\n$(minccmp -quiet -mask " + Atlas_Avg_Mask + " -xcorr -rmse " + Atlas_Avg + " " + nl_MNC_path + SpecID + "_ANTS_nl.mnc)\"" + " >> " + Quality_path + SpecID + "_Quality.txt\n")
    # Invert the concatenated transformation file. 
    Label_Query.write("xfminvert -clobber " + nl_XFM_path + SpecID + "_origtoANTS_nl.xfm " + nl_XFM_path + SpecID + "_origtoANTS_nl_inverted.xfm\n")
    # Propagate the atlas landmarks to the initialized space of each image using the inverted transformation file.
    try:
        if Atlas_Avg_LM:
            Label_Query.write("transformtags -vol1 -transformation " + nl_XFM_path + SpecID + "_origtoANTS_nl_inverted.xfm " + Atlas_Avg_LM + " " + Source_Tag_path + SpecID + "_Cranium_Landmarks.tag\n")
    except NameError:
        pass
    try:
        if Atlas_Avg_Endo_LM:
            Label_Query.write("transformtags -vol1 -transformation " + nl_XFM_path + SpecID + "_origtoANTS_nl_inverted.xfm " + Atlas_Avg_Endo_LM + " " + Source_Tag_path + SpecID + "_Endocast_Landmarks.tag\n")
    except NameError:
        pass
    try:
        if Atlas_Avg_Mand_LM:
            Label_Query.write("transformtags -vol1 -transformation " + nl_XFM_path + SpecID + "_origtoANTS_nl_inverted.xfm " + Atlas_Avg_Mand_LM + " " + Source_Tag_path + SpecID + "_Mandible_Landmarks.tag\n")
    except NameError:
        pass
    # Propagate the atlas segmentations to the initialized space of each image using the inverted transformation file. 	
    try:
        if Atlas_Avg_Segs:
            Label_Query.write("mincresample -like " + Atlas_Avg + " -clobber -transform " + nl_XFM_path + SpecID + "_origtoANTS_nl_inverted.xfm " + Atlas_Avg_Segs + " " + Source_Resample_path + SpecID + "_Segs.mnc\n")
    except NameError:
        pass
    Label_Query.write("echo \"The job ended at $(date).\"")
    # Close the file.
    Label_Query.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create master job submission scripts for all stages. These scripts will automatically submit all .sh scripts to the queue and will be chained together.

# Job_Submission_First
Job_Submission_First = open("Job_Submission_First.sh",'a')
Job_Submission_First.write("#!/bin/bash\n#SBATCH --partition=single\n#SBATCH --nodes=" + n_nodes + "\n#SBATCH --mem=" + Job_Submission_Mem + "\n#SBATCH --time=" + Job_Submission_Time + "\n#SBATCH --job-name=Job_Submission_First.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_First.write("cd " + Scripts_path + "\n\n")
Job_Submission_First.write("sleep 10\n\n")
Job_Submission_First.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 1 " + str(Specimen_List_Length) + ")\n\n")
Job_Submission_First.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"Label_Query_$NUM.sh\"\nLabel=\"sbatch $NAME\"\n$Label\necho $Label\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_First.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_First.write("# Create while loop to idle submission script.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 || $(squeue -t PD -u $USER --noheader | wc -l) -ge 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_First.write("#----------------------------------------------------- Remove current submission script from the queue.\n\n")
Job_Submission_First.write("echo \"The job ended at $(date).\"\n")
Job_Submission_First.write("scancel -u $USER --jobname=Job_Submission_First.sh")
