#-------------------------------------------------------------------------------------------------------------------------------------------------
# Julia script for landmark neural net.
#-------------------------------------------------------------------------------------------------------------------------------------------------
# Import packages.
using Pkg
using CSV
using Flux
using Flux: @epochs
using LinearAlgebra
using StatsBase
using DataFrames
using Zygote
using Plots
using BSON
using BSON: @save
using BSON: @load
# using CuArrays # If you want to use the GPU instead of CPU.
#-------------------------------------------------------------------------------------------------------------------------------------------------
# The only notes you need to read, and the only variables you need to alter, are between these lines.
# 1. NOTES:

# A) Follow the code in GPA_and_Projection.R. This involves performing separate GPAs on the manual and registration-derived landmarks,
# then projecting the automated tangent space coordinates into the manual tangent space. It is very important that you remember what
# manual configurations were used in the training set, as this will always be the mean shape on which any registration-derived
# test set must be superimposed. Once the manual and automated configurations are in the same space, combine the
# shape coordinates into a single dataset for import into Julia.

# B) If you want to acquire size information, extract the centroid size vector from the original GPA. In general, registration-based
# size measures (e.g., volumes, linear distances, centroid size) are highly correlated (>0.95) with manual size measures.

# C) Let's assume you have all of your data in /path/to/Landmarks/.

# 2. VARIABLES:

# A) Read in training dataset. Let's assume the first n rows are automated data and last n rows are manual data. The header (line 1) is ignored.
Training_Set = CSV.File("/path/to/Landmarks/<>.csv")
Training_Set = DataFrame(Training_Set)

# B) Read in testing dataset.
Testing_Set = CSV.File("/path/to/Landmarks/<>.csv")
Testing_Set = DataFrame(Testing_Set)

# B) Split the datasets up, convert them to matrices, and transpose. Let's assume the first column has specimen IDs.
x_Train = Matrix(Training_Set[1:n,2:end])'
y_Train = Matrix(Training_Set[n+1:end,2:end])'
x_Test = Matrix(Testing_Set[1:end,2:end])'

# C) Define training and testing data arrays.
x_Train = reshape(collect(x_Train), size(x_Train)[1], size(x_Train)[2])
y_Train = reshape(collect(y_Train), size(y_Train)[1], size(y_Train)[2])
x_Test = reshape(collect(x_Test), size(x_Test)[1], size(x_Test)[2])

# Define whether your data are in two or three (K) dimensions.
K = 3

# Determine how many landmarks (P) there are.
P = trunc(Int, size(x_Train)[1]/K)

#----------------------------------------------------------------------------------------------------------------------------
# Define loss functions.
# First, we define an RMSE loss, as it improves performance over MSE alone.
function RMSE(x,y)
 	return sqrt(sum((x .- y).^2)) * 1 // size(x,1)
end

# Second, we define a TPS loss. See https://github.com/anj1/ThinPlateSplines.jl.git for more detail.
Is_Zero(r::AbstractFloat) = abs(r)<eps(r)
Is_Zero(r) = false
TPS_Basis(r::T) where T<:Any  = Is_Zero(r) ? zero(T) : r*r*log(r)
My_Norm(a) = sqrt(sum(a.^2))

# Define TPS_Kernel for x.
TPS_Kernel(x) = [TPS_Basis(My_Norm(x[i,:] - x[j,:])) for i=1:size(x,1),j=1:size(x,1)]

# Solve the TPS interpolation and return an energy:
function TPS_Solve(x,y,λ)
	Bend = zeros(size(x,2))
    # Number of shape dimensions is P landmarks * K dimensions
	for i = 1:size(x,2)
        X = x[:,i]
        Y = y[:,i]
        X = convert(Array{Float64,2}, reshape(collect(X), P, K))
        Y = convert(Array{Float64,2}, reshape(collect(Y), P, K))

		# Create homogeneous coordinates.
		X_Hom = cat(dims=2,ones(P,1),X)
		Y_Hom = cat(dims=2,ones(P,1),Y)

		# Compute TPS kernel.
		Φ = TPS_Kernel(X)

		# QR decomposition.
		Q,R = qr(X_Hom)
		Q1 = Q[:,1:(K+1)]
		Q2 = Q[:,(K+2):end]

		# Calculate warping coefficients.
		C = Q2*inv(UniformScaling(λ) + Q2'*Φ*Q2)*Q2'*Y_Hom

		# Compute bending energy at a minimum and store in vector.
		Energy = λ*tr(C*Y_Hom')
		Bend[i] = Energy
	end
    # Calculate mean bending energy.
	return mean(Bend)
end

# Add losses together: 0.001 regularization worked best.
function Loss(x,y)
	return RMSE(Model(x), y) + TPS_Solve(Model(x),y,0.001)
end

# Define the architecture. We're going to use P*K units in each layer with rectified linear units as activation.
# Make sure they are not in the final layer.
Model = Chain(
    Dense(P*K, P*K, relu),
    Dense(P*K, P*K, relu),
    Dense(P*K, P*K, relu),
    Dense(P*K, P*K),
    identity)

# Track parameters used to calculate gradient of loss function and use ADAM as optimizer.
Ps = Flux.params(Model)
Opt = ADAM()

# Jointly define training data.
Data = [(x_Train,y_Train)]

# Train the model over 10,000 epochs using a) our loss, b) our dense architecture with RelU, c) the training data,
# and d) the Adam optimizer
@epochs 10000 Flux.train!(Loss, Ps, Data, Opt)

# Save the model and model weights with BSON.
Weights = params(Model);
@save "/path/to/Landmarks/<>.bson" Model
@save "/path/to/Landmarks/<>.bson" Weights

# For future reference, if we want to load the parameters back into our model:
@load "/path/to/Landmarks/<>.bson" Model
@load "/path/to/Landmarks/<>.bson" Weights
Flux.loadparams!(Model, Weights)

# Evaluate the model on your test data.
Preds_Data = collect(transpose(Model(x_Test)))
Preds = DataFrame(Preds_Data)
CSV.write("/path/to/Landmarks/<>.csv", Preds)
