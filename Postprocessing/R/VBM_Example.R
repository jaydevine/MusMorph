#-----------------------------------------------------------------------------------------------------------------------
# An example VBM script. This script takes in a set of .mnc Jacobian determinant volumes (see Postprocessing/Bash/Jacobians.sh for more detail on how to generate them) and performs a simple voxel-based morphometry test. Statistical parametric maps can be derived with the shinyRMINC application or with one of their plotting functions, such as "mincPlotSliceSeries". These maps can localize the magnitude, variance, etc. of morphological change among experimental groups at each voxel. They are a useful way to show morphological change across a volume, rather than just on the surface, as is common with geometric morphometrics.

# Supporting information: https://github.com/Mouse-Imaging-Centre/RMINC. 

#-----------------------------------------------------------------------------------------------------------------------

# Load libraries. 
library(devtools)
library(RMINC) # See installation of RMINC here: https://github.com/Mouse-Imaging-Centre/RMINC.
library(plotrix)
library(rgl)

# Path to determinants. If you have not made these files, see Postprocessing/Bash/Jacobians.sh.
MNC.Dir=c("/path/to/determinants")

# List of form determinants. Say they have the following suffix: "_form_inverted_determinant_p1_blur.mnc".
Form_List=list.files(path=MNC.Dir,pattern="*_form_inverted_determinant_p1_blur.mnc",full.names=TRUE)
# List of shape determinants. Say they have the following suffix: "_shape_inverted_determinant_p1_blur.mnc".
Shape_List=list.files(path=MNC.Dir,pattern="*_shape_inverted_determinant_p1_blur.mnc",full.names=TRUE)

# Read in metadata CSV. 
DF=read.csv("/path/to/DF/<>.csv", header=TRUE)

# Order the factors as needed. For example, you may want to define your baseline factor,
# like wildtype, at the beginning of the variable.

# Load in your atlas .mnc file. Only load in if needed, because it requires a lot of memory. 
Atlas=mincGetVolume("/path/to/Atlas/<>.mnc")

# Run a linear model at each voxel to test for differences among experimental groups. 
# The dependent variable is your list of form or shape determinants. The independent
# variable is a factor and/or covariate(s) from your DF. Call it DF$Factor. In addition,
# it is wise to restrict the model computation with a mask (i.e., the atlas mask) 
# to limit the amount of memory. 
Model=mincLm(Form_List~DF$Factor,
             mask="/path/to/Atlas_Mask/<>.mnc")

# Run a false discovery rate test on this model to correct for multiple testing error. 
# Again, it is advisable to use a mask to restrict the number of voxels being tested.
# This mask can be of the whole image, or it can be a segmentation of the image. 

FDR=mincFDR(NOSIP_LM_Nlin,
            mask="/path/to/Atlas_Mask/<>.mnc")

# Check the FDR thresholds. Select your significance value, which is often p < 0.05. 
print(FDR)

# You can plot these results with RMINC's interactive Shiny application.
# Plotcolumns will show you the determinant value at a single voxel for each
# treatment group, and "anatLow = x" / "anatHigh = y" define the lower and
# upper intensity bounds you want to display. 
launch_shinyRMINC(Model, anatVol = mincArray(Atlas),
                  plotcolumns = DF$Factor, anatLow = x, anatHigh = y)

# Alternatively, you can plot the statistics statically with mincPlotSliceSeries:
# - "anatomy" is the image you want to display, i.e., the atlas;
# - "statistics are the type of voxel-wise stats you want to display and "tvalue-Factor" is the name of the factor in the FDR test;
# - "anatLow" and "anatHigh" define the lower and upper intensity bounds of the displayed image;
# - "low" and "high" are the lower (p < 0.05) and upper (p < 0.01) bounds of the statistics you want to show;
# - "begin" and "end" are the slices to begin and end at.
# ' "dimension" is the view of the anatomy, e.g., coronal, sagittal, or transverse. 
plot.new()
svg(filename="/path/to/Plot/<>.svg",
    width = x, height = y)
mincPlotSliceSeries(anatomy = mincArray(Atlas), 
                    statistics = mincArray(Atlas, "tvalue-Factor"),
                    anatLow = x, anatHigh=y,
                    symmetric=TRUE,
                    low = x, high = y,
                    begin = x, end = y,
                    dimension = x,
                    legend="t value")
dev.off()

# There are also RMINC functions to generate, e.g., the atlas volume with different statistics overlaid on it. For example, if we
# wanted to display the variance at each voxel:
Variance <- mincVar(Form_List, grouping = DF$Factor, 
                    mask="/path/to/Atlas_Mask/<>.mnc")

# Write the volume via mincWriteVolume, where the level of the factor would be in "" the the like.filename variable is the atlas.
# Defining all of the paths explicitly seems to work better than using pre-existing variables. 
setwd("/path/for/newfile")
mincWriteVolume(Variance, "/path/for/newfile/<>.mnc", "", like.filename = "/path/to/Atlas/<>.mnc")

# To read the file in later, use mincGetVolume, like we did with the atlas:
Variance <- mincGetVolume("/path/for/newfile/<>.mnc")

# There are numerous other handy functions, thanks to the RMINC developers.
