#### 0. Load R packages ####
library(rgl)
library(geomorph)
library(devtools)
install_github("marta-vidalgarcia/morpho.tools.GM")
library(morpho.tools.GM)
library(Rvcg)

#### 1. Load data ####
skull_mesh <- geomorph::read.ply("./Postprocessing/Data/Atlases/Calgary_Adult_Cranium_Atlas_DS_ascii.ply")

atlas_skull_lm <- morpho.tools.GM::tag2lm("./Postprocessing/Data/Atlases/Calgary_Adult_Cranium_Atlas_Landmarks.tag")
atlas_skull_lm <- read.table(file = "./Postprocessing/Data/Atlases/Calgary_Adult_Cranium_Atlas_Landmarks.tag", skip = 5, sep = " ", header=F)[, 2:4]

# Divide the data into type of landmark
LM_type_skull <- suppressWarnings(read.table(file = "./Postprocessing/Data/Atlases/Calgary_Adult_Cranium_Atlas_Landmarks.tag", skip = 5, sep = " ", header=F))[, 8]
levels(as.factor(LM_type_skull))
vec_LM_skull <- which(LM_type_skull == "LANDMARK")
vec_curve_skull <- which(LM_type_skull == "curve_semilandmark")
vec_surf_skull <- c(which(LM_type_skull == "surface_semilandmarks"), which(LM_type_skull == "surface_semilandmarks;"))

skull_fixed.lm <- vec_LM_skull
skull_curves.lm <- vec_curve_skull
skull_surface.lm <- vec_surf_skull


#### 2. Plotting ####
# Plot the mesh with the landmarks, curve semi-landmarks, and surface semi-landmarks
rgl::open3d(windowRect = c(20, 30, 800, 800))
# rgl.pop("lights")
# light3d(specular = "black")
rgl::shade3d(skull_mesh, color = "gray", alpha =0.9)
rgl::plot3d(atlas_skull_lm[skull_fixed.lm,], aspect = "iso", type = "s", size=1, col = "red", add = T)
rgl::text3d(x = atlas_skull_lm[skull_fixed.lm, 1], 
             y = atlas_skull_lm[skull_fixed.lm, 2], 
             z=  atlas_skull_lm[skull_fixed.lm, 3], 
             texts = row.names(atlas_skull_lm[skull_fixed.lm, ]), 
             cex = 1.5, offset = 0.5, pos = 3)
rgl::plot3d(atlas_skull_lm[skull_curves.lm,], aspect = "iso", type = "s", size=0.9, col = "green", add = T)
rgl::plot3d(atlas_skull_lm[87:108,], aspect = "iso", type = "s", size=0.8, col = "black", add = T)
rgl::plot3d(atlas_skull_lm[skull_surface.lm,], aspect = "iso", type = "s", size=0.6, col = "blue", add = T)
rgl::rgl.snapshot("./Postprocessing/Output/skullcast_LM_lateral.png", top = TRUE)
rgl::rgl.snapshot("./Postprocessing/Output/skullcast_LM_dorsal.png", top = TRUE)
rgl::rgl.snapshot("./Postprocessing/Output/skullcast_LM_ventral.png", top = TRUE)
rgl::rgl.close()


#### 3. Sliding the curve semi-landmarks ####  NEED TO CHECK NUMBERS AGAIN BC I REORDERED THE LANDMARKS
rgl::open3d(zoom = 0.7, windowRect = c(20, 30, 800, 1100))
rgl::shade3d(skull_mesh, color = "gray", alpha =0.55)
rgl::plot3d(atlas_skull_lm[skull_fixed.lm,], aspect = "iso", type = "s", size=0.35, col = "red", add = T)
rgl::text3d(x = atlas_skull_lm[skull_fixed.lm, 1], 
            y = atlas_skull_lm[skull_fixed.lm, 2], 
            z=  atlas_skull_lm[skull_fixed.lm, 3], 
            texts = row.names(atlas_skull_lm[skull_fixed.lm, ]), 
            cex = 1.25, offset = 0.5, pos = 3)


SKULL_curve1 <- c(95:99) # sliding between LM10 & LM11
SKULL_curve2 <- c(100:107) # sliding between LM11 & LM12
SKULL_curve3 <- c(108:111) # sliding between LM21 & LM11
SKULL_curve4 <- c(112:115) # sliding between LM22 & LM11
SKULL_curve5 <- c(116:125) # sliding between LM22 & LM78
SKULL_curve6 <- c(126:134) # sliding between LM13 & LM60
SKULL_curve7 <- c(135:143) # sliding between LM14 & LM59
SKULL_curve8 <- c(144:149) # sliding between LM1 & LM10
SKULL_curve9 <- c(150:155) # sliding between LM10 & LM10
SKULL_curve10 <- c(156:160) # sliding between LM7 & LM5
SKULL_curve11a <- c(161:165) # sliding between LM7 & LM6
SKULL_curve11b <- c(161:170) # sliding between LM41 & LM64
SKULL_curve12 <- c(171:180) # sliding between LM42 & LM71
SKULL_curve13 <- c(181:183) # sliding between LM54 & LM53
SKULL_curve14 <- c(184:187) # sliding between LM56 & LM54
SKULL_curve15 <- c(188:191) # sliding between LM55 & LM53
SKULL_curve16 <- c(192:200) # sliding between LM28 & LM70
SKULL_curve17 <- c(201:207) # sliding between LM70 & LM1
SKULL_curve18 <- c(208:215) # sliding between LM68 & LM19
SKULL_curve19 <- c(216:221) # sliding between LM19 & LM69
SKULL_curve20 <- c(222:230) # sliding between LM27 & LM63
SKULL_curve21 <- c(231:237) # sliding between LM63 & LM2
SKULL_curve22 <- c(238:245) # sliding between LM18 & LM20
SKULL_curve23 <- c(246:251) # sliding between LM20 & LM62
SKULL_curve24 <- c(252:264) # sliding between LM68 & LM72
SKULL_curve25 <- c(265:275) # sliding between LM61 & LM65
SKULL_curve26 <- c(276:284) # sliding between LM7 & LM23
SKULL_curve27 <- c(285:289) # sliding between LM7 & LM6
SKULL_curve28 <- c(290:292) # sliding between LM80 & LM27
SKULL_curve29 <- c(293:295) # sliding between LM81 & LM28
SKULL_curve30 <- c(296:302) # sliding between LM72 & LM90
SKULL_curve31 <- c(303:309) # sliding between LM65 & LM89
SKULL_curve32 <- c(310:313) # sliding between LM9 & LM8
SKULL_curve33 <- c(314:325) # sliding between LM91 & LM91
SKULL_curve34 <- c(326:336) # sliding between LM79 & LM79

rgl::plot3d(atlas_skull_lm[SKULL_curve1,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve2,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve3,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve4,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve5,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve6,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve7,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve8,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve9,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve10,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve11,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve12,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve13,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve14,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve15,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve16,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve17,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve18,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve19,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve20,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve21,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve22,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve23,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve24,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve25,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve26,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve27,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve28,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve29,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve30,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve31,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve32,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve33,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)
rgl::plot3d(atlas_skull_lm[SKULL_curve34,], aspect = "iso", type = "s", size = 0.8, col = "blue", add = T)



# We need to create a curveslide matrix to know where from to where to the semis slide
curve1_left <- c(10, (SKULL_curve1-1)[2:length(SKULL_curve1)])
curve1_right <- c((SKULL_curve1+1)[1:length(SKULL_curve1)-1], 11)
curveslide_01 <- cbind(curve1_left, SKULL_curve1, curve1_right)

curve2_left <- c(11, (SKULL_curve2-1)[2:length(SKULL_curve2)])
curve2_right <- c((SKULL_curve2+1)[1:length(SKULL_curve2)-1], 12)
curveslide_02 <- cbind(curve2_left, SKULL_curve2, curve2_right)

curve3_left <- c(21, (SKULL_curve3-1)[2:length(SKULL_curve3)])
curve3_right <- c((SKULL_curve3+1)[1:length(SKULL_curve3)-1], 11)
curveslide_03 <- cbind(curve3_left, SKULL_curve3, curve3_right)

curve4_left <- c(22, (SKULL_curve4-1)[2:length(SKULL_curve4)])
curve4_right <- c((SKULL_curve4+1)[1:length(SKULL_curve4)-1], 11)
curveslide_04 <- cbind(curve4_left, SKULL_curve4, curve4_right)

curve5_left <- c(22, (SKULL_curve5-1)[2:length(SKULL_curve5)])
curve5_right <- c((SKULL_curve5+1)[1:length(SKULL_curve5)-1], 78)
curveslide_05 <- cbind(curve5_left, SKULL_curve5, curve5_right)

curve6_left <- c(13, (SKULL_curve6-1)[2:length(SKULL_curve6)])
curve6_right <- c((SKULL_curve6+1)[1:length(SKULL_curve6)-1], 60)
curveslide_06 <- cbind(curve6_left, SKULL_curve6, curve6_right)

curve7_left <- c(14, (SKULL_curve7-1)[2:length(SKULL_curve7)])
curve7_right <- c((SKULL_curve7+1)[1:length(SKULL_curve7)-1], 59)
curveslide_07 <- cbind(curve7_left, SKULL_curve7, curve7_right)

curve8_left <- c(1, (SKULL_curve8-1)[2:length(SKULL_curve8)])
curve8_right <- c((SKULL_curve8+1)[1:length(SKULL_curve8)-1], 10)
curveslide_08 <- cbind(curve8_left, SKULL_curve8, curve8_right)

curve9_left <- c(10, (SKULL_curve9-1)[2:length(SKULL_curve9)])
curve9_right <- c((SKULL_curve9+1)[1:length(SKULL_curve9)-1], 10)
curveslide_09 <- cbind(curve9_left, SKULL_curve9, curve9_right)

curve10_left <- c(7, (SKULL_curve10-1)[2:length(SKULL_curve10)])
curve10_right <- c((SKULL_curve10+1)[1:length(SKULL_curve10)-1], 5)
curveslide_10 <- cbind(curve10_left, SKULL_curve10, curve10_right)

curve11a_left <- c(7, (SKULL_curve11a-1)[2:length(SKULL_curve11a)])
curve11a_right <- c((SKULL_curve11a+1)[1:length(SKULL_curve11a)-1], 6)
curveslide_11a <- cbind(curve11a_left, SKULL_curve11a, curve11a_right)

curve11b_left <- c(41, (SKULL_curve11b-1)[2:length(SKULL_curve11b)])
curve11b_right <- c((SKULL_curve11b+1)[1:length(SKULL_curve11b)-1], 64)
curveslide_11b <- cbind(curve11b_left, SKULL_curve11b, curve11b_right)

curve12_left <- c(42, (SKULL_curve12-1)[2:length(SKULL_curve12)])
curve12_right <- c((SKULL_curve12+1)[1:length(SKULL_curve12)-1], 71)
curveslide_12 <- cbind(curve12_left, SKULL_curve12, curve12_right)

curve13_left <- c(54, (SKULL_curve13-1)[2:length(SKULL_curve13)])
curve13_right <- c((SKULL_curve13+1)[1:length(SKULL_curve13)-1], 53)
curveslide_13 <- cbind(curve13_left, SKULL_curve13, curve13_right)

curve14_left <- c(56, (SKULL_curve14-1)[2:length(SKULL_curve14)])
curve14_right <- c((SKULL_curve14+1)[1:length(SKULL_curve14)-1], 54)
curveslide_14 <- cbind(curve14_left, SKULL_curve14, curve14_right)

curve15_left <- c(55, (SKULL_curve15-1)[2:length(SKULL_curve15)])
curve15_right <- c((SKULL_curve15+1)[1:length(SKULL_curve15)-1], 53)
curveslide_15 <- cbind(curve15_left, SKULL_curve15, curve15_right)

curve16_left <- c(28, (SKULL_curve16-1)[2:length(SKULL_curve16)])
curve16_right <- c((SKULL_curve16+1)[1:length(SKULL_curve16)-1], 70)
curveslide_16 <- cbind(curve16_left, SKULL_curve16, curve16_right)

curve17_left <- c(70, (SKULL_curve17-1)[2:length(SKULL_curve17)])
curve17_right <- c((SKULL_curve17+1)[1:length(SKULL_curve17)-1], 1)
curveslide_17 <- cbind(curve17_left, SKULL_curve17, curve17_right)

curve18_left <- c(68, (SKULL_curve18-1)[2:length(SKULL_curve18)])
curve18_right <- c((SKULL_curve18+1)[1:length(SKULL_curve18)-1], 19)
curveslide_18 <- cbind(curve18_left, SKULL_curve18, curve18_right)

curve19_left <- c(19, (SKULL_curve19-1)[2:length(SKULL_curve19)])
curve19_right <- c((SKULL_curve19+1)[1:length(SKULL_curve19)-1], 69)
curveslide_19 <- cbind(curve19_left, SKULL_curve19, curve19_right)

curve20_left <- c(27, (SKULL_curve20-1)[2:length(SKULL_curve20)])
curve20_right <- c((SKULL_curve20+1)[1:length(SKULL_curve20)-1], 63)
curveslide_20 <- cbind(curve20_left, SKULL_curve20, curve20_right)

curve21_left <- c(63, (SKULL_curve21-1)[2:length(SKULL_curve21)])
curve21_right <- c((SKULL_curve21b+1)[1:length(SKULL_curve21)-1], 2)
curveslide_21 <- cbind(curve21_left, SKULL_curve21, curve21_right)

curve22_left <- c(18, (SKULL_curve22-1)[2:length(SKULL_curve22)])
curve22_right <- c((SKULL_curve22+1)[1:length(SKULL_curve22)-1], 20)
curveslide_22 <- cbind(curve22_left, SKULL_curve22, curve22_right)

curve23_left <- c(20, (SKULL_curve23-1)[2:length(SKULL_curve23)])
curve23_right <- c((SKULL_curve23+1)[1:length(SKULL_curve23)-1], 62)
curveslide_23 <- cbind(curve23_left, SKULL_curve23, curve23_right)

curve24_left <- c(68, (SKULL_curve24-1)[2:length(SKULL_curve24)])
curve24_right <- c((SKULL_curve24+1)[1:length(SKULL_curve24)-1], 72)
curveslide_24 <- cbind(curve24_left, SKULL_curve24, curve24_right)

curve25_left <- c(61, (SKULL_curve25-1)[2:length(SKULL_curve25)])
curve25_right <- c((SKULL_curve25+1)[1:length(SKULL_curve25)-1], 65)
curveslide_25 <- cbind(curve25_left, SKULL_curve25, curve25_right)

curve26_left <- c(7, (SKULL_curve26-1)[2:length(SKULL_curve26)])
curve26_right <- c((SKULL_curve26+1)[1:length(SKULL_curve26)-1], 23)
curveslide_26 <- cbind(curve26_left, SKULL_curve26, curve26_right)

curve27_left <- c(7, (SKULL_curve27-1)[2:length(SKULL_curve27)])
curve27_right <- c((SKULL_curve27+1)[1:length(SKULL_curve27)-1], 6)
curveslide_27 <- cbind(curve27_left, SKULL_curve27, curve27_right)

curve28_left <- c(80, (SKULL_curve28-1)[2:length(SKULL_curve28)])
curve28_right <- c((SKULL_curve28+1)[1:length(SKULL_curve28)-1], 27)
curveslide_28 <- cbind(curve28_left, SKULL_curve28, curve28_right)

curve29_left <- c(81, (SKULL_curve29-1)[2:length(SKULL_curve29)])
curve29_right <- c((SKULL_curve29+1)[1:length(SKULL_curve29)-1], 28)
curveslide_29 <- cbind(curve29_left, SKULL_curve29, curve29_right)

curve30_left <- c(72, (SKULL_curve30-1)[2:length(SKULL_curve30)])
curve30_right <- c((SKULL_curve30+1)[1:length(SKULL_curve30)-1], 90)
curveslide_30 <- cbind(curve30_left, SKULL_curve30, curve30_right)

curve31_left <- c(65, (SKULL_curve31-1)[2:length(SKULL_curve31)])
curve31_right <- c((SKULL_curve31b+1)[1:length(SKULL_curve31)-1], 89)
curveslide_31 <- cbind(curve31_left, SKULL_curve31, curve31_right)

curve32_left <- c(9, (SKULL_curve32-1)[2:length(SKULL_curve32)])
curve32_right <- c((SKULL_curve32+1)[1:length(SKULL_curve32)-1], 8)
curveslide_32 <- cbind(curve32_left, SKULL_curve32, curve32_right)

curve33_left <- c(91, (SKULL_curve33-1)[2:length(SKULL_curve33)])
curve33_right <- c((SKULL_curve33+1)[1:length(SKULL_curve33)-1], 91)
curveslide_33 <- cbind(curve33_left, SKULL_curve33, curve33_right)

curve34_left <- c(79, (SKULL_curve34-1)[2:length(SKULL_curve34)])
curve34_right <- c((SKULL_curve34+1)[1:length(SKULL_curve34)-1], 79)
curveslide_34 <- cbind(curve34_left, SKULL_curve34, curve34_right)


# all our curveslide matrices
ls(pattern = "curveslide*")
curveslide_list <- lapply(ls(pattern = "curveslide*"), get)
str(curveslide_list)
curveslide_all <- do.call(rbind, curveslide_list)

write.csv(curveslide_all, "./Postprocessing/output/semiLMs_sliding/Calgary_Adult_Cranium_Atlas_Curveslide.csv")

#### 4. Analysing the 3D landmark data with GMM ####
# For example:
skull_array <- morpho.tools.GM::tag2array(string_del = "_Cranium_Landmarks.tag", propagated = TRUE)

GPA_skull <- geomorph::gpagen(A = skull_array, curves = as.matrix(curveslide_all), surfaces = skull_surface.lm)

