#------------------------------------------------------------------------------------------------
# Base software installations.
#------------------------------------------------------------------------------------------------
FROM ubuntu:latest

# Make installations noninterctive.
ENV DEBIAN_FRONTEND=noninteractive

# Specify working dir.
WORKDIR /app

#------------------------------------------------------------------------------------------------
# Install Bash dependencies.
#------------------------------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    bc \
    bison \
    build-essential \
    cmake \
    curl \
    flex \
    g++ \
    gdebi \
    git \
    imagemagick \
    libarmadillo-dev \
    libc6 \
    libcurl4-openssl-dev \
    libfreetype6-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libjpeg-dev \
    libpng-dev \
    libpq-dev \
    libssh2-1-dev \
    libssl-dev \
    libstdc++6 \
    libuser \
    libuser1-dev \
    libx11-dev \
    libxi6 \
    libxi-dev \
    libxml2-dev \
    libxmu6 \
    libxmu-dev \
    libxmu-headers \
    libz-dev \
    nano \
    octave \
    perl \
    python3.6 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    r-base \
    r-base-dev \
    r-cran-devtools \
    r-cran-randomforest \
    r-cran-rcpparmadillo \
    r-cran-rcppeigen \
    r-cran-rgl \
    r-cran-rjson \
    rrdtool \
    teem-apps \
    wget \
    xauth \
    x11-xserver-utils \
    x11proto-core-dev \
    xorg \
    zlib1g-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*apt

# Upgrade pip and set Pythonpath.
RUN pip3 install --upgrade pip
ENV PYTHONPATH "${PYTHONPATH}:/app"

#------------------------------------------------------------------------------------------------
# Install Python dependencies.
#------------------------------------------------------------------------------------------------
RUN pip3 install \
    numpy \
    pynrrd

#------------------------------------------------------------------------------------------------
# Install R dependencies.
#------------------------------------------------------------------------------------------------
RUN Rscript -e "install.packages('roxygen2')" && \
    Rscript -e "install.packages('Morpho', dependencies=TRUE)" && \
    Rscript -e "install.packages('geomorph', dependencies=TRUE)" && \
    Rscript -e "install.packages('plotrix', dependencies=TRUE)" && \
    Rscript -e "install.packages('Rvcg', dependencies=TRUE)" && \
    Rscript -e "devtools::install_github('marta-vidalgarcia/morpho.tools.GM')" && \
    Rscript -e "devtools::install_github('Mouse-Imaging-Centre/RMINC', upgrade_dependencies=FALSE)"

#------------------------------------------------------------------------------------------------
# Install Julia dependencies.
#------------------------------------------------------------------------------------------------
ENV JULIA_VERSION=1.7.2

RUN mkdir /opt/julia-${JULIA_VERSION} && \
    cd /tmp && \
    wget -q https://julialang-s3.julialang.org/bin/linux/x64/`echo ${JULIA_VERSION} | cut -d. -f 1,2`/julia-${JULIA_VERSION}-linux-x86_64.tar.gz && \
    tar xzf julia-${JULIA_VERSION}-linux-x86_64.tar.gz -C /opt/julia-${JULIA_VERSION} --strip-components=1 && \
    rm /tmp/julia-${JULIA_VERSION}-linux-x86_64.tar.gz

# Symbolic link.
RUN ln -fs /opt/julia-*/bin/julia /usr/local/bin/julia

# Install Julia packages and precompile.
RUN julia -e 'import Pkg; Pkg.add("CSV"); using CSV' && \
    julia -e 'import Pkg; Pkg.add("Flux"); using Flux' && \
    julia -e 'import Pkg; Pkg.add("LinearAlgebra"); using LinearAlgebra' && \
    julia -e 'import Pkg; Pkg.add("StatsBase"); using StatsBase' && \
    julia -e 'import Pkg; Pkg.add("DataFrames"); using DataFrames' && \
    julia -e 'import Pkg; Pkg.add("Zygote"); using Zygote' && \
    julia -e 'import Pkg; Pkg.add("Plots"); using Plots' && \
    julia -e 'import Pkg; Pkg.add("BSON"); using BSON' && \
    julia -e 'import Pkg; Pkg.update()'

#------------------------------------------------------------------------------------------------
# Install MINC Toolkit dependencies.
#------------------------------------------------------------------------------------------------
# New working directory.
WORKDIR /home/musmorph/
ENV HOME /home/musmorph
# Specify MINC toolkit version.
ENV MINC_VERSION=1.9.18

# Get software.
RUN wget https://packages.bic.mni.mcgill.ca/minc-toolkit/Debian/minc-toolkit-${MINC_VERSION}-20200813-Ubuntu_18.04-x86_64.deb && \
    dpkg -i minc-toolkit-${MINC_VERSION}-20200813-Ubuntu_18.04-x86_64.deb && \
    rm -f minc-toolkit-${MINC_VERSION}-20200813-Ubuntu_18.04-x86_64.deb

# Add user to execute commands and source MINC toolkit.
RUN useradd -ms /bin/bash musmorph && \ 
    echo ". /opt/minc/${MINC_VERSION}/minc-toolkit-config.sh" >> /home/musmorph/.bashrc

# Install minc-stuffs.
USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    automake

# Need to clone git repository.
RUN git clone --recursive https://github.com/Mouse-Imaging-Centre/minc-stuffs.git /opt/minc-stuffs && \
    cd /opt/minc-stuffs && \
    ./autogen.sh && \
    ./configure --with-build-path=/opt/minc/${MINC_VERSION} && \
    make && \
    make install && \
    python3 setup.py install

# Make directory tree for MusMorph scripts, data organization, etc. For some reason, mkdir -p functions differently in Docker? Command is clunky here.
RUN mkdir Project Data && \
    cd /home/musmorph/Project && mkdir Scripts Quality Source lsq6 lsq12 nl && \
    cd /home/musmorph/Project/Source && mkdir Blurred MNC Orig Resample Tag XFM && \
    cd /home/musmorph/Project/lsq6 && mkdir Blurred MNC XFM && \
    cd /home/musmorph/Project/lsq12 && mkdir Blurred MNC XFM && \
    cd /home/musmorph/Project/nl && mkdir Ana_Test Blurred INIT MNC XFM && \
    cd /home/musmorph/Project/Scripts && git clone https://github.com/jaydevine/MusMorph.git .

USER musmorph
