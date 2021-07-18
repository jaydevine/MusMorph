#### 0. Load R packages ####
library(rgl)
library(geomorph)
library(devtools)
install_github("marta-vidalgarcia/morpho.tools.GM")
library(morpho.tools.GM)
library(Rvcg)

#### 1. Load data ####
# endo_mesh <- geomorph::read.ply("./Postprocessing/data/atlas/Calgary_Adult_Endocast_Atlas.ply")
# endo_lowres <- vcgQEdecim(endo_mesh, percent = 0.125)
# rgl::open3d(windowRect = c(20, 30, 800, 800))
# rgl::shade3d(endo_lowres, color="gray", alpha=1)
# writePLY("./Postprocessing/data/atlas/Calgary_Adult_Endocast_Atlas_lowres.ply")

endo_mesh <- geomorph::read.ply("./Postprocessing/data/atlas/Calgary_Adult_Endocast_Atlas_lowres.ply")

atlas_endo_lm <- morpho.tools.GM::tag2lm("./Postprocessing/data/atlas/Calgary_Adult_Endocast_Atlas_Landmarks.tag")

# Divide the data into type of landmark
LM_type_endo <- suppressWarnings(read.table(file = "./Postprocessing/data/atlas/Calgary_Adult_Endocast_Atlas_Landmarks.tag", skip = 4, sep = " ", header=F))[, 8]
levels(as.factor(LM_type_endo))
vec_LM_endo <- which(LM_type_endo == "LANDMARK")
vec_curve_endo <- which(LM_type_endo == "curve_semilandmark")
vec_surf_endo <- c(which(LM_type_endo == "surface_semilandmarks"), which(LM_type_endo == "surface_semilandmarks;"))

ENDO_fixed.lm <- vec_LM_endo
ENDO_curves.lm <- vec_curve_endo
ENDO_surface.lm <- vec_surf_endo


#### 2. Plotting ####
# Plot the mesh with the landmarks, curve semi-landmarks, and surface semi-landmarks
rgl::open3d(windowRect = c(20, 30, 800, 800))
rgl::shade3d(endo_mesh, color="gray", alpha=1)
rgl::plot3d(atlas_endo_lm[ENDO_fixed.lm,], aspect="iso", type="s", size=1, col="red", add=T)
rgl::plot3d(atlas_endo_lm[ENDO_curves.lm,], aspect="iso", type="s", size=0.9, col="green", add=T)
rgl::plot3d(atlas_endo_lm[87:108,], aspect="iso", type="s", size=0.8, col="black", add=T)
rgl::plot3d(atlas_endo_lm[ENDO_surface.lm,], aspect="iso", type="s", size=0.6, col="blue", add=T)
rgl::rgl.snapshot("./Postprocessing/output/Endocast_LM_lateral.png", top = TRUE)
rgl::rgl.snapshot("./Postprocessing/output/Endocast_LM_dorsal.png", top = TRUE)
rgl::rgl.snapshot("./Postprocessing/output/Endocast_LM_ventral.png", top = TRUE)
rgl::rgl.close()

# Lateral view
open3d(zoom = 0.75, userMatrix = lateral, windowRect = c(0, 0, 1000, 700)) 
shade3d(skull_mesh, color = "gray", alpha = 0.8)
plot3d(atlas_lm, aspect = 'iso', type = 's', size = 1.1, col = 'darkblue', add = TRUE)

rgl.close()


#### 3. Sliding the curve semi-landmarks ####

ENDO_curve1 <- c(13:23) # between LM 12 and 7. semi 13 slides between lm 12 and semi 14. Semi 23 slides between semi 22 and LM 7
ENDO_curve2 <- c(24:34) # between LM 12 and 6. semi 24 slides between lm 12 and semi 25. Semi 34 slides between semi 33 and LM 6
ENDO_curve3 <- c(35:39)  # between LM 3 and 5. Semi 35 slides between lm 3 and semi 36. Semi 39 slides between semi 38 and lm 5
ENDO_curve4 <- c(40:44)  # between LM 3 and 4. Semi 40 slides between lm 3 and semi 41. Semi 44 slides between semi 43 and lm 4
ENDO_curve5 <- c(45,46)  # between LM 7 and 9. Semi 45 slides between lm 7 and semi 46. Semi 46 slides between semi 45 and lm 9
ENDO_curve6 <- c(47,48)  # between LM 6 and 8. Semi 47 slides between lm 6 and semi 48. Semi 48 slides between semi 47 and lm 8
ENDO_curve7 <- c(49:53)  # between LM 5 and 9. Semi 49 slides between lm 5 and semi 50. Semi 53 slides between semi 52 and lm 9
ENDO_curve8 <- c(54:58)  # between LM 4 and 8. Semi 54 slides between lm 4 and semi 55. Semi 58 slides between semi 57 and lm 8
ENDO_curve9 <- c(59:65)  # between LM 5 and 9. Semi 59 slides between lm 5 and semi 60. Semi 65 slides between semi 64 and lm 9
ENDO_curve10 <- c(66:72)  # between LM 4 and 8. Semi 66 slides between lm 4 and semi 67. Semi 72 slides between semi 71 and lm 8
ENDO_curve11 <- c(73:75) # between LM 1 and 2. semi 73 slides between lm 2 and semi 74. semi 75 slides between 74 and 1
ENDO_curve12 <- c(76:78) # between LM 1 and 11
ENDO_curve13 <- c(79:86) # between LM 11 and 10


# We need to create a curveslide matrix to know where from to where to the semis slide
curve1_left <- c(12, (ENDO_curve1-1)[2:length(ENDO_curve1)])
curve1_right <- c((ENDO_curve1+1)[1:length(ENDO_curve1)-1], 7)
curveslide_1 <- cbind(curve1_left, ENDO_curve1, curve1_right)

curve2_left <- c(12, (ENDO_curve2-1)[2:length(ENDO_curve2)])
curve2_right <- c((ENDO_curve2+1)[1:length(ENDO_curve2)-1], 6)
curveslide_2 <- cbind(curve2_left, ENDO_curve2, curve2_right)

curve3_left <- c(3, (ENDO_curve3-1)[2:length(ENDO_curve3)])
curve3_right <- c((ENDO_curve3+1)[1:length(ENDO_curve3)-1], 5)
curveslide_3 <- cbind(curve3_left, ENDO_curve3, curve3_right)

curve4_left <- c(3, (ENDO_curve4-1)[2:length(ENDO_curve4)])
curve4_right <- c((ENDO_curve4+1)[1:length(ENDO_curve4)-1], 4)
curveslide_4 <- cbind(curve4_left, ENDO_curve4, curve4_right)

curve5_left <- c(7, (ENDO_curve5-1)[2:length(ENDO_curve5)])
curve5_right <- c((ENDO_curve5+1)[1:length(ENDO_curve5)-1], 9)
curveslide_5 <- cbind(curve5_left, ENDO_curve5, curve5_right)

curve6_left <- c(6, (ENDO_curve6-1)[2:length(ENDO_curve6)])
curve6_right <- c((ENDO_curve6+1)[1:length(ENDO_curve6)-1], 8)
curveslide_6 <- cbind(curve6_left, ENDO_curve6, curve6_right)

curve7_left <- c(5, (ENDO_curve7-1)[2:length(ENDO_curve7)])
curve7_right <- c((ENDO_curve7+1)[1:length(ENDO_curve7)-1], 9)
curveslide_7 <- cbind(curve7_left, ENDO_curve7, curve7_right)

curve8_left <- c(4, (ENDO_curve8-1)[2:length(ENDO_curve8)])
curve8_right <- c((ENDO_curve8+1)[1:length(ENDO_curve8)-1], 8)
curveslide_8 <- cbind(curve8_left, ENDO_curve8, curve8_right)

curve9_left <- c(5, (ENDO_curve9-1)[2:length(ENDO_curve9)])
curve9_right <- c((ENDO_curve9+1)[1:length(ENDO_curve9)-1], 9)
curveslide_9 <- cbind(curve9_left, ENDO_curve9, curve9_right)

curve10_left <- c(4, (ENDO_curve10-1)[2:length(ENDO_curve10)])
curve10_right <- c((ENDO_curve10+1)[1:length(ENDO_curve10)-1], 8)
curveslide_10 <- cbind(curve10_left, ENDO_curve10, curve10_right)

curve11_left <- c(1, (ENDO_curve11-1)[2:length(ENDO_curve11)])
curve11_right <- c((ENDO_curve11+1)[1:length(ENDO_curve11)-1], 2)
curveslide_11 <- cbind(curve11_left, ENDO_curve11, curve11_right)

curve12_left <- c(1, (ENDO_curve12-1)[2:length(ENDO_curve12)])
curve12_right <- c((ENDO_curve12+1)[1:length(ENDO_curve12)-1], 11)
curveslide_12 <- cbind(curve12_left, ENDO_curve12, curve12_right)

curve13_left <- c(11, (ENDO_curve13-1)[2:length(ENDO_curve13)])
curve13_right <- c((ENDO_curve13+1)[1:length(ENDO_curve13)-1], 10)
curveslide_13 <- cbind(curve13_left, ENDO_curve13, curve13_right)

# all our curveslide matrices
ls(pattern="curveslide*")
curveslide_list <- lapply(list(ls(pattern="curveslide*")), get)
curveslide_all <- do.call(rbind, curveslide_list)

write.csv(curveslide_all, "./Postprocessing/output/curveslide_endocast.csv")

#### 4. Analysing the 3D landmark data with GMM ####
# For example:
endo_array <- morpho.tools.GM::tag2array(string_del = "_endo_landmarks.tag", propagated = TRUE)

GPA_endocast <- geomorph::gpagen(A = endo_array, curves = as.matrix(curveslide_all), surfaces = ENDO_surface.lm)

