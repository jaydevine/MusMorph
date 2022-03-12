# **MusMorph, a database of standardized mouse morphology data for morphometric meta-analyses**

This repository contains a) [Bash/R preprocessing scripts](https://github.com/jaydevine/MusMorph/tree/main/Preprocessing) for file conversion and initialization, b) [Python/Bash processing scripts](https://github.com/jaydevine/MusMorph/tree/main/Processing) for atlas construction, pairwise volumetric image registration, and labelling (e.g., segmentations or landmarks), and c) [R and Julia postprocessing scripts](https://github.com/jaydevine/MusMorph/tree/main/Postprocessing) to optimize your landmark predictions if need be, as well as example R scripts for morphometrics.

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

Alternatively, if you have [Docker](https://www.docker.com/), our Ubuntu image has all of these dependencies installed. After creating a FaceBase account (see 7. above), download the MusMorph data to a local directory, then pull our Docker image and run it with the data path (e.g., /path/to/data) defined:

`docker pull jaydevine/musmorph:latest`
`docker run --interactive --tty --net=host --privileged --env DISPLAY=$DISPLAY --volume="$HOME/.Xauthority:/root/.Xauthority:rw" --volume="/path/to/data:/home/musmorph/Data" musmorph:latest /bin/bash`

If you do not have data or just want to play around with commands, feel free to remove the second "--volume" option.

## **Notes on Data**

The data and metadata are available in the [MusMorph project repository](https://doi.org/10.25550/3-HXMC) on [FaceBase](https://www.facebase.org). After creating a free account and logging in, the MusMorph data and metadata can be downloaded at any level in the project hierarchy using the “Export: BDBag” tool at the top-right of the browser. This export function uses DERIVA, the software platform that powers FaceBase, to generate a BDBag (Big Data Bag) ZIP file. Users then need to download the file and process it via BDBag client tools, either via the command line or GUI application. Specific details about the DERIVA Client installation and the step-by-step export instructions are available here: www.facebase.org/help/exporting.

## **License**

This project is licensed under the GNU General Public License. See the [LICENSE file](./LICENSE.md) for details.

## **Acknowledgments**

We thank the [Advanced Research Computing team](https://it.ucalgary.ca/research-computing-services/our-resources/high-performance-computing-hpc) at the University of Calgary for facilitating image processing and storage on the ARC and Helix compute clusters. We also thank [FaceBase](https://www.facebase.org) and the [International Mouse Phenotyping Consortium](https://www.mousephenotype.org/) for assisting with image data storage and acquisition. Finally, we would like to acknowledge funding from a CIHR Foundation Grant (#159920), an NIH R01 (#2R01DE019638), [Alberta Innovates](https://albertainnovates.ca/) and the [Alberta Children’s Hospital Research Institute](https://research4kids.ucalgary.ca/).
