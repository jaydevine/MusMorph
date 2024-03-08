#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This is a Python script for pairwise spatial normalization using SyN's non-linear algorithm. It will generate a series of Bash scripts that will pairwise register your images to an atlas. Any compute cluster can be used. To run these scripts, you must install the MINC Toolkit module onto the cluster beforehand, unless one already exists. You will notice here, for example, that we use a module called "minc/1.9.15", which is defined in the Bash header of every script via "module load minc/1.9.15". SLURM identifies the software on the cluster using this line. Other parameters you can play around with are time and memory. 

# The resulting Bash scripts non-linearly register high-resolution mouse images (35 um) to an atlas. Other resolutions can be used, but the blurring and registratation step values need to be scaled accordingly. For instance, if you have 100 um image files, you would just scale the blurring values and the registration step values by a factor of 2. To execute these scripts, upload them to your remote /path/to/<PROJECT>/Scripts directory, and run "sbatch Job_Submission_First.sh". 

# Citation: Percival, C.J., Devine, J., Darwin, B.C., Liu, W., van Eede, M., Henkelman, R.M. and Hallgrimsson, B., 2019. The effect of automated landmark identification on morphometric analyses. J Anat (2019). https://doi.org/10.1111/joa.12973
# Citation: Devine, J., Aponte, J.D., Katz, D.C. et al. A Registration and Deep Learning Approach to Automated Landmark Detection for Geometric Morphometrics. Evol Biol (2020). https://doi.org/10.1007/s11692-020-09508-8

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PLEASE READ! THE ONLY VARIABLES THAT NEED TO BE EDITED WITHIN THIS SCRIPT ARE BETWEEN THESE DASHED LINES.

# Import packages.
import os
import csv

# 1) Your local and remote directories must be mapped correctly (i.e., the directories match the variables and "<PROJECT>" should be replaced with your project name);
# 2) Let's assume your local specimen list is called spec_list.txt;
# 3) Name your initialized source images $spec.mnc, where $spec is the exact name of the specimen annotated in spec_list.txt; 
# 4) The initialized source images, atlas, and atlas mask must be sftp'd into your remote /path/to/$PROJECT_NAME/Source/MNC directory on the cluster before any analyses can begin.
# 5) The Bash (.sh) scripts you generate from running this Python script should be sftp'd into your remote /path/to/$PROJECT_NAME/Scripts directory.

# Define project name on cluster.
PROJECT_NAME = input("Enter project name (e.g., DO): ")

# Define project path on cluster.
CLUSTER_PATH = input("Enter project path on cluster (e.g., /work/hallgrimsson_lab/): ")

# Define full project path on cluster.
PROJECT_PATH = CLUSTER_PATH + PROJECT_NAME + "/"

# Echo reminder to create remote directory structure.
print("\nCreate directory structure on cluster that roughly matches your local structure. E.g.:\n")
print(f"mkdir -p {PROJECT_PATH}{{Scripts,Quality,Source/{{Blurred,MNC,Orig,Resample,Tag,XFM}},lsq6/{{Blurred,MNC,XFM}},lsq12/{{Blurred,MNC,XFM}},nl/{{Ana_Test,Blurred,INIT,MNC,XFM}}}}\n")

# Change the local working directory to print out scripts.
LOCAL_SCRIPT_PATH = input("Enter path to local scripts directory (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Scripts/): ")
os.chdir(LOCAL_SCRIPT_PATH)

# Define path to list specimens Here, spec_list.txt is usually a list of 25 specimens. 
All_Specimens = input("Enter path to listen of specimens (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/spec_list.txt): ")

# Define atlas files.
Atlas = input("Enter name of atlas file (e.g., Calgary_Adult_Skull_Atlas.mnc): ")
Atlas_Mask = input("Enter name of atlas file (e.g., Calgary_Adult_Skull_Atlas_Mask.mnc): ")

# Cluster parameters:
Module = "minc/1.9.15"
n_nodes = "1"
lsq6_Time = "07:00:00"
lsq6_Mem = "25000M"
lsq12_Time = "07:00:00"
lsq12_Mem = "25000M"
nl_Time = "11:00:00"
nl_Mem = "25000M"
Job_Submission_Time = "05-00:00:00"
Job_Submission_Mem = "2000M"

# Echo default parameters.
print("\nThese are the default compute cluster parameters:")
print(f"Module: {Module}")
print(f"Number of nodes: {n_nodes}")
print(f"lsq6 Time: {lsq6_Time}")
print(f"lsq6 Memory: {lsq6_Mem}")
print(f"lsq12 Time: {lsq12_Time}")
print(f"lsq12 Memory: {lsq12_Mem}")
print(f"nl Time: {nl_Time}")
print(f"nl Memory: {nl_Mem}")
print(f"Job Submission Time: {Job_Submission_Time}")
print(f"Job Submission Memory: {Job_Submission_Mem}\n")

# Reminder to change parameters if needed.
print(f"They need to be changed manually if you encounter any errors. Please put these scripts into the {PROJECT_PATH}Scripts directory and all of your image data into the {PROJECT_PATH}Source/MNC/ directory. \n")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Define remote compute cluster paths.
Scripts_path = PROJECT_PATH + "Scripts/"
Source_XFM_path = PROJECT_PATH + "Source/XFM/"
Source_MNC_path = PROJECT_PATH + "Source/MNC/"
Source_Tag_path = PROJECT_PATH + "Source/Tag/"
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

# Define paths to atlas files.
Atlas_Avg = Source_MNC_path + Atlas
Atlas_Avg_Mask = Source_MNC_path + Atlas_Mask

# Define blur files without "_blur" suffix.
Atlas_Avg_Mask_352 = Source_MNC_path + "Atlas_average_mask_352"
Atlas_Avg_Mask_176 = Source_MNC_path + "Atlas_average_mask_176"
Atlas_Avg_Mask_098 = Source_MNC_path + "Atlas_average_mask_098"
Atlas_Avg_Mask_078 = Source_MNC_path + "Atlas_average_mask_078"
Atlas_Avg_Mask_064 = Source_MNC_path + "Atlas_average_mask_064"
Atlas_Avg_Mask_050 = Source_MNC_path + "Atlas_average_mask_050"
Atlas_Avg_352 = lsq6_Blurred_path + "Atlas_average_352"
Atlas_Avg_176 = lsq6_Blurred_path + "Atlas_average_176"
Atlas_Avg_098 = lsq12_Blurred_path + "Atlas_average_098"
Atlas_Avg_078 = lsq6_Blurred_path + "Atlas_average_078"
Atlas_Avg_064 = lsq12_Blurred_path + "Atlas_average_064"
Atlas_Avg_050 = lsq12_Blurred_path + "Atlas_average_050"

# Define blur files with "_blur" suffix.
Atlas_Avg_Mask_352_Blur = Source_MNC_path + "Atlas_average_mask_352_blur.mnc"
Atlas_Avg_Mask_176_Blur = Source_MNC_path + "Atlas_average_mask_176_blur.mnc"
Atlas_Avg_Mask_098_Blur = Source_MNC_path + "Atlas_average_mask_098_blur.mnc"
Atlas_Avg_Mask_078_Blur = Source_MNC_path + "Atlas_average_mask_078_blur.mnc"
Atlas_Avg_Mask_064_Blur = Source_MNC_path + "Atlas_average_mask_064_blur.mnc"
Atlas_Avg_Mask_050_Blur = Source_MNC_path + "Atlas_average_mask_050_blur.mnc"
Atlas_Avg_352_Blur = lsq6_Blurred_path + "Atlas_average_352_blur.mnc"
Atlas_Avg_176_Blur = lsq6_Blurred_path + "Atlas_average_176_blur.mnc"
Atlas_Avg_098_Blur = lsq12_Blurred_path + "Atlas_average_098_blur.mnc"
Atlas_Avg_098_Dxyz = lsq12_Blurred_path + "Atlas_average_098_dxyz.mnc"
Atlas_Avg_078_Blur = lsq6_Blurred_path + "Atlas_average_078_blur.mnc"
Atlas_Avg_064_Blur = lsq12_Blurred_path + "Atlas_average_064_blur.mnc"
Atlas_Avg_050_Blur = lsq12_Blurred_path + "Atlas_average_050_blur.mnc"

# Define blur files with "dxyz" suffix.
Atlas_Avg_Mask_352_Dxyz = Source_MNC_path + "Atlas_average_mask_352_dxyz.mnc"
Atlas_Avg_Mask_176_Dxyz = Source_MNC_path + "Atlas_average_mask_176_dxyz.mnc"
Atlas_Avg_Mask_098_Dxyz = Source_MNC_path + "Atlas_average_mask_098_dxyz.mnc"
Atlas_Avg_Mask_078_Dxyz = Source_MNC_path + "Atlas_average_mask_078_dxyz.mnc"
Atlas_Avg_Mask_064_Dxyz = Source_MNC_path + "Atlas_average_mask_064_dxyz.mnc"
Atlas_Avg_Mask_050_Dxyz = Source_MNC_path + "Atlas_average_mask_050_dxyz.mnc"
Atlas_Avg_352_Dxyz = lsq6_Blurred_path + "Atlas_average_352_dxyz.mnc"
Atlas_Avg_176_Dxyz = lsq6_Blurred_path + "Atlas_average_176_dxyz.mnc"
Atlas_Avg_098_Dxyz = lsq12_Blurred_path + "Atlas_average_098_dxyz.mnc"
Atlas_Avg_078_Dxyz = lsq6_Blurred_path + "Atlas_average_078_dxyz.mnc"
Atlas_Avg_064_Dxyz = lsq12_Blurred_path + "Atlas_average_064_dxyz.mnc"
Atlas_Avg_050_Dxyz = lsq12_Blurred_path + "Atlas_average_050_dxyz.mnc"

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

# Code the strings for iterative blurring via mincblur. -clobber overwrites existing files; -no apodize turns off apodization, which is designed to reduce diffraction edge effects (e.g., detector noise); -gradient calculates the change in intensity of a single pixel in the source image to the target image; -fwhm stands for full-width at half-maximum. In other words, what we want to do is convolve a "smoothing kernel", or Gaussian function, over an input volume in order to average neighboring points. The full-width at half-maximum describes the width of the Gaussian function at half of its peak to the left and right;
MNC_Blur = "mincblur -clobber -no_apodize -gradient -fwhm "

# Code the hierarchical registration strings which call upon the minctracc command. -clobber overwrites existing files; -xcorr stands for cross-correlation, which is the similarity metric to be optimized (maximized); -lsq6 indicates that we want perform a rigid body transformation with six degrees of freedom (translation (z,y,x) and rotation (z,y,x)); -lsq12 indicates that we want to perform a 12-parameter affine transformation with twelve degrees of freedom (translation (z,y,x), rotation (z,y,x), scale (z,y,x), and shear (z,y,x)); -w_translations/rotations/scales/shear optimization weights along z,y,x; -step is the z,y,x resolution; -simplex is the optimizer; -tol is the value at which the optimization stops.
lsq6_Register_352_Blur = "minctracc -clobber -xcorr -lsq6 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.352 0.352 0.352 -simplex 0.78 -use_simplex -tol 0.0001 "
lsq6_Register_176_Blur = "minctracc -clobber -xcorr -lsq6 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.176 0.176 0.176 -simplex 0.54 -use_simplex -tol 0.0001 "
lsq6_Register_078_Blur = "minctracc -clobber -xcorr -lsq6 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.078 0.078 0.078 -simplex 0.32 -use_simplex -tol 0.0001 "
lsq12_Register_098_Blur = "minctracc -clobber -xcorr -lsq12 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.098 0.098 0.098 -simplex 0.980 -use_simplex -tol 0.0001 "
lsq12_Register_064_Blur = "minctracc -clobber -xcorr -lsq12 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.064 0.064 0.064 -simplex 0.490 -use_simplex -tol 0.0001 "
lsq12_Register_050_Blur = "minctracc -clobber -xcorr -lsq12 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.050 0.050 0.050 -simplex 0.333 -use_simplex -tol 0.0001 "

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Begin writing .sh scripts that will be submitted to the cluster.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Blur the atlas file.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Open a file to write to; 'a' for append; lsq6_First is the first 6-parameter .sh script to submit, because it blurs the intended target (i.e., the landmark initialized average) as well as a mask of equivalent resolution to constrain our computation.
Atlas_Blur = open("Atlas_Blur.sh",'a')
# Write standard .sh header. This header is needed for SLURM job submission.
Atlas_Blur.write("#!/bin/bash\n#SBATCH --nodes=" + n_nodes + "\n#SBATCH --mem=" + lsq6_Mem + "\n#SBATCH --time=" + lsq6_Time + "\n\nmodule load " + Module + "\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
# Write commands to blur the atlas file and Atlas_average_mask with isotropic blurring kernels. These blur values should be decided upon with respect to the original resolution of the image. Here, we're assuming 35 micron resolution.
Atlas_Blur.write(MNC_Blur + "0.352 " + Atlas_Avg + " " + Atlas_Avg_352 + "\n")
Atlas_Blur.write(MNC_Blur + "0.176 " + Atlas_Avg + " " + Atlas_Avg_176 + "\n")
Atlas_Blur.write(MNC_Blur + "0.098 " + Atlas_Avg + " " + Atlas_Avg_098 + "\n")
Atlas_Blur.write(MNC_Blur + "0.078 " + Atlas_Avg + " " + Atlas_Avg_078 + "\n")
Atlas_Blur.write(MNC_Blur + "0.064 " + Atlas_Avg + " " + Atlas_Avg_064 + "\n")
Atlas_Blur.write(MNC_Blur + "0.050 " + Atlas_Avg + " " + Atlas_Avg_050 + "\n")
Atlas_Blur.write(MNC_Blur + "0.352 " + Atlas_Avg_Mask + " " + Atlas_Avg_Mask_352 + "\n")
Atlas_Blur.write(MNC_Blur + "0.176 " + Atlas_Avg_Mask + " " + Atlas_Avg_Mask_176 + "\n")
Atlas_Blur.write(MNC_Blur + "0.098 " + Atlas_Avg_Mask + " " + Atlas_Avg_Mask_098 + "\n")
Atlas_Blur.write(MNC_Blur + "0.078 " + Atlas_Avg_Mask + " " + Atlas_Avg_Mask_078 + "\n")
Atlas_Blur.write(MNC_Blur + "0.064 " + Atlas_Avg_Mask + " " + Atlas_Avg_Mask_064 + "\n")
Atlas_Blur.write(MNC_Blur + "0.050 " + Atlas_Avg_Mask + " " + Atlas_Avg_Mask_050 + "\n")
Atlas_Blur.write("echo \"The job ended at $(date).\"")
# Close the file.
Atlas_Blur.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 6-parameter (translation (z,y,x), rotation (z,y,x)) optimal rigid body (affine...) registration stage.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Open a file to write to; 'a' for append; lsq6_Query is the only 6-parameter stage.
# Begin a for loop to blur all landmark initialized source files, register them to , and resample each image into the new translation and rotation invariant space. Note that we ideally want to resample the LM initialized images, rather than the original .mnc images. Hence, the LM .xfm is not included in the concatenation.
# Begin a counter.
lsq6_Counter=0
for SpecID in Specimen_IDs:
# Add 1 to the counter for every new file in the loop.
	lsq6_Counter += 1
	# Open a file to write to; 'a' for append; lsq6_Second is the second stage of .sh scripts to submit.
	lsq6_Query = open("lsq6_Query_" + str(lsq6_Counter) + ".sh",'a')
	# Add header.
	lsq6_Query.write("#!/bin/bash\n#SBATCH --nodes=" + n_nodes + "\n#SBATCH --mem=" + lsq6_Mem + "\n#SBATCH --time=" + lsq6_Time + "\n\nmodule load " + Module + "\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	lsq6_Query.write("echo \"Begin the optimized 6-parameter registration for " + SpecID + ".\"\n\n")
	# Blur each image, as done with the average and average mask, with a 0.352, 0.176, and 0.078 isotropic Gaussian blurring kernel. These blur values should be decided upon with respect to the original resolution of the image.
	lsq6_Query.write(MNC_Blur + "0.352 " + Source_MNC_path + SpecID + ".mnc " + lsq6_Blurred_path + SpecID + "_352\n")
	lsq6_Query.write(MNC_Blur + "0.176 " + Source_MNC_path + SpecID + ".mnc " + lsq6_Blurred_path + SpecID + "_176\n")
	lsq6_Query.write(MNC_Blur + "0.078 " + Source_MNC_path + SpecID + ".mnc " + lsq6_Blurred_path + SpecID + "_078\n")
	# Call registration strings. We begin with the most blurred (e.g., 0.352) image. -model_mask specifies the mask we wish to use. Note that we use a mask with the same amount of blurring; -identity specifies an identity matrix that initializes the transformation matrix. Upon specifying a transformation matrix, we extract the relevant transformation parameters (here, rotation and translation) and optimize them to find the best transformation; -transformation specifies a file giving a previous source to target mapping, which is used as the new coordinate starting point for the optimization.
	lsq6_Query.write(lsq6_Register_352_Blur + lsq6_Blurred_path + SpecID + "_352_blur.mnc " + Atlas_Avg_352_Blur + " " + lsq6_XFM_path + SpecID + "_lsq6_0.xfm -model_mask " + Atlas_Avg_Mask_352_Blur + " -identity\n")
	lsq6_Query.write(lsq6_Register_176_Blur + lsq6_Blurred_path + SpecID + "_176_blur.mnc " + Atlas_Avg_176_Blur + " " + lsq6_XFM_path + SpecID + "_lsq6_1.xfm -model_mask " + Atlas_Avg_Mask_176_Blur + " -transformation " + lsq6_XFM_path + SpecID + "_lsq6_0.xfm\n")
	lsq6_Query.write(lsq6_Register_078_Blur + lsq6_Blurred_path + SpecID + "_078_blur.mnc " + Atlas_Avg_078_Blur + " " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm -model_mask " + Atlas_Avg_Mask_078_Blur + " -transformation " + lsq6_XFM_path + SpecID + "_lsq6_1.xfm\n")
	# Resample the original image into the rotation and translation invariant space using the concatenated transformation. Be mindful of your "original" images and their naming convention.
	lsq6_Query.write("mincresample -like " + Atlas_Avg + " -clobber -transformation " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm " + Source_MNC_path + SpecID + ".mnc " + lsq6_MNC_path + SpecID + "_lsq6.mnc\n\n")
	lsq6_Query.write("echo \"The job ended at $(date).\"")
	# Close the 6-parameter blur/register file.
	lsq6_Query.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 12-parameter (translation (z,y,x), rotation (z,y,x), scale (z,y,x), shear (z,y,x)) optimized affine registration stage.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Open a file to write to; 'a' for append; lsq12_Query is the only 12-parameter stage.
# Begin a for loop to blur all landmark initialized source files, register them to LM_Average, and resample each image into the new translation and rotation invariant space.
# Note that we ideally want to resample the LM initialized images, rather than the original .mnc images. Hence, the LM .xfm is not included in the concatenation.
# Begin a counter.
lsq12_Counter=0
for SpecID in Specimen_IDs:
# Add 1 to the counter for every new file in the loop.
	lsq12_Counter += 1
	# Open a file to write to; 'a' for append; lsq6_Second is the second stage of .sh scripts to submit.
	lsq12_Query = open("lsq12_Query_" + str(lsq12_Counter) + ".sh",'a')
	# Add header.
	lsq12_Query.write("#!/bin/bash\n#SBATCH --nodes=" + n_nodes + "\n#SBATCH --mem=" + lsq12_Mem + "\n#SBATCH --time=" + lsq12_Time + "\n\nmodule load " + Module + "\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	lsq12_Query.write("echo \"Begin the optimized 12-parameter registration for " + SpecID + ".\"\n\n")
	# Blur each image, as done with the average and average mask, with a 0.352, 0.176, and 0.078 isotropic Gaussian blurring kernel. These blur values should be decided upon with respect to the original resolution of the image.
	lsq12_Query.write(MNC_Blur + "0.098 " + lsq6_MNC_path + SpecID + "_lsq6.mnc " + lsq12_Blurred_path + SpecID + "_098\n")
	lsq12_Query.write(MNC_Blur + "0.064 " + lsq6_MNC_path + SpecID + "_lsq6.mnc " + lsq12_Blurred_path + SpecID + "_064\n")
	lsq12_Query.write(MNC_Blur + "0.050 " + lsq6_MNC_path + SpecID + "_lsq6.mnc " + lsq12_Blurred_path + SpecID + "_050\n")
	# Call registration strings. We begin with the most blurred (e.g., 0.352) image. -model_mask specifies the mask we wish to use. Note that we use a mask with the same amount of blurring; -identity specifies an identity matrix that initializes the transformation matrix. Upon specifying a transformation matrix, we extract the relevant transformation parameters (here, rotation and translation) and optimize them to find the best transformation; -transformation specifies a file giving a previous source to target mapping, which is used as the new coordinate starting point for the optimization.
	lsq12_Query.write(lsq12_Register_098_Blur + lsq12_Blurred_path + SpecID + "_098_blur.mnc " + Atlas_Avg_098_Blur + " " + lsq12_XFM_path + SpecID + "_lsq12_0.xfm -model_mask " + Atlas_Avg_Mask_098_Blur + " -identity\n")
	lsq12_Query.write(lsq12_Register_064_Blur + lsq12_Blurred_path + SpecID + "_064_blur.mnc " + Atlas_Avg_064_Blur + " " + lsq12_XFM_path + SpecID + "_lsq12_1.xfm -model_mask " + Atlas_Avg_Mask_064_Blur + " -transformation " + lsq12_XFM_path + SpecID + "_lsq12_0.xfm\n")
	lsq12_Query.write(lsq12_Register_050_Blur + lsq12_Blurred_path + SpecID + "_050_blur.mnc " + Atlas_Avg_050_Blur + " " + lsq12_XFM_path + SpecID + "_lsq12_2.xfm -model_mask " + Atlas_Avg_Mask_050_Blur + " -transformation " + lsq12_XFM_path + SpecID + "_lsq12_1.xfm\n")
	# Concatenate .xfm files.
	lsq12_Query.write("xfmconcat -clobber " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + SpecID + "_lsq12_2.xfm " + lsq12_XFM_path + SpecID + "_origtolsq12.xfm\n")
	# Resample the original image into the rotation and translation invariant space using the concatenated transformation. Be mindful of your "original" images and their naming convention.
	lsq12_Query.write("mincresample -like " + Atlas_Avg + " -clobber -transformation " + lsq12_XFM_path + SpecID + "_origtolsq12.xfm " + Source_MNC_path + SpecID + ".mnc " + lsq12_MNC_path + SpecID + "_lsq12.mnc\n\n")
	lsq12_Query.write("echo \"The job ended at $(date).\"")
	# Close the 12-parameter blur/register file.
	lsq12_Query.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NON-LINEAR STAGE
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create .sh files for non-linear registration.
# Begin a counter.
nl_Counter=0
for SpecID in Specimen_IDs:
# Add 1 to the counter for every new file in the loop.
	nl_Counter += 1
	# Open a file to write to; 'a' for append; lsq6_Second is the second stage of .sh scripts to submit.
	nl_Query = open("nl_Query_" + str(nl_Counter) + ".sh",'a')
	# Add header.
	nl_Query.write("#!/bin/bash\n#SBATCH --nodes=" + n_nodes + "\n#SBATCH --mem=" + nl_Mem + "\n#SBATCH --time=" + nl_Time + "\n\nmodule load " + Module + "\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	nl_Query.write("echo \"Begin the optimized non-linear registration for " + SpecID + ".\"\n\n")
	# Blur each lsq12 image with a 0.098 isotropic Gaussian blurring kernel. These blur values should be decided upon with respect to the original resolution of the image.
	nl_Query.write(MNC_Blur + "0.098 " + lsq12_MNC_path + SpecID + "_lsq12.mnc " + nl_Blurred_path + SpecID + "_098\n")
	# Call the ANTS registration string. -m is the similarity metric (CC is cross-correlation); -x is the mask; -t is the transformation model (SyN is SymmetricNormalization, and is a diffeomorphic transformation); -r is the regularization model (Gaussian); -i is the number of iterations and number of resolution levels; -o is the output transformation.
	nl_Query.write("ANTS 3 --number-of-affine-iterations 0 -m CC[" + lsq12_MNC_path + SpecID + "_lsq12.mnc," + Atlas_Avg + ",1.0,4] -m CC[" + nl_Blurred_path + SpecID + "_098_dxyz.mnc," + Atlas_Avg_098_Dxyz + ",1.0,4] -x [" + Atlas_Avg_Mask_098_Blur + "] -t SyN[0.4] -r Gauss[5,1] -i 100x100x100x0 -o " + nl_XFM_path + SpecID + "_ANTS_nl.xfm\n")
	nl_Query.write("echo \"The job ended at $(date).\"")
	# Close the file.
	nl_Query.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create master job submission scripts for all stages. These scripts will automatically submit all .sh scripts to the queue and will be chained together. In other words, only the first script, Job_Submission_First.sh, needs to be submitted.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Job_Submission_First (i.e., 6-parameter registrations).
Job_Submission_First = open("Job_Submission_First.sh",'a')
Job_Submission_First.write("#!/bin/bash\n#SBATCH --nodes=" + n_nodes + "\n#SBATCH --mem=" + Job_Submission_Mem + "\n#SBATCH --time=" + Job_Submission_Time + "\n#SBATCH --job-name=Job_Submission_First.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_First.write("cd " + Scripts_path + "\n\n")
Job_Submission_First.write("sleep 10\n\n")
Job_Submission_First.write("Atlas_Blur=$(sbatch -W Atlas_Blur.sh | awk '{print $4}')\n\n")
Job_Submission_First.write("until [[ $(squeue -t CD -u $USER --noheader -j ${Atlas_Blur##* } | wc -l) -eq 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_First.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 1 " + str(Specimen_List_Length) + ")\n\n")
Job_Submission_First.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq6_Query_$NUM.sh\"\nLSQ6=\"sbatch $NAME\"\n$LSQ6\necho $LSQ6\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_First.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_First.write("# Create while loop for PD jobs to idle submission script.\nwhile [[ $(squeue -t PD -u $USER --noheader | wc -l) -gt 0 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_First.write("# Create while loop for R jobs to idle submission script.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_First.write("#----------------------------------------------------- Submit next job submission script and remove current submission script from the queue.\n\n")
Job_Submission_First.write("sbatch Job_Submission_Second.sh\n\n")
Job_Submission_First.write("echo \"The job ended at $(date).\"\n")
Job_Submission_First.write("scancel -u $USER --jobname=Job_Submission_First.sh")
# Job_Submission_Second (i.e., 12-parameter registrations).
Job_Submission_Second = open("Job_Submission_Second.sh",'a')
Job_Submission_Second.write("#!/bin/bash\n#SBATCH --nodes=" + n_nodes + "\n#SBATCH --mem=" + Job_Submission_Mem + "\n#SBATCH --time=" + Job_Submission_Time + "\n#SBATCH --job-name=Job_Submission_Second.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Second.write("cd " + Scripts_path + "\n\n")
Job_Submission_Second.write("sleep 10\n\n")
Job_Submission_Second.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 1 " + str(Specimen_List_Length) + ")\n\n")
Job_Submission_Second.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq12_Query_$NUM.sh\"\nLSQ12=\"sbatch $NAME\"\n$LSQ12\necho $LSQ12\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Second.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Second.write("# Create while loop for PD jobs to idle submission script.\nwhile [[ $(squeue -t PD -u $USER --noheader | wc -l) -gt 0 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Second.write("# Create while loop for R jobs to idle submission script.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Second.write("#----------------------------------------------------- Submit next job submission script and remove current submission script from the queue.\n\n")
Job_Submission_Second.write("Job_Submission_Third=$(sbatch Job_Submission_Third.sh)\n\n")
Job_Submission_Second.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Second.write("scancel -u $USER --jobname=Job_Submission_Second.sh")
# Job_Submission_Third (i.e., nl_Fourth non-linear registrations).
Job_Submission_Third = open("Job_Submission_Third.sh",'a')
Job_Submission_Third.write("#!/bin/bash\n#SBATCH --nodes=" + n_nodes + "\n#SBATCH --mem=" + Job_Submission_Mem + "\n#SBATCH --time=" + Job_Submission_Time + "\n#SBATCH --job-name=Job_Submission_Third.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Third.write("cd " + Scripts_path + "\n\n")
Job_Submission_Third.write("sleep 10\n\n")
Job_Submission_Third.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 1 " + str(Specimen_List_Length) + ")\n\n")
Job_Submission_Third.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"nl_Query_$NUM.sh\"\nnl=\"sbatch $NAME\"\n$nl\necho $nl\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Third.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Third.write("# Create while loop for PD jobs to idle submission script.\nwhile [[ $(squeue -t PD -u $USER --noheader | wc -l) -gt 0 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Third.write("# Create while loop for R jobs to idle submission script.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Third.write("#----------------------------------------------------- Remove current submission script from the queue.\n\n")
Job_Submission_Third.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Third.write("scancel -u $USER --jobname=Job_Submission_Third.sh")
