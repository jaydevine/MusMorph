# **MusMorph, a database of standardized mouse morphology data for morphometric meta-analyses**

Citation: TBD.

This repository contains a) Bash/R preprocessing scripts for file conversion and initialization, b) Python/Bash processing scripts for atlas construction, pairwise volumetric image registration, and labelling (e.g., segmentations or landmarks), c) R and Julia postprocessing scripts to optimize your landmark predictions if need be, as well as example R scripts.

## **Keywords**

Big data, morphology, phenotyping, genotype-phenotype map, complex traits, morphometrics, micro-computed tomography.

## **Prerequisites for acquiring new data and/or analyzing and visualizing the data**

1. Linux or macOS;
2. [Medical Imaging NetCDF (MINC) Toolkit](https://github.com/BIC-MNI/minc-toolkit-v2) (or from their [website](https://bic-mni.github.io/)) with local and remote/compute cluster installations. Note that MINC is a modality neutral imaging data format and associated set of tools and libraries developed at the Montreal Neurological Institute (MNI) and freely available online. More information can be found at the [MINC Wikibooks page](http://en.wikibooks.org/wiki/MINC);
3. Volumetric imaging data. 
4. [Python](https://www.python.org/downloads/) and associated packages;
5. [R](https://cran.r-project.org/bin/) and associated packages;
6. [Julia](https://julialang.org/downloads/) and associated packages.

## **Notes on Data**

The data and metadata are available on [FaceBase](https://www.facebase.org).

## **License**

This project is licensed under the GNU General Public License. See the [LICENSE file](./LICENSE.md) for details.

## **Acknowledgments**

We thank the [Advanced Research Computing team](https://it.ucalgary.ca/research-computing-services/our-resources/high-performance-computing-hpc) at the University of Calgary for facilitating image processing and storage on the ARC and Helix compute clusters. We also thank [FaceBase](https://www.facebase.org) and the [International Mouse Phenotyping Consortium](https://www.mousephenotype.org/) for assisting with image data storage and acquisition. Finally, we would like to acknowledge funding from a CIHR Foundation Grant (#159920), an NIH R01 (#2R01DE019638), and the [Alberta Children’s Hospital Research Institute](https://research4kids.ucalgary.ca/). 
