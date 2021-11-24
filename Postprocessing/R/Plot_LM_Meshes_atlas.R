### PLOT meshes and landmarks on DO atlas

library(rgl)
library(Morpho)
library(Rvcg)
library(magick)
library(morpho.tools.GM)

dir()
setwd("SLIDING_SEMILANDMARKS/")

mandible_mesh <- file2mesh("DO_mandible_segmented_meshlab_atlas.ply")
mandible_lm <- tag2lm("Global_mandible_landmarks.tag")
skull_mesh <- file2mesh("DO_whole_head_atlas_new_position_only_head.ply")
skull_lm <- tag2lm("Global_Skull_68_LMs.tag")
head_mesh <- file2mesh("DO_whole_head_atlas.ply")


#### PLOT MANDIBLE MESH and LANDMARKS ####
open3d(zoom=0.9, windowRect = c(0,0,1000,700)) # bigger RGL window
shade3d(mandible_mesh, color="gray", alpha=0.8) # we are just plotting the mesh we imported. Alpha is the transparency level
plot3d(mandible_lm, aspect="iso", type="s", size=1, col="red", add=T) # plot the landmarks on top


model <- par3d()$modelMatrix
lateral <- par3d()$userMatrix # this is the left side. Add right if needed
superior <- par3d()$userMatrix # showing the top of the head
diff_lateral <- par3d()$userMatrix
# ventral <- par3d()$userMatrix
rgl.close()

save(lateral, superior, diff_lateral, file = "RGL_skull_LM_positions.rdata")

load("RGL_skull_LM_positions.rdata")

open3d(zoom=0.9, userMatrix = lateral, windowRect = c(0,0,1000,700))
shade3d(mandible_mesh, color="gray", alpha=0.8) # we are just plotting the mesh we imported. Alpha is the transparency level
plot3d(mandible_lm, aspect="iso", type="s", size=0.8, col="red", add=T) # plot the landmarks on top
rgl.snapshot("figs/landmarks_lateral_red.png", top = TRUE)
rgl.close()


open3d(zoom=0.9, userMatrix = superior, windowRect = c(0,0,1000,700), zoom = 0.75)
shade3d(mandible_mesh, color="gray", alpha=0.8) # we are just plotting the mesh we imported. Alpha is the transparency level
plot3d(mandible_lm, aspect="iso", type="s", size=0.8, col="blue", add=T) # plot the landmarks on top
rgl.snapshot("figs/landmarks_superior.png", top = TRUE)
rgl.close()




### Plot mandible and skull meshes
open3d(zoom=0.9, userMatrix = lateral, windowRect = c(0,0,1000,700))
shade3d(mandible_mesh, color="grey", alpha=0.8, add = T)
shade3d(skull_mesh, color="blue", alpha=0.8, add = T)
plot3d(mandible_lm, aspect="iso", type="s", size=0.6, col="red", add=T) # plot the landmarks on top

rgl.snapshot("figs/mesh_skull_mandible_open_landmarks.png", top = TRUE)
rgl.close()


### Plot mandible and skull meshes together
open3d(zoom=0.9, userMatrix = lateral, windowRect = c(0,0,1000,700))
shade3d(head_mesh, color="grey", alpha=0.8, add = T)
rgl.snapshot("figs/mesh_skull_mandible_closed2.png", top = TRUE)
plot3d(mandible_lm, aspect="iso", type="s", size=0.6, col="red", add=T)
rgl.snapshot("figs/mesh_skull_mandible_closed_lm.png", top = TRUE)# plot the landmarks on top
plot3d(skull_lm, aspect="iso", type="s", size=1, col="blue", add=T) # plot the landmarks on top
rgl.snapshot("figs/mesh_skull_mandible_closed_lm2_bigger.png", top = TRUE)
rgl.close()