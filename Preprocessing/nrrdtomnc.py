#!/usr/bin/env python3

"""
Dependencies required: pynrrd  (pip install pynrrd), teem-unu (sudo apt install teem-apps), numpy (pip install numpy), MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2).

sudo pip3 install --system pynrrd

The script can be ran via python3 nrrdtmnc.py -i filename -p res 
"""

import argparse
from os import listdir, makedirs
from os.path import join, isdir, splitext, basename, dirname, abspath
import subprocess as sp
import numpy as np
from glob import glob
try:
    import nrrd
except ImportError:
    raise ImportError("Failed to import pynrrd. Try 'pip install pynrrd'")

DTYPES = {'uint8': {'np': np.uint8, 'txt': ('unsigned', 'byte')},
          'uint16': {'np': np.uint16, 'txt': ('unsigned', 'short')},
          'unsigned char': {'np': np.uint8, 'txt': ('unsigned', 'byte')},
          'unsigned short': {'np': np.uint16, 'txt': ('unsigned', 'short')}}


def nrrd_to_minc_file(nrrd_file, out_folder, pixel_size):#, mask):

    # Get dimensions from header
    with open(nrrd_file, 'rb') as n: # Had to change 'r' to 'rb'
        header = nrrd.read_header(n)

    # Get dimensions
    dims = [str(x) for x in header['sizes'][::-1]]
    print("Dimensions: {}".format(dims)) # Had to alter the brackets here

    # Get datatype
    sign, dtype = DTYPES[header['type']]['txt']
    np_dtype = DTYPES[header['type']]['np']

    # Create output paths
    if isdir(out_folder) is False:
        makedirs(out_folder)

    sans_ext = splitext(basename(nrrd_file))[0]
    minc_path = join(out_folder, sans_ext) + ".mnc"

    # Stream NRRD data
    try:
        unu_data = sp.Popen(('unu', 'data', nrrd_file), stdout=sp.PIPE)
    except Exception as e:
        try:
            unu_data = sp.Popen(('teem-unu', 'data', nrrd_file), stdout=sp.PIPE)
        except sp.CalledProcessError:
            print("teem-unu is not installed! Get it via apt-get install teem-apps") # Again, brackets for python3 print.

    # Decompress the streamed data from unu data
    if header['encoding'] == 'gzip':
        stream = sp.Popen('gunzip', stdin=unu_data.stdout, stdout=sp.PIPE)
    else:
        stream = unu_data
    # Hash out mask info:
    #if mask: 
    #    value_range = ['-orange', '0', '1']
    #else:
    # Reform try and expect without mask:
    try:
        value_range = ['-real_range', '0', str(np.iinfo(np_dtype).max)]
    except ValueError:
        value_range = ['-real_range', '0', str(np.finfo(np_dtype).max)]

    # Create list of sp calls
    sp_call = ['rawtominc', '-clobber', '-2', '-{}'.format(dtype), '-{}'.format(sign),
               '-xstart', '0',
               '-ystart', '0',
               '-zstart', '0',
               '-xstep', '{}'.format(pixel_size),
               '-ystep', '{}'.format(pixel_size),
               '-zstep', '{}'.format(pixel_size),
               minc_path, dims[0], dims[1], dims[2]]

    sp_call[5:5] = value_range

    # Pass the raw data stream to raw_to_minc
    sp.check_output(sp_call, stdin=stream.stdout)
    unu_data.wait()


if __name__ == "__main__":

    # Mandatory command line arguments
    parser = argparse.ArgumentParser(description="Convert NRRD file to MINC")
    parser.add_argument('--input', '-i', dest='input_folder', help='Input NRRD file/folder of NRRDs', required=True)
    parser.add_argument('--output', '-o', dest='output_folder', help='Output folder', required=False)
    parser.add_argument('--pixel', '-p', dest='pixel_size', help='Pixel size', required=True)
    #parser.add_argument('--mask', '-m', dest='mask', action='store_true', default=False, required=False)

    args = parser.parse_args()
    if not args.output_folder:
        import os
        args.output_folder = os.getcwd()

    nrrd_to_minc_file(args.input_folder, args.output_folder, args.pixel_size)#, args.mask)
