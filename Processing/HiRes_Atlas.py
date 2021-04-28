# This is a Python script designed to generate an unbiased popoulation average. The script generates a series of bash (.sh) files that should be executed in parallel on a compute cluster. Any compute cluster can be used. To run these scripts, you must install the MINC Toolkit module onto the cluster beforehand, unless one already exists. You will notice here, for example, that we use a module called "minc-toolkit/2016-11", which is defined in the Bash header of every script via "module load minc-toolkit/2016-11". SLURM identifies the software on the cluster using this line. Other parameters you can play around with are time and memory. 

# The resulting Bash scripts non-linearly register high-resolution mouse images (12 um) together. Other resolutions can be used to create an atlas, but the blurring and registratation step values need to be scaled accordingly. For instance, if you have 36 um image files, you would just scale the blurring values and the registration step values by a factor of 3. To execute these scripts, upload them to your remote /path/to/<PROJECT>/Scripts directory, and run "sbatch Job_Submission_First.sh". 

# To use OS dependent functionality.
import os
# To read and write data in the .csv format.
import csv

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# PLEASE READ! THE ONLY VARIABLES THAT NEED TO BE EDITED WITHIN THIS SCRIPT ARE BETWEEN THESE DASHED LINES.

# 1) Your local and remote directories must be mapped correctly (i.e., the directories match the variables and "<PROJECT>" should be replaced with your project name);
# 2) Let's assume your local specimen list is called spec_list.txt;
# 3) Name your initialized source images $spec.mnc, where $spec is the exact name of the specimen annotated in spec_list.txt; 
# 4) Let's assume your initial average and average mask are called LM_average.mnc and LM_average_mask.mnc, respectively;
# 5) The initialized source images, average, and average mask must be sftp'd into your remote /path/to/<PROJECT>/Source/MNC directory on the cluster before any analyses can begin.
# 6) The Bash (.sh) scripts you generate from running this Python script should be sftp'd into your remote /path/to/<PROJECT>/Scripts directory.

#---LOCAL---

# Change the working directory.
os.chdir("/path/to/<PROJECT>/Scripts")
# Define list of all specimens Here, spec_list.txt should be a list of 25 specimens. 
All_Specimens = "/path/to/<PROJECT>/Source/spec_list.txt"

# Create remote directory structure that matches your local structure. E.g.:
# mkdir -p <PROJECT>/{Scripts,Quality,Source/{aim,Resample,Blurred,MNC,Orig,Corr,Tag,Tiff,XFM},lsq6/{Blurred,MNC,XFM},lsq12/{Blurred,MNC,XFM},nl/{Ana_Test,Blurred,INIT,MNC,XFM}}

#---REMOTE---

# Define supercomputer paths.
Scripts_path = "/path/to/<PROJECT>/Scripts/"
Source_XFM_path = "/path/to/<PROJECT>/Source/XFM/"
Source_MNC_path = "/path/to/<PROJECT>/Source/MNC/"
lsq6_Blurred_path = "/path/to/<PROJECT>/lsq6/Blurred/"
lsq6_XFM_path = "/path/to/<PROJECT>/lsq6/XFM/"
lsq6_MNC_path = "/path/to/<PROJECT>/lsq6/MNC/"
lsq12_Blurred_path = "/path/to/<PROJECT>/lsq12/Blurred/"
lsq12_XFM_path = "/path/to/<PROJECT>/lsq12/XFM/"
lsq12_MNC_path = "/path/to/<PROJECT>/lsq12/MNC/"
nl_Init_path = "/path/to/<PROJECT>/nl/INIT/"
nl_Blurred_path = "/path/to/<PROJECT>/nl/Blurred/"
nl_XFM_path = "/path/to/<PROJECT>/nl/XFM/"
nl_MNC_path = "/path/to/<PROJECT>/nl/MNC/"

# Define average files.
LM_Avg = "/path/to/<PROJECT>/Source/MNC/LM_average.mnc"
LM_Avg_Mask = "/path/to/<PROJECT>/Source/MNC/LM_average_mask.mnc"
lsq6_Avg = "/path/to/<PROJECT>/lsq6/<PROJECT>_lsq6_average.mnc"
lsq12_Avg = "/path/to/<PROJECT>/lsq12/<PROJECT>_lsq12_average.mnc"
nl_1_Avg = "/path/to/<PROJECT>/nl/MNC/NL_1_average.mnc"
nl_2_Avg = "/path/to/<PROJECT>/nl/MNC/NL_2_average.mnc"
nl_3_Avg = "/path/to/<PROJECT>/nl/MNC/NL_3_average.mnc"
nl_4_Avg = "/path/to/<PROJECT>/nl/MNC/<PROJECT>_Atlas.mnc"

# Define blur files without "_blur" suffix.
LM_Avg_167 = "/path/to/<PROJECT>/Source/MNC/LM_average_167"
LM_Avg_088 = "/path/to/<PROJECT>/Source/MNC/LM_average_088"
LM_Avg_049 = "/path/to/<PROJECT>/Source/MNC/LM_average_049"
LM_Avg_039 = "/path/to/<PROJECT>/Source/MNC/LM_average_039"
LM_Avg_032 = "/path/to/<PROJECT>/Source/MNC/LM_average_032"
LM_Avg_025 = "/path/to/<PROJECT>/Source/MNC/LM_average_025"
LM_Avg_Mask_400 = "/path/to/<PROJECT>/nl/INIT/LM_average_mask_400"
LM_Avg_Mask_300 = "/path/to/<PROJECT>/nl/INIT/LM_average_mask_300"
LM_Avg_Mask_200 = "/path/to/<PROJECT>/nl/INIT/LM_average_mask_200"
LM_Avg_Mask_100 = "/path/to/<PROJECT>/nl/INIT/LM_average_mask_100"
LM_Avg_Mask_167 = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_167"
LM_Avg_Mask_088 = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_088"
LM_Avg_Mask_049 = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_049"
LM_Avg_Mask_039 = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_039"
LM_Avg_Mask_032 = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_032"
LM_Avg_Mask_025 = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_025"
lsq12_Avg_400 = "/path/to/<PROJECT>/nl/INIT/<PROJECT>_lsq12_average_400"
nl_1_Avg_300 = "/path/to/<PROJECT>/nl/INIT/NL_1_average_300"
nl_2_Avg_200 = "/path/to/<PROJECT>/nl/INIT/NL_2_average_200"
nl_3_Avg_100 = "/path/to/<PROJECT>/nl/INIT/NL_3_average_100"

# Define blur files with "_blur" suffix.
LM_Avg_167_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_167_blur.mnc"
LM_Avg_088_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_088_blur.mnc"
LM_Avg_049_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_049_blur.mnc"
LM_Avg_039_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_039_blur.mnc"
LM_Avg_032_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_032_blur.mnc"
LM_Avg_025_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_025_blur.mnc"
LM_Avg_Mask_400_Blur = "/path/to/<PROJECT>/nl/INIT/LM_average_mask_400_blur.mnc"
LM_Avg_Mask_300_Blur = "/path/to/<PROJECT>/nl/INIT/LM_average_mask_300_blur.mnc"
LM_Avg_Mask_200_Blur = "/path/to/<PROJECT>/nl/INIT/LM_average_mask_200_blur.mnc"
LM_Avg_Mask_100_Blur = "/path/to/<PROJECT>/nl/INIT/LM_average_mask_100_blur.mnc"
LM_Avg_Mask_167_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_167_blur.mnc"
LM_Avg_Mask_088_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_088_blur.mnc"
LM_Avg_Mask_049_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_049_blur.mnc"
LM_Avg_Mask_039_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_039_blur.mnc"
LM_Avg_Mask_032_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_032_blur.mnc"
LM_Avg_Mask_025_Blur = "/path/to/<PROJECT>/Source/MNC/LM_average_mask_025_blur.mnc"
lsq12_Avg_400_Blur = "/path/to/<PROJECT>/nl/INIT/<PROJECT>_lsq12_average_400_blur.mnc"
nl_1_Avg_300_Blur = "/path/to/<PROJECT>/nl/INIT/NL_1_average_300_blur.mnc"
nl_2_Avg_200_Blur = "/path/to/<PROJECT>/nl/INIT/NL_2_average_200_blur.mnc"
nl_3_Avg_100_Blur = "/path/to/<PROJECT>/nl/INIT/NL_3_average_100_blur.mnc"

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Open and read ('r') the specimen list.
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
Specimen_Upper=(Specimen_List_Length*Specimen_List_Length)-1
# Close the specimen list.
Specimen_List.close()

# Code the strings for iterative blurring via mincblur. -clobber overwrites existing files; -no apodize turns off apodization, which is designed to reduce diffraction edge effects (e.g., detector noise); -gradient calculates the change in intensity of a single pixel in the source image to the target image; -fwhm stands for full-width at half-maximum. In other words, what we want to do is convolve a "smoothing kernel", or Gaussian function, over an input volume in order to average neighboring points. The full-width at half-maximum describes the width of the Gaussian function at half of its peak to the left and right;
MNC_Blur = "mincblur -clobber -no_apodize -gradient -fwhm "

# Code the hierarchical registration strings which call upon the minctracc command. -clobber overwrites existing files; -xcorr stands for cross-correlation, which is the similarity metric to be optimized (maximized); -lsq6 indicates that we want perform a rigid body transformation with six degrees of freedom (translation (z,y,x) and rotation (z,y,x)); -lsq12 indicates that we want to perform a 12-parameter affine transformation with twelve degrees of freedom (translation (z,y,x), rotation (z,y,x), scale (z,y,x), and shear (z,y,x)); -w_translations/rotations/scales/shear optimization weights along z,y,x; -step is the z,y,x resolution; -simplex is the optimizer; -tol is the value at which the optimization stops.
lsq6_Register_167_Blur = "minctracc -clobber -xcorr -lsq6 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.167 0.167 0.167 -simplex 0.39 -use_simplex -tol 0.0001 "
lsq6_Register_088_Blur = "minctracc -clobber -xcorr -lsq6 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.088 0.088 0.088 -simplex 0.27 -use_simplex -tol 0.0001 "
lsq6_Register_039_Blur = "minctracc -clobber -xcorr -lsq6 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.039 0.039 0.039 -simplex 0.16 -use_simplex -tol 0.0001 "
lsq12_Register_049_Blur = "minctracc -clobber -xcorr -lsq12 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.049 0.049 0.049 -simplex 0.490 -use_simplex -tol 0.0001 "
lsq12_Register_032_Blur = "minctracc -clobber -xcorr -lsq12 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.032 0.032 0.032 -simplex 0.245 -use_simplex -tol 0.0001 "
lsq12_Register_025_Blur = "minctracc -clobber -xcorr -lsq12 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.025 0.025 0.025 -simplex 0.167 -use_simplex -tol 0.0001 "
nl_1_Register_400_Blur_Begin = "minctracc -clobber -xcorr -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.4 0.4 0.4 -simplex 1.0 -use_simplex -tol 0.0001 "
nl_1_Register_400_Blur_End = "-iterations 40 -similarity 0.8 -weight 0.8 -stiffness 0.98 -nonlinear corrcoeff -sub_lattice 6 -lattice_diameter 1.2 1.2 1.2 -max_def_magnitude 1 -debug -xcorr -identity "
nl_2_Register_300_Blur_Begin = "minctracc -clobber -xcorr -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.3 0.3 0.3 -simplex 1.0 -use_simplex -tol 0.0001 "
nl_2_Register_300_Blur_End = "-iterations 20 -similarity 0.8 -weight 0.8 -stiffness 0.98 -nonlinear corrcoeff -sub_lattice 6 -lattice_diameter 0.8 0.8 0.8 -max_def_magnitude 1 -debug -xcorr -transform "
nl_3_Register_200_Blur_Begin = "minctracc -clobber -xcorr -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.2 0.2 0.2 -simplex 1.0 -use_simplex -tol 0.0001 "
nl_3_Register_200_Blur_End = "-iterations 15 -similarity 0.8 -weight 0.8 -stiffness 0.98 -nonlinear corrcoeff -sub_lattice 6 -lattice_diameter 0.6 0.6 0.6 -max_def_magnitude 1 -debug -xcorr -transform "
nl_4_Register_100_Blur_Begin = "minctracc -clobber -xcorr -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.1 0.1 0.1 -simplex 0.6 -use_simplex -tol 0.0001 "
nl_4_Register_100_Blur_End = "-iterations 15 -similarity 0.8 -weight 0.8 -stiffness 0.98 -nonlinear corrcoeff -sub_lattice 6 -lattice_diameter 0.3 0.3 0.3 -max_def_magnitude 1 -debug -xcorr -transform "

# Beginning of mincbigaverage command to which .mnc files will be added.
lsq6_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
lsq12_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
nl_1_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
nl_2_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
nl_3_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
nl_4_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Begin writing .sh scripts that will be submitted to the cluster.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 6-parameter (translation (z,y,x), rotation (z,y,x)) optimized rigid body registration.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Open a file to write to; 'a' for append; lsq6_First is the first 6-parameter .sh script to submit, because it blurs the intended target (i.e., the landmark initialized average) as well as a mask of equivalent resolution to constrain our computation.
lsq6_First = open("lsq6_First.sh",'a')
# Write standard .sh header. This header is needed for SLURM job submission.
lsq6_First.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=20000M\n#SBATCH --time=05:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
# Write commands to blur LM_average and LM_average_mask with isotropic blurring kernels of 167 microns, 88 microns, and 78 microns. These blur values should be decided upon with respect to the original resolution of the image. Here, we're assuming 35 micron resolution.
lsq6_First.write(MNC_Blur + "0.167 " + LM_Avg + " " + LM_Avg_167 + "\n")
lsq6_First.write(MNC_Blur + "0.088 " + LM_Avg + " " + LM_Avg_088 + "\n")
lsq6_First.write(MNC_Blur + "0.039 " + LM_Avg + " " + LM_Avg_039 + "\n")
lsq6_First.write(MNC_Blur + "0.167 " + LM_Avg_Mask + " " + LM_Avg_Mask_167 + "\n")
lsq6_First.write(MNC_Blur + "0.088 " + LM_Avg_Mask + " " + LM_Avg_Mask_088 + "\n")
lsq6_First.write(MNC_Blur + "0.039 " + LM_Avg_Mask + " " + LM_Avg_Mask_039 + "\n\n")
lsq6_First.write("echo \"The job ended at $(date).\"")
# Close the file.
lsq6_First.close()

# Begin a for loop to blur all landmark initialized source files, register them to LM_Average, and resample each image into the new translation and rotation invariant space.
# Note that we ideally want to resample the LM initialized images (e.g., SpecID_to_Target.mnc), rather than the original .mnc images. Hence, the LM .xfm is not included in the concatenation.
# Begin a counter.
i=0
for SpecID in Specimen_IDs:
	# Add 1 to the counter for every new file in the loop.
	i += 1
	# Open a file to write to; 'a' for append; lsq6_Second is the second stage of .sh scripts to submit.
	lsq6_Second = open("lsq6_Second_" + str(i) + ".sh",'a')
	# Add header.
	lsq6_Second.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=25000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	lsq6_Second.write("echo \"Begin the optimized 6-parameter registration for " + SpecID + ".\"\n\n")
	# Blur each image, as done with the average and average mask, with a 0.167, 0.088, and 0.039 isotropic Gaussian blurring kernel. These blur values should be decided upon with respect to the original resolution of the image.
	lsq6_Second.write(MNC_Blur + "0.167 " + Source_MNC_path + SpecID + ".mnc " + lsq6_Blurred_path + SpecID + "_167\n")
	lsq6_Second.write(MNC_Blur + "0.088 " + Source_MNC_path + SpecID + ".mnc " + lsq6_Blurred_path + SpecID + "_088\n")
	lsq6_Second.write(MNC_Blur + "0.039 " + Source_MNC_path + SpecID + ".mnc " + lsq6_Blurred_path + SpecID + "_039\n")
	# Call registration strings. We begin with the most blurred (e.g., 0.167) image. -model_mask specifies the mask we wish to use. Note that we use a mask with the same amount of blurring; -identity specifies an identity matrix that initializes the transformation matrix. Upon specifying a transformation matrix, we extract the relevant transformation parameters (here, rotation and translation) and optimize them to find the best transformation; -transformation specifies a file giving a previous source to target mapping, which is used as the new coordinate starting point for the optimization.
	lsq6_Second.write(lsq6_Register_167_Blur + lsq6_Blurred_path + SpecID + "_167_blur.mnc " + LM_Avg_167_Blur + " " + lsq6_XFM_path + SpecID + "_lsq6_0.xfm -model_mask " + LM_Avg_Mask_167_Blur + " -identity\n")
	lsq6_Second.write(lsq6_Register_088_Blur + lsq6_Blurred_path + SpecID + "_088_blur.mnc " + LM_Avg_088_Blur + " " + lsq6_XFM_path + SpecID + "_lsq6_1.xfm -model_mask " + LM_Avg_Mask_088_Blur + " -transformation " + lsq6_XFM_path + SpecID + "_lsq6_0.xfm\n")
	lsq6_Second.write(lsq6_Register_039_Blur + lsq6_Blurred_path + SpecID + "_039_blur.mnc " + LM_Avg_039_Blur + " " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm -model_mask " + LM_Avg_Mask_039_Blur + " -transformation " + lsq6_XFM_path + SpecID + "_lsq6_1.xfm\n")
	# Resample the original image into the rotation and translation invariant space using the concatenated transformation. Be mindful of your "original" images and their naming convention.
	lsq6_Second.write("mincresample -like " + LM_Avg + " -clobber -transformation " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm " + Source_MNC_path + SpecID + ".mnc " + lsq6_MNC_path + SpecID + "_lsq6.mnc\n\n")
	lsq6_Second.write("echo \"The job ended at $(date).\"")
	# Close the 6-parameter blur/register file.
	lsq6_Second.close()

# Open a file to write to; 'a' for append; lsq6_Third is the third and final stage of 6-parameter .sh scripts to submit.
lsq6_Third = open("lsq6_Third.sh",'a')
# Add header.
lsq6_Third.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=20000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
lsq6_Third.write("echo \"All lsq6 files are being averaged.\"\n")
# Add _lsq6.mnc files to MNC_Avg string.
for SpecID in Specimen_IDs:
	lsq6_MNC_Avg += lsq6_MNC_path + SpecID + "_lsq6.mnc "
lsq6_Third.write(lsq6_MNC_Avg + lsq6_Avg + "\n\n")
lsq6_Third.write("echo \"The job ended at $(date).\"")
# Close the 6-parameter average file.
lsq6_Third.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 12-parameter (translation (z,y,x), rotation (z,y,x), scale (z,y,x), shear (z,y,x)) optimized affine registration.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Open file to write to; 'a' for append; lsq12_First is the first 12-parameter .sh script to submit, because it blurs the like file (LM_average) and the mask to constrain our computation.
lsq12_First = open("lsq12_First.sh",'a')
# Add header.
lsq12_First.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=20000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
lsq12_First.write("echo \"We are blurring LM_average and LM_average_mask.\"\n")
lsq12_First.write(MNC_Blur + "0.049 " + LM_Avg + " " + LM_Avg_049 + "\n")
lsq12_First.write(MNC_Blur + "0.032 " + LM_Avg + " " + LM_Avg_032 + "\n")
lsq12_First.write(MNC_Blur + "0.025 " + LM_Avg + " " + LM_Avg_025 + "\n")
lsq12_First.write(MNC_Blur + "0.049 " + LM_Avg_Mask + " " + LM_Avg_Mask_049 + "\n")
lsq12_First.write(MNC_Blur + "0.032 " + LM_Avg_Mask + " " + LM_Avg_Mask_032 + "\n")
lsq12_First.write(MNC_Blur + "0.025 " + LM_Avg_Mask + " " + LM_Avg_Mask_025 + "\n\n")
lsq12_First.write("echo \"The job ended at $(date).\"")
# Close the average blur file.
lsq12_First.close()

# Write commands to blur each specimen with isotropic blurring kernels equal in size to those used in lsq12_First.
# Begin a counter.
i=0
for SpecID in Specimen_IDs:
	# Add 1 to the counter for every new file in the loop.
	i += 1
	# Open a file to write to; 'a' for append; lsq12_Second is the second 12-parameter stage designed to blur every specimen in a descending fashion for the hierarchical registration.
	lsq12_Second = open("lsq12_Second_" + str(i) + ".sh",'a')
	# Add header.
	lsq12_Second.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=20000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	lsq12_Second.write("echo \"We are blurring " + SpecID + ".\"\n")
	# Blur the previously created lsq6 images, as done with the average and average mask, with a 0.049, 0.032, and 0.025 isotropic Gaussian blurring kernel. These blur values should be decided upon with respect to the original resolution of the image.
	lsq12_Second.write(MNC_Blur + "0.049 " + lsq6_MNC_path + SpecID + "_lsq6.mnc " + lsq12_Blurred_path + SpecID + "_049\n")
	lsq12_Second.write(MNC_Blur + "0.032 " + lsq6_MNC_path + SpecID + "_lsq6.mnc " + lsq12_Blurred_path + SpecID + "_032\n")
	lsq12_Second.write(MNC_Blur + "0.025 " + lsq6_MNC_path + SpecID + "_lsq6.mnc " + lsq12_Blurred_path + SpecID + "_025\n\n")
	lsq12_Second.write("echo \"The job ended at $(date).\"")
	# Close the 12-parameter blur file.
	lsq12_Second.close()

# Create a single big .sh file containing all of the 12-parameter pairwise registration commands.
# Open a file to write to; 'a' for append; lsq12_Third is the third stage of the 12-parameter stage, where the images are registered to one another. A big script is initially created, then divided specimen by specimen so as to generate many smaller scripts that may be submitted en masse and in parallel on a cluster.
lsq12_Third = open("lsq12_Temp_Big.sh",'a')
for SpecID in Specimen_IDs:
	for SpecID2 in Specimen_IDs:
		# Add header.
		lsq12_Third.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=25000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
		# Call the registration strings. We begin with the most blurred (e.g., 0.049 microns) image. -model_mask specifies the mask we wish to use. Note that we use a -model_mask with the same amount of blurring to constrain our computation. -identity specifies an identity matrix that initializes the transformation matrix. Upon specifying a transformation matrix, we extract the relevant transformation parameters (here, rotation and translation) and optimize them to find the best transformation; -transform specifies a file giving a previous source to target mapping, which is used as the new coordinate starting point for the optimization.
		lsq12_Third.write(lsq12_Register_049_Blur + lsq12_Blurred_path + SpecID + "_049_blur.mnc " + lsq12_Blurred_path + SpecID2 + "_049_blur.mnc " + lsq12_XFM_path + SpecID + "_to_" + SpecID2 + "_lsq12_0.xfm -model_mask " + LM_Avg_Mask_049_Blur + " -identity\n")
		lsq12_Third.write(lsq12_Register_032_Blur + lsq12_Blurred_path + SpecID + "_032_blur.mnc " + lsq12_Blurred_path + SpecID2 + "_032_blur.mnc " + lsq12_XFM_path + SpecID + "_to_" + SpecID2 + "_lsq12_1.xfm -model_mask " + LM_Avg_Mask_032_Blur + " -transform " + lsq12_XFM_path + SpecID + "_to_" + SpecID2 + "_lsq12_0.xfm\n")
		lsq12_Third.write(lsq12_Register_025_Blur + lsq12_Blurred_path + SpecID + "_025_blur.mnc " + lsq12_Blurred_path + SpecID2 + "_025_blur.mnc " + lsq12_XFM_path + SpecID + "_to_" + SpecID2 + "_lsq12_2.xfm -model_mask " + LM_Avg_Mask_025_Blur + " -transform " + lsq12_XFM_path + SpecID + "_to_" + SpecID2 + "_lsq12_1.xfm\n")
		lsq12_Third.write("echo \"The job ended at $(date).\"\n")
# Close the 12-parameter registration file.
lsq12_Third.close()

# Divide the lsq12_Temp_Big.sh file into a series of small lsq12_Third_*.sh files.
# lines_per_file is equal to the number of lines to divide each script into. Note that this MAY vary depending on the cluster and job requirements you're using!
lines_per_file = 15
# Give the smallfile variable null behavior.
smallfile = None
# Open the previously created lsq12_Temp_Big.sh file, refer to it as the bigfile object, and split it into 18 line chunks.
with open("lsq12_Temp_Big.sh") as bigfile:
	for lineno, line in enumerate(bigfile):
		if lineno % lines_per_file == 0:
			if smallfile:
				smallfile.close()
			small_filename = "lsq12_Third_" + str(int(lineno/15)) + ".sh"
			smallfile = open(small_filename, "w")
		smallfile.write(line)
	if smallfile:
			smallfile.close()

# Range should be equal to the number of specimens, because we want a single file for each specimen.
for Element in list(range(Specimen_List_Length)):
	# Open a file to write to; 'a' for append; lsq12_Fourth is the fourth stage of the registration. Upon generating transformation (.xfm) outputs for every specimen, we want to average them, concate the average .xfm with previous .xfm files, and use that total concatenated transformation to resample the original specimen into the 12-parameter space.
	lsq12_Fourth = open("lsq12_Fourth_" + str(Element) + ".sh",'a')
	# Add header.
	lsq12_Fourth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=05:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	# Start XFM_Avg string for each specimen.
	XFM_Avg ="xfmavg -verbose -clobber "
	for SpecID in Specimen_IDs[(Specimen_Group*Element):(Specimen_Group*(Element+1))]:
		for SpecID2 in Specimen_IDs:
			XFM_Avg += lsq12_XFM_path + SpecID + "_to_" + SpecID2 + "_lsq12_2.xfm "
		# Average the added $spec_to_$spec2_lsq12_2.xfm files in the form of $spec_lsq12_AVG.xfm.
		lsq12_Fourth.write(XFM_Avg + lsq12_XFM_path + SpecID + "_lsq12_AVG.xfm\n")
		# Concatenate .xfm files.
		lsq12_Fourth.write("xfmconcat -clobber " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + SpecID + "_lsq12_AVG.xfm " + lsq12_XFM_path + SpecID + "_origtolsq12.xfm\n")
		# Resample source image into 12-parameter space with concatenated .xfm.
		lsq12_Fourth.write("mincresample -like " + LM_Avg + " -clobber -transformation " + lsq12_XFM_path + SpecID + "_origtolsq12.xfm " + Source_MNC_path + SpecID + ".mnc " + lsq12_MNC_path + SpecID + "_lsq12.mnc\n\n")
	lsq12_Fourth.write("echo \"The job ended at $(date).\"")
	# Close the xfmconcat and resample file.
	lsq12_Fourth.close()

# Create .mnc average script for specimens.
# Open a file to write to; 'a' for append; lsq12_Fifth is the fifth and final stage of the 12-parameter affine registration. After creating the lsq12 resampled .mnc images, we average these to create a target for non-linear deformations.
lsq12_Fifth = open("lsq12_Fifth.sh",'a')
# Add header.
lsq12_Fifth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=20000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
lsq12_Fifth.write("echo \"All lsq12 files are being averaged.\"\n")
for SpecID in Specimen_IDs:
	# Add the new $spec_lsq12.mnc files to the Avg_String variable.
	lsq12_MNC_Avg += lsq12_MNC_path + SpecID + "_lsq12.mnc "
lsq12_Fifth.write(lsq12_MNC_Avg + lsq12_Avg + "\n\n")
lsq12_Fifth.write("echo \"The job ended at $(date).\"")
# Close the average file.
lsq12_Fifth.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# FIRST NON-LINEAR STAGE (includes nl_First.sh, nl_Second_*.sh, and nl_Third.sh)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Open a file to write to; 'a' for append; nl_First is the first non-linear deformation script, where we blur the 12-parameter average and mask with the largest blurring kernels.
nl_First = open("nl_First.sh",'a')
# Add header.
nl_First.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=20000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
# Blur the average and average mask with different kernels. Observe that these blurs (1.4mm), relative to those at the 12-parameter stage, are much larger.
nl_First.write(MNC_Blur + "0.4 " + lsq12_Avg + " " + lsq12_Avg_400 + "\n")
nl_First.write(MNC_Blur + "0.4 " + LM_Avg_Mask + " " + LM_Avg_Mask_400 + "\n\n")
nl_First.write("echo \"The job ended at $(date).\"")
nl_First.close()

# Create .sh files for the first round of non-linear commands (nl_1).
for Element in list(range(Specimen_List_Length)):
	# Open a file to write to; 'a' for append; nl_Second includes the non-linear registrations of the most blurred images.
	nl_Second = open("nl_Second_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Second.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=25000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for SpecID in Specimen_IDs[(Specimen_Group*Element):(Specimen_Group*(Element+1))]:
		# Blur string.
		nl_Second.write(MNC_Blur + "0.4 " + lsq12_MNC_path + SpecID + "_lsq12.mnc " + nl_Blurred_path + SpecID + "_400\n")
		# Registration string.
		nl_Second.write(nl_1_Register_400_Blur_Begin + nl_Blurred_path + SpecID + "_400_blur.mnc " + lsq12_Avg_400_Blur + " " + nl_XFM_path + SpecID + "_nl_1.xfm -model_mask " + LM_Avg_Mask_400_Blur + " " + nl_1_Register_400_Blur_End + "\n")
		# Concatenate .xfm files.
		nl_Second.write("xfmconcat -clobber " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + SpecID + "_lsq12_AVG.xfm " + nl_XFM_path + SpecID + "_nl_1.xfm " + nl_XFM_path + SpecID + "_origtonl_1.xfm\n")
		# Resample source image into the first on-linear space with concatenated .xfm.
		nl_Second.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + SpecID + "_origtonl_1.xfm " + Source_MNC_path + SpecID + ".mnc "+ nl_MNC_path + SpecID + "_nl_1.mnc\n\n")
	nl_Second.write("echo \"The job ended at $(date).\"")
	# Close the file.
	nl_Second.close()

# Average the non-linear files from the first set of deformations.
for SpecID in Specimen_IDs:
	nl_1_MNC_Avg += nl_MNC_path + SpecID + "_nl_1.mnc "
# Open a file to write to; 'a' for append; nl_Third is the averaging of all nl_Second images to create a target for the next set of non-linear deformations.
nl_Third = open("nl_Third.sh",'a')
# Add header.
nl_Third.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=25000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
nl_Third.write("echo \"All of the first non-linearly deformed files are being averaged.\"\n")
nl_Third.write(nl_1_MNC_Avg + nl_1_Avg + "\n\n")
# Blur string for the average and average mask.
nl_Third.write("echo \"Blur this first non-linear average, as it will become the target in the next set of the hierarchical non-linear deformations.\"\n")
nl_Third.write(MNC_Blur + "0.3 " + nl_1_Avg + " " + nl_1_Avg_300 + "\n")
nl_Third.write(MNC_Blur + "0.3 " + LM_Avg_Mask + " " + LM_Avg_Mask_300 + "\n\n")
nl_Third.write("echo \"The job ended at $(date).\"")
# Close the script.
nl_Third.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# SECOND NON-LINEAR STAGE (includes nl_Fourth_*.sh and nl_Fifth.sh)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create .sh files for the second round of non-linear commands (nl_2).
for Element in list(range(Specimen_List_Length)):
	# Open a file to write to; 'a' for append; nl_Fourth includes the non-linear registrations of the second most blurred images.
	nl_Fourth = open("nl_Fourth_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Fourth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=25000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for SpecID in Specimen_IDs[(Specimen_Group*Element):(Specimen_Group*(Element+1))]:
		# Blur string.
		nl_Fourth.write(MNC_Blur + "0.3 " + lsq12_MNC_path + SpecID + "_lsq12.mnc " + nl_Blurred_path + SpecID + "_300\n")
		# Registration string.
		nl_Fourth.write(nl_2_Register_300_Blur_Begin + nl_Blurred_path + SpecID + "_300_blur.mnc " + nl_1_Avg_300_Blur + " " + nl_XFM_path + SpecID + "_nl_2.xfm -model_mask " + LM_Avg_Mask_300_Blur + " " + nl_2_Register_300_Blur_End + nl_XFM_path + SpecID + "_nl_1.xfm\n")
		# Concatenate .xfm files.
		nl_Fourth.write("xfmconcat -clobber " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + SpecID + "_lsq12_AVG.xfm " + nl_XFM_path + SpecID + "_nl_2.xfm " + nl_XFM_path + SpecID + "_origtonl_2.xfm\n")
		# Resample source image into the second non-linear space with concatenated .xfm.
		nl_Fourth.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + SpecID + "_origtonl_2.xfm " + Source_MNC_path + SpecID + ".mnc "+ nl_MNC_path + SpecID + "_nl_2.mnc\n\n")
	nl_Fourth.write("echo \"The job ended at $(date).\"")
	# Close the file.
	nl_Fourth.close()

# Average the non-linear files from the first set of deformations.
for SpecID in Specimen_IDs:
	nl_2_MNC_Avg += nl_MNC_path + SpecID + "_nl_2.mnc "
# Open a file to write to; 'a' for append; nl_Fifth is the averaging of all nl_Fourth images to create a target for the next set of non-linear deformations.
nl_Fifth = open("nl_Fifth.sh",'a')
# Add header.
nl_Fifth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=25000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
nl_Fifth.write("echo \"All of the second non-linearly deformed files are being averaged.\"\n")
nl_Fifth.write(nl_2_MNC_Avg + nl_2_Avg + "\n\n")
# Blur string for the average and average mask.
nl_Fifth.write("echo \"Blur this second non-linear average, as it will become the target in the next set of the hierarchical non-linear deformations.\"\n")
nl_Fifth.write(MNC_Blur + "0.2 " + nl_2_Avg + " " + nl_2_Avg_200 + "\n")
nl_Fifth.write(MNC_Blur + "0.2 " + LM_Avg_Mask + " " + LM_Avg_Mask_200 + "\n\n")
nl_Fifth.write("echo \"The job ended at $(date).\"")
# Close the NL_4 end script.
nl_Fifth.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# THIRD NON-LINEAR STAGE (includes nl_Sixth_*.sh and nl_Seventh.sh)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create .sh files for the third round of non-linear commands (nl_3).
for Element in list(range(Specimen_List_Length)):
	# Open a file to write to; 'a' for append; nl_Sixth includes the non-linear registrations of the third most blurred images.
	nl_Sixth = open("nl_Sixth_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Sixth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=25000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for SpecID in Specimen_IDs[(Specimen_Group*Element):(Specimen_Group*(Element+1))]:
		# Blur string.
		nl_Sixth.write(MNC_Blur + "0.2 " + lsq12_MNC_path + SpecID + "_lsq12.mnc " + nl_Blurred_path + SpecID + "_200\n")
		# Registration string.
		nl_Sixth.write(nl_3_Register_200_Blur_Begin + nl_Blurred_path + SpecID + "_200_blur.mnc " + nl_2_Avg_200_Blur + " " + nl_XFM_path + SpecID + "_nl_3.xfm -model_mask " + LM_Avg_Mask_200_Blur + " " + nl_3_Register_200_Blur_End + nl_XFM_path + SpecID + "_nl_2.xfm\n")
		# Concatenate .xfm files.
		nl_Sixth.write("xfmconcat -clobber " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + SpecID + "_lsq12_AVG.xfm " + nl_XFM_path + SpecID + "_nl_3.xfm " + nl_XFM_path + SpecID + "_origtonl_3.xfm\n")
		# Resample source image into third non-linear space with concatenated .xfm.
		nl_Sixth.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + SpecID + "_origtonl_3.xfm " + Source_MNC_path + SpecID + ".mnc "+ nl_MNC_path + SpecID + "_nl_3.mnc\n\n")
	nl_Sixth.write("echo \"The job ended at $(date).\"")
	# Close the script.
	nl_Sixth.close()

# Average the non-linear files from the third set of deformations.
for SpecID in Specimen_IDs:
	nl_3_MNC_Avg += nl_MNC_path + SpecID + "_nl_3.mnc "
# Open a file to write to; 'a' for append; nl_Seventh is the averaging of all nl_Sixth images to create a target for the final non-linear deformation.
nl_Seventh = open("nl_Seventh.sh",'a')
# Add header.
nl_Seventh.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=25000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
nl_Seventh.write("echo \"All of the third non-linearly deformed files are being averaged.\"\n")
nl_Seventh.write(nl_3_MNC_Avg + nl_3_Avg + "\n\n")
# Blur string for the average and average mask.
nl_Seventh.write("echo \"Blur this third non-linear average, as it will become the target in the next set of the hierarchical non-linear deformations.\"\n")
nl_Seventh.write(MNC_Blur + "0.1 " + nl_3_Avg + " " + nl_3_Avg_100 + "\n")
nl_Seventh.write(MNC_Blur + "0.1 " + LM_Avg_Mask + " " + LM_Avg_Mask_100 + "\n\n")
nl_Seventh.write("echo \"The job ended at $(date).\"")
# Close the script.
nl_Seventh.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# FOURTH NON-LINEAR STAGE (includes nl_Sixth_*.sh and nl_Seventh.sh)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create .sh files for the third round of non-linear commands (nl_3).
for Element in list(range(Specimen_List_Length)):
	# Open a file to write to; 'a' for append; nl_Eighth includes the non-linear registrations of the fourth most (least) blurred images.
	nl_Eighth = open("nl_Eighth_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Eighth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=25000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for SpecID in Specimen_IDs[(Specimen_Group*Element):(Specimen_Group*(Element+1))]:
		# Blur string.
		nl_Eighth.write(MNC_Blur + "0.1 " + lsq12_MNC_path + SpecID + "_lsq12.mnc " + nl_Blurred_path + SpecID + "_100\n")
		# Registration string.
		nl_Eighth.write(nl_4_Register_100_Blur_Begin + nl_Blurred_path + SpecID + "_100_blur.mnc " + nl_3_Avg_100_Blur + " " + nl_XFM_path + SpecID + "_nl_4.xfm -model_mask " + LM_Avg_Mask_100_Blur + " " + nl_4_Register_100_Blur_End + nl_XFM_path + SpecID + "_nl_3.xfm\n")
		# Concatenate .xfm files.
		nl_Eighth.write("xfmconcat -clobber " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + SpecID + "_lsq12_AVG.xfm " + nl_XFM_path + SpecID + "_nl_4.xfm " + nl_XFM_path + SpecID + "_origtonl_4.xfm\n")
		# Resample source image into third non-linear space with concatenated .xfm.
		nl_Eighth.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + SpecID + "_origtonl_4.xfm " + Source_MNC_path + SpecID + ".mnc "+ nl_MNC_path + SpecID + "_nl_4.mnc\n\n")
	nl_Eighth.write("echo \"The job ended at $(date).\"")
	# Close the script.
	nl_Eighth.close()

# Average the non-linear files from the third set of deformations.
for SpecID in Specimen_IDs:
	nl_4_MNC_Avg += nl_MNC_path + SpecID + "_nl_4.mnc "
# Open a file to write to; 'a' for append; nl_Ninth is the averaging of all nl_Eighth images to create a final average atlas to be labelled.
nl_Ninth = open("nl_Ninth.sh",'a')
# Add header.
nl_Ninth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=20000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
nl_Ninth.write("echo \"All of the fourth non-linearly deformed files are being averaged.\"\n")
nl_Ninth.write(nl_4_MNC_Avg + nl_4_Avg + "\n\n")
nl_Ninth.write("echo \"The job ended at $(date).\"")
# Close the script.
nl_Ninth.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create master job submission scripts for all stages. These scripts will automatically submit all .sh scripts to the queue and will be chained together. In other words, only the first script, Job_Submission_First.sh, needs to be submitted.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Job_Submission_First (i.e., 6-parameter blurs, registrations, concatenations, resamplings, and the average).
Job_Submission_First = open("Job_Submission_First.sh",'a')
Job_Submission_First.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_First.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_First.write("cd " + Scripts_path + "\n\n")
Job_Submission_First.write("sleep 10\n\n")
Job_Submission_First.write("lsq6_First=$(sbatch lsq6_First.sh)\n\n")
Job_Submission_First.write("until [[ $(squeue -t CD -u $USER --noheader -j ${lsq6_First##* } | wc -l) -eq 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_First.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 1 " + str(Specimen_List_Length) + ")\n\n")
Job_Submission_First.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq6_Second_$NUM.sh\"\nLSQ6=\"sbatch $NAME\"\n$LSQ6\necho $LSQ6\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_First.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_First.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_First.write("# Submit 6-parameter average script.\nlsq6_Third=$(sbatch lsq6_Third.sh)\n\n")
Job_Submission_First.write("#----------------------------------------------------- Submit next job submission script after average finishes and remove current submission script from the queue.\n\n")
Job_Submission_First.write("sbatch --dependency=afterok:${lsq6_Third##* } Job_Submission_Second.sh\n\n")
Job_Submission_First.write("echo \"The job ended at $(date).\"\n")
Job_Submission_First.write("scancel -u $USER --jobname=Job_Submission_First.sh")
# Job_Submission_Second (i.e., 12-parameter blurs).
Job_Submission_Second = open("Job_Submission_Second.sh",'a')
Job_Submission_Second.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Second.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Second.write("cd " + Scripts_path + "\n\n")
Job_Submission_Second.write("sleep 10\n\n")
Job_Submission_Second.write("lsq12_First=$(sbatch lsq12_First.sh)\n\n")
Job_Submission_Second.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 1 " + str(Specimen_List_Length) + ")\n\n")
Job_Submission_Second.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq12_Second_$NUM.sh\"\nLSQ12=\"sbatch $NAME\"\n$LSQ12\necho $LSQ12\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Second.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Second.write("# Create while loop to idle submission script before the registrations.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Second.write("#----------------------------------------------------- Submit 12-parameter registration job submission script and remove current submission script from the queue.\n\n")
Job_Submission_Second.write("Job_Submission_Third=$(sbatch Job_Submission_Third.sh)\n\n")
Job_Submission_Second.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Second.write("scancel -u $USER --jobname=Job_Submission_Second.sh")
# Job_Submission_Third (i.e., 12-parameter pairwise registrations).
Job_Submission_Third = open("Job_Submission_Third.sh",'a')
Job_Submission_Third.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Third.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Third.write("cd " + Scripts_path + "\n\n")
Job_Submission_Third.write("sleep 10\n\n")
Job_Submission_Third.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Specimen_Upper) + ")\n\n")
Job_Submission_Third.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq12_Third_$NUM.sh\"\nLSQ12=\"sbatch $NAME\"\n$LSQ12\necho $LSQ12\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Third.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Third.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Third.write("#----------------------------------------------------- Submit xfm average, concatenating, and resampling job submission script and remove current submission script from the queue.\n\n")
Job_Submission_Third.write("Job_Submission_Fourth=$(sbatch Job_Submission_Fourth.sh)\n\n")
Job_Submission_Third.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Third.write("scancel -u $USER --jobname=Job_Submission_Third.sh")
# Job_Submission_Fourth (i.e., 12-parameter concatenations, resamplings, and the average).
Job_Submission_Fourth = open("Job_Submission_Fourth.sh",'a')
Job_Submission_Fourth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Fourth.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Fourth.write("cd " + Scripts_path + "\n\n")
Job_Submission_Fourth.write("sleep 10\n\n")
Job_Submission_Fourth.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Specimen_List_Length-1) + ")\n\n")
Job_Submission_Fourth.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq12_Fourth_$NUM.sh\"\nLSQ12=\"sbatch $NAME\"\n$LSQ12\necho $LSQ12\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Fourth.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Fourth.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Fourth.write("#----------------------------------------------------- Submit lsq12 average job submission script and the first non-linear (NL_1) dependency, then remove current submission script from the queue.\n\n")
Job_Submission_Fourth.write("lsq12_Fifth=$(sbatch lsq12_Fifth.sh)\n\n")
Job_Submission_Fourth.write("sbatch --dependency=afterok:${lsq12_Fifth##* } Job_Submission_Fifth.sh\n\n")
Job_Submission_Fourth.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Fourth.write("scancel -u $USER --jobname=Job_Submission_Fourth.sh")
# Job_Submission_Fifth (i.e., NL_1 and the first hierarchical non-linear registration).
Job_Submission_Fifth = open("Job_Submission_Fifth.sh",'a')
Job_Submission_Fifth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Fifth.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Fifth.write("cd " + Scripts_path + "\n\n")
Job_Submission_Fifth.write("sleep 10\n\n")
Job_Submission_Fifth.write("nl_First=$(sbatch nl_First.sh)\n\n")
Job_Submission_Fifth.write("until [[ $(squeue -t CD -u $USER --noheader -j ${nl_First##* } | wc -l) -eq 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Fifth.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Specimen_List_Length-1) + ")\n\n")
Job_Submission_Fifth.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"nl_Second_$NUM.sh\"\nNL1=\"sbatch $NAME\"\n$NL1\necho $NL1\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Fifth.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Fifth.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Fifth.write("#----------------------------------------------------- Submit NL_1 average job submission script and the second non-linear (NL_2) dependency, then remove current submission script from the queue.\n\n")
Job_Submission_Fifth.write("nl_Third=$(sbatch nl_Third.sh)\n\n")
Job_Submission_Fifth.write("sbatch --dependency=afterok:${nl_Third##* } Job_Submission_Sixth.sh\n\n")
Job_Submission_Fifth.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Fifth.write("scancel -u $USER --jobname=Job_Submission_Fifth.sh")
# Job_Submission_Sixth (i.e., NL_2 and the second hierarchical non-linear registration).
Job_Submission_Sixth = open("Job_Submission_Sixth.sh",'a')
Job_Submission_Sixth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Sixth.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Sixth.write("cd " + Scripts_path + "\n\n")
Job_Submission_Sixth.write("sleep 10\n\n")
Job_Submission_Sixth.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Specimen_List_Length-1) + ")\n\n")
Job_Submission_Sixth.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"nl_Fourth_$NUM.sh\"\nNL2=\"sbatch $NAME\"\n$NL2\necho $NL2\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Sixth.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Sixth.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Sixth.write("#----------------------------------------------------- Submit NL_2 average job submission script and the third non-linear (NL_3) dependency, then remove current submission script from the queue.\n\n")
Job_Submission_Sixth.write("nl_Fifth=$(sbatch nl_Fifth.sh)\n\n")
Job_Submission_Sixth.write("sbatch --dependency=afterok:${nl_Fifth##* } Job_Submission_Seventh.sh\n\n")
Job_Submission_Sixth.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Sixth.write("scancel -u $USER --jobname=Job_Submission_Sixth.sh")
# Job_Submission_Seventh (i.e., NL_3 and the third hierarchical non-linear registration).
Job_Submission_Seventh = open("Job_Submission_Seventh.sh",'a')
Job_Submission_Seventh.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Seventh.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Seventh.write("cd " + Scripts_path + "\n\n")
Job_Submission_Seventh.write("sleep 10\n\n")
Job_Submission_Seventh.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Specimen_List_Length-1) + ")\n\n")
Job_Submission_Seventh.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"nl_Sixth_$NUM.sh\"\nNL3=\"sbatch $NAME\"\n$NL3\necho $NL3\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Seventh.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Seventh.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Seventh.write("#----------------------------------------------------- Submit NL_3 average job submission script and the fourth non-linear (NL_4) dependency, then remove current submission script from the queue.\n\n")
Job_Submission_Seventh.write("nl_Seventh=$(sbatch nl_Seventh.sh)\n\n")
Job_Submission_Seventh.write("sbatch --dependency=afterok:${nl_Seventh##* } Job_Submission_Eighth.sh\n\n")
Job_Submission_Seventh.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Seventh.write("scancel -u $USER --jobname=Job_Submission_Seventh.sh")
# Job_Submission_Eighth (i.e., NL_4 and the third hierarchical non-linear registration).
Job_Submission_Eighth = open("Job_Submission_Eighth.sh",'a')
Job_Submission_Eighth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Eighth.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Eighth.write("cd " + Scripts_path + "\n\n")
Job_Submission_Eighth.write("sleep 10\n\n")
Job_Submission_Eighth.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Specimen_List_Length-1) + ")\n\n")
Job_Submission_Eighth.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"nl_Eighth_$NUM.sh\"\nNL4=\"sbatch $NAME\"\n$NL4\necho $NL4\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Eighth.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Eighth.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Eighth.write("#----------------------------------------------------- Submit final NL_4 average script.\n\n")
Job_Submission_Eighth.write("nl_Ninth=$(sbatch nl_Ninth.sh)\n\n")
Job_Submission_Eighth.write("echo \"The job ended at $(date).\"\n")
