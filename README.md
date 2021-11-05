# **MusMorph, a database of standardized mouse morphology data for morphometric meta-analyses**

This repository contains a) Bash/R preprocessing scripts for file conversion and initialization, b) Python/Bash processing scripts for atlas construction, pairwise volumetric image registration, and labelling (e.g., segmentations or landmarks), c) R and Julia postprocessing scripts to optimize your landmark predictions if need be, as well as example R scripts.

## **Keywords**

Mouse, phenomics, craniofacial, imaging pipelines, deep learning, morphometrics, micro-computed tomography, FaceBase

## **Prerequisites for acquiring new data and/or analyzing and visualizing the data**

1. Linux or macOS; 
2. [Medical Imaging NetCDF (MINC) Toolkit](https://github.com/BIC-MNI/minc-toolkit-v2) (or from their [website](https://bic-mni.github.io/)) with local and remote/compute cluster installations. Note that MINC is a modality neutral imaging data format and associated set of tools and libraries developed at the Montreal Neurological Institute (MNI) and freely available online. More information can be found at the [MINC Wikibooks page](http://en.wikibooks.org/wiki/MINC);
3. Volumetric imaging data; 
4. [Python](https://www.python.org/downloads/) and associated packages;
5. [R](https://cran.r-project.org/bin/) and associated packages;
6. [Julia](https://julialang.org/downloads/) and associated packages;
7. A [FaceBase account](https://www.facebase.org).

## **Notes on Data**

The data and metadata are available in the [MusMorph project repository](https://doi.org/10.25550/3-HXMC) on [FaceBase](https://www.facebase.org). After creating a free account and logging in, the MusMorph data and metadata can be downloaded at any level in the project hierarchy using the “Export: BDBag” tool at the top-right of the browser. This export function uses DERIVA, the software platform that powers FaceBase, to generate a BDBag (Big Data Bag) ZIP file. Users then need to download the file and process it via BDBag client tools, either via the command line or GUI application. Specific details about the DERIVA Client installation and the step-by-step export instructions are available here: www.facebase.org/help/exporting.

## **License**

This project is licensed under the GNU General Public License. See the [LICENSE file](./LICENSE.md) for details.

## **Acknowledgments**

We thank the [Advanced Research Computing team](https://it.ucalgary.ca/research-computing-services/our-resources/high-performance-computing-hpc) at the University of Calgary for facilitating image processing and storage on the ARC and Helix compute clusters. We also thank [FaceBase](https://www.facebase.org) and the [International Mouse Phenotyping Consortium](https://www.mousephenotype.org/) for assisting with image data storage and acquisition. Finally, we would like to acknowledge funding from a CIHR Foundation Grant (#159920), an NIH R01 (#2R01DE019638), [Alberta Innovates](https://albertainnovates.ca/) and the [Alberta Children’s Hospital Research Institute](https://research4kids.ucalgary.ca/).
