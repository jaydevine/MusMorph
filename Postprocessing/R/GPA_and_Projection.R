#-----------------------------------------------------------------------------------------------------------------------
# GPA configurations onto manual training mean, then project into tangent space prior to training. 
#-----------------------------------------------------------------------------------------------------------------------
setwd("/path/to/wd/")
#-----------------------------------------------------------------------------------------------------------------------

# Load libraries.
library(Morpho)
library(geomorph)
library(morpho.tools.GM)

# Let's assume your landmark data are in /path/to/Landmarks. Say we have a manual landmark .csv and a set of automated .tag files. 
Manual <- read.csv("/path/to/Landmarks/<>.csv", header = T)
Auto <- morpho.tools.GM::tag2array(dir = "/path/to/Landmarks", propagated = TRUE)

# If you want to optimize the sparse adult landmarks described in MusMorph, make sure the proper landmarks are used. 
# These landmarks and their order are described in "Optimization_Landmarks.csv".

# Next, create training and testing sets from the manual and automated data. Make sure the specimen IDs match. 
# Let Man_Train, Man_Test, Auto_Train, and Auto_Test be our 3-D arrays with P landmarks in K dimensions.
Man_Train <- arrayspecs(Man_Train, P, K)
Man_Test <- arrayspecs(Man_Test, P, K)
Auto_Train <- arrayspecs(Auto_Train, P, K)
Auto_Test <- arrayspecs(Auto_Test, P, K)

# GPA manual training data.
Man_procSym <- procSym(MAN_Train_3D_Arr, reflect = TRUE, CSinit = TRUE, orp = TRUE,
                       tol = 1e-05, pairedLM = NULL, sizeshape = FALSE,
                       use.lm = NULL, center.part = FALSE, weights = NULL,
                       centerweight = FALSE, pcAlign = TRUE, distfun = c("angle", "riemann"),
                       SMvector = NULL, outlines = NULL, deselect = FALSE, recursive = TRUE,
                       iterations = 0, initproc = FALSE, bending = FALSE)

# GPA data to manual training data, including orthogonal projection.
Man_Train_Align <- align2procSym(Man_procSym, Man_Train, orp = TRUE)
Auto_Train_Align <- align2procSym(Man_procSym, Auto_Train, orp = TRUE)
Man_Test_Align <- align2procSym(Man_procSym ,Man_Test, orp = TRUE)
Auto_Test_Align <- align2procSym(Man_procSym, Auto_Test, orp = TRUE)

# Create 2D arrays.
Man_Train_Align <- two.d.array(Man_Train_Align)
Auto_Train_Align <- two.d.array(Auto_Train_Align)
Man_Test_Align <- two.d.array(Man_Test_Align)
Auto_Test_Align <- two.d.array(Auto_Test_Align)

# Write .csv files for import into Julia. 
write.csv(Man_Train_Align, "/path/to/Landmark/<>.csv")
write.csv(Auto_Train_Align, "/path/to/Landmark/<>.csv")
write.csv(Man_Test_Align, "/path/to/Landmark/<>.csv")
write.csv(Auto_Test_Align, "/path/to/Landmark/<>.csv")

#---