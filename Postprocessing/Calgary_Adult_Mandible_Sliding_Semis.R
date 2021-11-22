#### 0. Load R packages ####
library(rgl)
library(geomorph)
library(devtools)
install_github("marta-vidalgarcia/morpho.tools.GM")
library(morpho.tools.GM)
library(Rvcg)

#### 1. Load data ####
mand_mesh <- geomorph::read.ply("./Postprocessing/Data/Atlases/Calgary_Adult_Mandible_Atlas_DS_ascii.ply")
atlas_mand_lm <- morpho.tools.GM::tag2lm("./Postprocessing/Data/Atlases/Calgary_Adult_Mandible_Atlas_Landmarks.tag")
atlas_mand_lm <- suppressWarnings(read.table(file = "./Postprocessing/Data/Atlases/Calgary_Adult_Mandible_Atlas_Landmarks.tag", skip = 5, sep = " ", header=F))[, 2:4]

# Divide the data into type of landmark
LM_type_mand <- suppressWarnings(read.table(file = "./Postprocessing/Data/Atlases/Calgary_Adult_Mandible_Atlas_Landmarks.tag", skip = 5, sep = " ", header=F))[, 8]
levels(as.factor(LM_type_mand))
vec_LM_mand <- which(LM_type_mand == "LANDMARK")
vec_curve_mand <- which(LM_type_mand == "curve_semilandmark")
vec_surf_mand <- c(which(LM_type_mand == "surface_semilandmarks"), which(LM_type_mand == "surface_semilandmarks;"))
       
mand_fixed.lm <- vec_LM_mand
mand_curves.lm <- vec_curve_mand
mand_surface.lm <- vec_surf_mand


#### 2. Plotting ####
# Plot the mesh with the landmarks, curve semi-landmarks, and surface semi-landmarks
rgl::open3d(windowRect = c(20, 30, 800, 800))
# rgl.pop("lights")
# light3d(specular="black")
rgl::shade3d(mand_mesh, color="gray")
rgl::plot3d(atlas_mand_lm[mand_fixed.lm,], aspect="iso", type="s", size=1, col="red", add=T)
# rgl::text3d(x = atlas_mand_lm[mand_fixed.lm, 1], 
#              y = atlas_mand_lm[mand_fixed.lm, 2], 
#              z=  atlas_mand_lm[mand_fixed.lm, 3], 
#              texts = row.names(atlas_mand_lm[mand_fixed.lm, ]), 
#              cex = 1.5, offset = 0.5, pos = 3)
rgl::plot3d(atlas_mand_lm[mand_curves.lm,], aspect="iso", type="s", size=0.9, col="green", add=T)
rgl::plot3d(atlas_mand_lm[mand_surface.lm,], aspect="iso", type="s", size=0.6, col="blue", add=T)
rgl::rgl.snapshot("./Postprocessing/Output/Mandible_LM_lateral.png", top = TRUE)
rgl::rgl.snapshot("./Postprocessing/Output/Mandible_LM_dorsal.png", top = TRUE)
rgl::rgl.snapshot("./Postprocessing/Output/Mandible_LM_posterior.png", top = TRUE)
rgl::rgl.close()


#### 3. Sliding the curve semi-landmarks ####

MAND_curve1 <- c(20:25) # sliding between LM1 & LM2
MAND_curve2 <- c(26:31) # sliding between LM6 & LM7
MAND_curve3 <- c(32:43) # sliding between LM1 & LM5
MAND_curve4 <- c(44:55) # sliding between LM6 & LM10
MAND_curve5 <- c(56:64) # sliding betwen LM3 & LM5
MAND_curve6 <- c(65:74) # sliding between LM8 & LM10 
MAND_curve7 <- c(75:87) # sliding between LM6 & LM14
MAND_curve8 <- c(88:100) # sliding semis between LM1 & LM13
MAND_curve9 <- c(101:104) # sliding semis between LM14 & LM16
MAND_curve10 <- c(105:108) # sliding semis between LM9 & LM17
MAND_curve11 <- c(109:113) # sliding semis between LM2 & LM3
MAND_curve12 <- c(114:118) # sliding semis between LM7 & LM8
MAND_curve13 <- c(119:123) # sliding semis between LM16 & LM4
MAND_curve14 <- c(124:128) # sliding semis between LM17 & LM9
MAND_curve15 <- c(129:133) # sliding semis between LM16 & LM4
MAND_curve16 <- c(134:138) # sliding semis between LM17 & LM9
MAND_curve17 <- c(139:144) # sliding semis between LM18 & LM9 # MAND_curve17 <- c(239:244) # sliding semis between LM18 & LM9
MAND_curve18 <- c(145:150) # sliding semis between LM15 & LM4 # MAND_curve18 <- c(245:250) # sliding semis between LM15 & LM4

# We need to create a curveslide matrix to know where from to where to the semis slide
curve1_left <- c(1, (MAND_curve1-1)[2:length(MAND_curve1)])
curve1_right <- c((MAND_curve1+1)[1:length(MAND_curve1)-1], 2)
curveslide_1 <- cbind(curve1_left, MAND_curve1, curve1_right)

curve2_left <- c(6, (MAND_curve2-1)[2:length(MAND_curve2)])
curve2_right <- c((MAND_curve2+1)[1:length(MAND_curve2)-1], 7)
curveslide_2 <- cbind(curve2_left, MAND_curve2, curve2_right)

curve3_left <- c(1, (MAND_curve3-1)[2:length(MAND_curve3)])
curve3_right <- c((MAND_curve3+1)[1:length(MAND_curve3)-1], 5)
curveslide_3 <- cbind(curve3_left, MAND_curve3, curve3_right)

curve4_left <- c(6, (MAND_curve4-1)[2:length(MAND_curve4)])
curve4_right <- c((MAND_curve4+1)[1:length(MAND_curve4)-1], 10)
curveslide_4 <- cbind(curve4_left, MAND_curve4, curve4_right)

curve5_left <- c(3, (MAND_curve5-1)[2:length(MAND_curve5)])
curve5_right <- c((MAND_curve5+1)[1:length(MAND_curve5)-1], 5)
curveslide_5 <- cbind(curve5_left, MAND_curve5, curve5_right)

curve6_left <- c(8, (MAND_curve6-1)[2:length(MAND_curve6)])
curve6_right <- c((MAND_curve6+1)[1:length(MAND_curve6)-1], 10)
curveslide_6 <- cbind(curve6_left, MAND_curve6, curve6_right)

curve7_left <- c(6, (MAND_curve7-1)[2:length(MAND_curve7)])
curve7_right <- c((MAND_curve7+1)[1:length(MAND_curve7)-1], 14)
curveslide_7 <- cbind(curve7_left, MAND_curve7, curve7_right)

curve8_left <- c(1, (MAND_curve8-1)[2:length(MAND_curve8)])
curve8_right <- c((MAND_curve8+1)[1:length(MAND_curve8)-1], 13)
curveslide_8 <- cbind(curve8_left, MAND_curve8, curve8_right)

curve9_left <- c(14, (MAND_curve9-1)[2:length(MAND_curve9)])
curve9_right <- c((MAND_curve9+1)[1:length(MAND_curve9)-1], 16)
curveslide_9 <- cbind(curve9_left, MAND_curve9, curve9_right)

curve10_left <- c(9, (MAND_curve10-1)[2:length(MAND_curve10)])
curve10_right <- c((MAND_curve10+1)[1:length(MAND_curve10)-1], 17)
curveslide_10 <- cbind(curve10_left, MAND_curve10, curve10_right)

curve11_left <- c(2, (MAND_curve11-1)[2:length(MAND_curve11)])
curve11_right <- c((MAND_curve11+1)[1:length(MAND_curve11)-1], 3)
curveslide_11 <- cbind(curve11_left, MAND_curve11, curve11_right)

curve12_left <- c(7, (MAND_curve12-1)[2:length(MAND_curve12)])
curve12_right <- c((MAND_curve12+1)[1:length(MAND_curve12)-1], 8)
curveslide_12 <- cbind(curve12_left, MAND_curve12, curve12_right)

curve13_left <- c(16, (MAND_curve13-1)[2:length(MAND_curve13)])
curve13_right <- c((MAND_curve13+1)[1:length(MAND_curve13)-1], 4)
curveslide_13 <- cbind(curve13_left, MAND_curve13, curve13_right)

curve14_left <- c(17, (MAND_curve14-1)[2:length(MAND_curve14)])
curve14_right <- c((MAND_curve14+1)[1:length(MAND_curve14)-1], 9)
curveslide_14 <- cbind(curve14_left, MAND_curve14, curve14_right)

curve15_left <- c(16, (MAND_curve15-1)[2:length(MAND_curve15)])
curve15_right <- c((MAND_curve15+1)[1:length(MAND_curve15)-1], 4)
curveslide_15 <- cbind(curve15_left, MAND_curve15, curve15_right)

curve16_left <- c(17, (MAND_curve16-1)[2:length(MAND_curve16)])
curve16_right <- c((MAND_curve16+1)[1:length(MAND_curve16)-1], 9)
curveslide_16 <- cbind(curve16_left, MAND_curve16, curve16_right)

curve17_left <- c(18, (MAND_curve17-1)[2:length(MAND_curve17)])
curve17_right <- c((MAND_curve17+1)[1:length(MAND_curve17)-1], 9)
curveslide_17 <- cbind(curve17_left, MAND_curve17, curve17_right)

curve18_left <- c(15, (MAND_curve18-1)[2:length(MAND_curve18)])
curve18_right <- c((MAND_curve18+1)[1:length(MAND_curve18)-1], 4)
curveslide_18 <- cbind(curve18_left, MAND_curve18, curve18_right)


# all our curveslide matrices
ls(pattern="curveslide*")
curveslide_list <- lapply(ls(pattern="curveslide_*"), get)
curveslide_all <- do.call(rbind, curveslide_list)

write.csv(curveslide_all, "./Postprocessing/Calgary_Adult_Mandible_Atlas_Curveslide.csv")

#### 4. Analysing the 3D landmark data with GMM ####
# For example:
mand_array <- morpho.tools.GM::tag2array(string_del = "_Mandible_Landmarks.tag", propagated = TRUE)

GPA_mandible <- geomorph::gpagen(A = mand_array, curves = as.matrix(curveslide_all), surfaces = mand_surface.lm)
